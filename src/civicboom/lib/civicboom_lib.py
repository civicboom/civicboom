"""
Set of helpers specific to the Civicboom project
  (these are not part of misc because misc continas more genereal functions that could be used in a range of projects)
"""

from pylons import url, app_globals, tmpl_context as c, config
from pylons.i18n.translation import _

from civicboom.model.meta import Session
from civicboom.lib.database.get_cached import get_user

from civicboom.lib.communication.email import send_email

from civicboom.model                            import DraftContent, CommentContent, Media, Tag, FlaggedContent, UserLogin
from civicboom.lib.database.get_cached          import get_content, get_tag
from civicboom.lib.database.actions             import del_content
from civicboom.lib.database.polymorphic_helpers import morph_content_to

from civicboom.lib.services.janrain         import janrain
from civicboom.lib.services.cdyne_profanity import profanity_check
from civicboom.lib.services.twitter_global  import status as twitter_global_status
from civicboom.lib.services.tiny_url        import tiny_url

from civicboom.lib.text          import clean_html_markup, strip_html_tags, safe_python_strings
from civicboom.lib.misc          import remove_where
from civicboom.lib.helpers       import truncate



from sets import Set # may not be needed in Python 2.7+
import hashlib
import random
import json

import logging
log      = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# Pending Users Allowed URL
#-------------------------------------------------------------------------------
# Users in pending status are forced to complete the registration process.
#   some urls have to be made avalable to pending users (such as signout, etc)
pending_user_allowed_list = ['register/new_user','account/','widget/', 'misc/']
def deny_pending_user(url_to_check):
    for url_safe in pending_user_allowed_list:
        if url_to_check.find(url_safe)>=0:
            return False
    return True


#-------------------------------------------------------------------------------
# Verify Email
#-------------------------------------------------------------------------------

def send_verifiy_email(user, controller='account', action='verify_email', message=None):
    if not message:
        message = _('verify this email address')
    Session.refresh(user)
    validation_link = url(controller=controller, action=action, id=user.id, host=app_globals.site_host, hash=user.hash())
    message         = _('Please %s by clicking on, or copying the following link into your browser: %s') % (message, validation_link)
    send_email(user.email_unverifyed, subject=_('verify e-mail address'), content_text=message)

def verify_email(user, hash, commit=False):
    user = get_user(user)
    if user and user.hash() == hash:
        user.email            = user.email_unverifyed
        user.email_unverifyed = None
        if commit:
            Session.commit()
        return True
    return False

#-------------------------------------------------------------------------------
# Accounts
#-------------------------------------------------------------------------------

def associate_janrain_account(user, type, token):
    """
    Associate a login record for a Janrain account
    This is called at:
        1.) Registration
        2.) Linking multiple login accounts to a single Civicboom account
    """
    login = None
    try:
        login = Session.query(UserLogin).filter(UserLogin.token == token).filter(UserLogin.type == type).one()
    except:
        pass
    if login:
        if login.user == user: return # If login already belongs to this user then abort
        if login.user: # Warn existing user that account is being reallocated
            login.user.send_email(subject=_('login account reallocated'), content_text=_('your %s account has been allocated to the user %s') % (type, user.username))
        if not config['development_mode']:
            janrain('unmap', identifier=login.token, primaryKey=login.member_id)
        login.user   = user
    else:
        login = UserLogin()
        login.user   = user
        login.type   = type
        login.token  = token
        Session.add(login)
    Session.commit()
    if not config['development_mode']:
        janrain('map', identifier=login.token, primaryKey=login.member_id) # Let janrain know this users primary key id, this is needed for agrigation posts

#-------------------------------------------------------------------------------
# Password Setter
#-------------------------------------------------------------------------------
# don't know if this is right place, but related account stuff was the closest I could think of

def set_password(user, token):
    # search for existing record and remove it
    try:    Session.delete(Session.query(UserLogin).filter(user=user).filter(token=token).one())
    #try: Session.execute(UserLogin.__table__.delete().where(and_(UserLogin.__table__.c.member_id == user.id, UserLogin.__table__.c.token == token)))
    except: pass
    # Set new password
    u_login = UserLogin()
    u_login.user   = user
    u_login.type   = 'password'
    u_login.token  = token
    Session.add(u_login)


#-------------------------------------------------------------------------------
# Content Aggrigation
#-------------------------------------------------------------------------------


def aggregation_dict(content, safe_strings=True):
    """
    Gets a Python dict summary version of this content for aggregation via Janrain
    https://rpxnow.com/docs#api_activity
    
    safe_strings will escape all harful characters. This is used for constructing a javascript representaion for the Janrain Widget in javascript code
    """
    
    content_preview = {}
    
    content_url = url(host=app_globals.site_host, controller='content', action='view', id=content.id)

    def action(content):
        if   content.__type__ == "assignment": return _("Set an _assignment")
        elif content.parent                  : return _("Wrote a response")
        elif content.__type__ == "article"   : return _("Wrote an _article")
    
    def description(content):
        return "%s: %s" % (action(content), content.title)

    def action_links(content):
        action_links = []
        action_links.append({'href':url(host=app_globals.site_host, controller='content_actions', action='edit'  , form_parent_id=content.id), 'text':_('Write a response')  })
        if content.__type__ == "assignment":
            action_links.append({'href':url(host=app_globals.site_host, controller='content_actions', action='accept', id            =content.id), 'text':_('Accept _assignment')})
        return action_links
    
    def media(content):
        media_list = []
        for media in content.attachments:
            if   media.type    == "image": media_list.append({'href':content_url, 'type':"image", 'src':media.thumbnail_url})
            elif media.subtype == "mp3"  : media_list.append({'href':content_url, 'type':"mp3"  , 'src':media.media_url    })
        return media_list
    
    def properties(content):
        properties = {}
        if content.__type__ == "article":
            properties['Rating'] = content.rating
        # TODO: Additional properties
        #"Location": {
        #  "href": "http:\/\/bit.ly\/3fkBwe",
        #  "text": "North Portland"
        #},
        return properties

    content_preview['url']                    = content_url
    content_preview['title']                  = content.title
    content_preview['action']                 = action(content)
    content_preview['description']            = description(content)
    content_preview['user_generated_content'] = truncate(safe_python_strings(strip_html_tags(content.content)))
    content_preview['action_links']           = action_links(content)
    content_preview['media']                  = media(content)
    content_preview['properties']             = properties(content)
    
    if safe_strings:
        content_preview = safe_python_strings(content_preview)
    
    return content_preview


def aggregate_via_user(content, user):
    """
    Call janrain 'activity' for all known accounts for this user
    https://rpxnow.com/docs#api_activity
    
    Requires Janrain Pro
    """
    #content = get_content(content)
    #user    = get_user(user)
    #if not content: return
    #if not user   : return
    content_json = json.dumps(aggregation_dict(content))
    location = ''
    if content.location:
        location = '%s %s' % (content.location.coords(Session)[1], content.location.coords(Session)[0])
        
    if config['feature.aggregate.janrain']:
        for login in [login for login in user.login_details if login.type!='password']:
            janrain('activity', identifier=login.token, activity=content_json, location=location)
    else:
        log.debug('janrain aggregation disabled: \n%s' % content_json)



def twitter_global(content):
    """
    Twitter content via Civicbooms global feed
    
    In the future should maybe be linked to the Civicboom user, and all users could have twitter keys stored
    """

    content_dict = aggregation_dict(content, safe_strings=True)

    # Create Twitter message with tiny URL
    if len(content_dict['title']) > 70:
        title           = truncate(content_dict['title']                 , length=70)
        content_preview = truncate(content_dict['user_generated_content'], length=30)
    else:
        title           = content_dict['title']
        content_preview = truncate(content_dict['user_generated_content'], length=100-len(content_dict['title']))
    
    twitter_post = {}
    twitter_post['status'] = "%s: %s (%s)" % (title, content_preview, tiny_url(content_dict['url']))

    # Add location if avalable
    if content.location:
        twitter_post['lat']                 = content.location.coords(Session)[1]
        twitter_post['long']                = content.location.coords(Session)[0]
        twitter_post['display_coordinates'] = True
    
    # Optional ideas
    # t['in_reply_to_status_id '] # If this is a reply to another tweet (could be good in the future if we can store master tweets)
    # t['trim_user'] = False? default?
    # t['place_id']  = "" #need reverse Geocode using the twitter api call geo/reverse_geocode
    # t['include_entities'] = True
    if config['feature.aggregate.twitter_global']:
        twitter_global_status(twitter_post)
    else:
        log.debug('twitter_global aggregation disabled: \n%s' % twitter_post)

#-------------------------------------------------------------------------------
# Content Management
#-------------------------------------------------------------------------------


#------------------------------
# Form POST contains Content
#------------------------------
# AllanC - is there a way this can be placed at the end of the file away from the rest of the edit action for clarity?
def form_post_contains_content(form):
    """
    Check if a range of required fields are not null
    Returns boolean
    """
    return_bool = False
    if form:
        for field in ("title","content","media_file"):
            if "form_"+field in form and form["form_"+field]:
                return_bool = True
    return return_bool
  


#------------------------------
# Form POST to Content Object
#------------------------------
def form_to_content(form, content):
    """
    Takes form post data and either overlays the form with an existing object or create the relevent content object type and overlay form data
    Will never return None - will always return at leist an empty content object
    """
    
    if not content:
        if   not form                          : content = DraftContent()
        elif form.get('form_type') == "comment": content = CommentContent()
        else                                   : content = DraftContent()
        content.creator = c.logged_in_user
        
    if not content.parent and "form_parent_id" in form:
        content.parent_id = form["form_parent_id"]
        
    if not form: return content #If there is no form data there is nothing to overlay or do

    #----------------------------------------------------
    # Morph content type before overlaying any form data
    #----------------------------------------------------
    # As mophing functions alter the data at the database level, we perform the morph before we ever chnage any of the contents data

    """
    # If we are publishing from a draft and draft is linked to a publish id
    if 'submit_publish' in form and content.__type__ == "draft" and content.publish_id:
        # Get the original published content object and overlay the cloned draft
        old_draft_id = content.id
        content = get_content(content.publish_id)
        if content:
            del_content(old_draft_id) # This is kind of risky because if there is a problem with the form post and it does not commit, the old draft is los
        else:
            content = DraftContent() # The existing article the publish_id is pointing too does not exisit any more, so the content should be saved as a draft, 
        
        #if not content.editable_by(c.logged_in_user): # AllanC - do we need to double double check this user has permissions on this content to do this?
        #    raise exception


    # If we are trying to save a draft over a published content object
    if 'submit_draft' in form and content.__type__ != "draft":
        # Rather than changing the published object, we create a draft clone of
        # it that remebers the id of the orrignal content it was cloned from.
        # Before we create this new clone, check the DB to see if there is an
        # existing draft record associated with this published content
        try:
            content = Session.query(DraftContent).filter_by(publish_id=content.id).one()
        except:
            content_clone = DraftContent()
            content_clone.publish_id = content.id
            content = content_clone
            # The content will be populated with the form data and commited by the controler
    """

    if 'form_type' in form:
        content = morph_content_to(content, form['form_type'])


    #-------------------------------
    # Overlay Form over Base Content
    #-------------------------------
    # Owner
    if "form_owner" in form:
        content.creator_id = form["form_owner"]
        # Although the form limits the user to a selectable list, any id can be passed here, it is possible that with an API call a user can give content to anyone.
        # FIXME: including people who don't want the content attributed to them...
    elif content.creator == None:
        content.creator = c.logged_in_user

    
    # for key in form: print "%s:%s" % (key,form[key])
    
    # TODO: from most form values we need to escape '"' and "'" characters as these are used in HTML alt tags and value tags
    
    # Content
    if "form_content" in form:
        content.content = clean_html_markup(form["form_content"])

    # Tags
    if "form_tags" in form:
        form_tags    = [tag for tag in form["form_tags"].split(" ") if tag!=""] # Get tags from form removing any empty strings
        content_tags = [tag.name for tag in content.tags]                     # Get tags form current content object
        
        # Add any new tag objects
        for tag in Set(form_tags).difference(content_tags):
            content.tags.append(get_tag(tag))

        # Remove any missing tag objects
        def remove_check(tag):
            return tag.name in Set(content_tags).difference(form_tags)
        remove_where(content.tags, remove_check)

    # Existing Media Form Fields
    for media in content.attachments:
        # Update media item fields
        caption_key = "form_media_caption_%d" % (media.id)
        if caption_key in form:
            media.caption = form[caption_key]
        credit_key = "form_media_credit_%d"   % (media.id)
        if credit_key in form:
            media.credit = form[credit_key]
        # Remove media if required
        if "form_file_remove_%d" % media.id in form:
            content.attachments.remove(media)

    # Add Media - if file present in form post
    if 'form_media_file' in form and form['form_media_file'] != "":
        form_file = form["form_media_file"]
        media = Media()
        media.load_from_file(tmp_file=form_file, original_name=form_file.filename, caption=form["form_media_caption"], credit=form["form_media_credit"])
        content.attachments.append(media)
        #Session.add(media) # is this needed as it is appended to content and content is in the session?

    if 'form_licence' in form:
        content.license_id = form['form_licence']

    # Any left over fields that just need a simple set
    for field in ["title", ]:
        form_field_name = "form_"+field
        if form_field_name in form:
            setattr(content,field,form[form_field_name])

    

    return content

#---------------------------------------
# Generate and Store Content Upload Key
#---------------------------------------
# Generate tempory content unique key in memcache for additional media appends from flash or javascript
def get_content_media_upload_key(content):
    """
    Generate/Get a tempory key associated with this content
    The tempory key stays active for "x" minuets in memcache (so page reloads can refer to the same key)
    The key is used for file uploads from sources that cannot send the authentication cookie each time
    
    Suggestion: This could be persisted in the database? Maybe a separate database JUST for tempory stuff like this
    """
    if not content or content.id == None: return ""
    content_id_key  = "content_upload_%d" % content.id
    memcache_expire = 60*60 # memcache expire time in seconds 60*60 = 1 Hour
    mc              = app_globals.memcache
    key             = mc.get(content_id_key)
    if not key:
        key = hashlib.md5(str(random.random())).hexdigest()
        mc.set(content_id_key,             key, time=memcache_expire)
        mc.set(key           , str(content.id), time=memcache_expire)
    return key


#------------------------------
# Profanity Check
#------------------------------
def profanity_filter(content, delay_commit=False):
    """
    Checks content for profanity using the CDYNE web service
    If there is a profanity, replace the content with the cleaned version
    """
    content = get_content(content)
    if not content                           : return
    if not config['feature.profanity_filter']: return
    
    # TODO: this could fire off a thead to perform the profanity checking? (Raised as Feature #55)

    # maybe we could profanity check drafts and tell users that the content has raised an issue before they publish it?
    
    profanity_response = profanity_check(content.content)
    if not profanity_response:
        content.flag(comment=u"automatic profanity check failed, please manually inspect")
    elif profanity_response['FoundProfanity']:
        content.content = profanity_response['CleanText']
        content.flag(comment=u"found %s" % profanity_response['ProfanityCount'])
        #send_email(config['email.moderator'],
        #    subject=_('profanity detected'),
        #    content_text="%s" % (url(controller='content', action='view', id=content.id))
        #    )
        #content.status = "pending"
        #if not delay_commit:
        #    Session.commit()
        #update_content(content)
        #return False
    #return True

