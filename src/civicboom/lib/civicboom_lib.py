"""
Set of helpers specific to the Civicboom project
  (these are not part of misc because misc continas more genereal functions that could be used in a range of projects)
"""

import civicboom.lib.constants as constants
from civicboom.lib.base import url, app_globals, c, config, _


from civicboom.model.meta import Session

from civicboom.lib.communication.email_lib import send_email

from civicboom.model                            import DraftContent, ArticleContent, AssignmentContent, CommentContent, Media, Tag, FlaggedContent, UserLogin, PaymentAccount
from civicboom.lib.database.get_cached          import get_content, get_tag, get_member
from civicboom.lib.database.actions             import del_content


from civicboom.lib.services.janrain         import janrain
from civicboom.lib.services.cdyne_profanity import profanity_check
from civicboom.lib.services.twitter_global  import status as twitter_global_status
from civicboom.lib.services.tiny_url        import tiny_url

from civicboom.lib.text          import clean_html_markup, strip_html_tags, safe_python_strings
from civicboom.lib.helpers       import truncate


from sets import Set # may not be needed in Python 2.7+
import hashlib
import random
import json
import datetime

import logging
log      = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# Pending Users Allowed URL
#-------------------------------------------------------------------------------
# Users in pending status are forced to complete the registration process.
#   some urls have to be made avalable to pending users (such as signout, etc)
pending_user_allowed_list = ['register/new_user','account/','widget/', 'misc/', '/accept']
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
#    Session.refresh(user)
    validation_link = url(controller=controller, action=action, id=user.id, hash=user.hash(), subdomain='') # Need https here?
    message         = _('Please %s by clicking on, or copying the following link into your browser: %s') % (message, validation_link)
    send_email(user.email_unverified, subject=_('verify e-mail address'), content_text=message)


def verify_email(user, hash, commit=False):
    user = get_member(user)
    if user and user.hash() == hash:
        if user.email_unverified:
            user.email            = user.email_unverified
            user.email_unverified = None
        if commit:
            Session.commit()
        return True
    return False


def send_forgot_password_email(user):
    validation_link = url(controller='account', action='forgot_password', protocol='https', id=user.username, hash=user.hash(), subdomain='')
    message         = _('Please click or copy the following link into your browser to reset your password: %s' % validation_link)
    user.send_email(subject=_('reset password'), content_text=message)


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
        if login.user == user:
            return # If login already belongs to this user then abort
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

def set_password(user, new_token, delay_commit=False):
    """
    Set password
    WARNING! We assume the user has already been authenticated
    - remove old password (if found)
    - create new password record
    """
    # search for existing record and remove it
    #
    try:
        #existing_login = Session.query(UserLogin).filter(UserLogin.user==user, UserLogin.type=='password').one()
        for existing_login in [login for login in user.login_details if login.type=='password']:
            log.debug("removing password for %s" % user.username)
            #if existing_login.token == old_token: raise Exception('old password token does not match - aborting password change')
            Session.delete(existing_login)
            log.debug("removed ok")
    #try: Session.execute(UserLogin.__table__.delete().where(and_(UserLogin.__table__.c.member_id == user.id, UserLogin.__table__.c.token == token)))
    except:
        pass
    # Set new password
    u_login = UserLogin()
    u_login.user   = user
    u_login.type   = 'password'
    u_login.token  = new_token
    Session.add(u_login)
    
    if not delay_commit:
        Session.commit()



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
    
    content_url          = url('content', id=content['id'], subdomain='')
    content_creator_name = content.get('creator',{}).get('name', '')

    def action(content):
        if   content.get('type'  ) == "assignment": return content_creator_name + _("Created a _assignment")
        elif content.get('parent')                : return content_creator_name + _("Wrote a response"  )
        elif content.get('type'  ) == "article"   : return content_creator_name + _("Wrote _article" )
    
    def description(content):
        return "%s: %s" % (action(content), content.get('title'))

    def action_links(content):
        action_links = []
        action_links.append(    {'href':url('new_content'   ,                  parent_id=content['id'], subdomain=''), 'text':_('Write a response')  })
        if content.get('type') == "assignment":
            action_links.append({'href':url('content_action', action='accept', id       =content['id'], subdomain=''), 'text':_('Accept _assignment')})
        return action_links
    
    def media(content):
        media_list = []
        if not content.get('attachments'):
            media_list.append({'href':content_url, 'type':"image", 'src':content.get('thumbnail_url')})
        else:
            for media in content.get('attachments'):
                if media.get('type')=="image":
                    media_list.append({'href':content_url, 'type':"image", 'src':media.get('thumbnail_url')})
                if media.get('subtype')=="mp3":
                    media_list.append({'href':content_url, 'type':"mp3"  , 'src':media.get('media_url')    })
        return media_list
    
    def properties(content):
        properties = {}
        if content.get('type') == "article":
            properties['Rating'] = content.get('rating')
        # TODO: Additional properties
        #"Location": {
        #  "href": "http:\/\/bit.ly\/3fkBwe",
        #  "text": "North Portland"
        #},
        return properties

    content_preview['url']                    = content_url
    content_preview['title']                  = content.get('title')
    content_preview['action']                 = action(content)
    content_preview['description']            = description(content)
    content_preview['user_generated_content'] = truncate(safe_python_strings(strip_html_tags(content['content'])), length=100, indicator=_('... read more'), whole_word=True)
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
    #user    = get_member(user)
    #if not content: return
    #if not user   : return
    content_json = json.dumps(aggregation_dict(content.to_dict('full')))
    location = ''
    if content.location:
        location = '%s %s' % (content.location.coords(Session)[1], content.location.coords(Session)[0])
        
    if config['online'] and config['feature.aggregate.janrain']:
        # AllanC: Q Does this need to be done for each login method? or does janrain handle this?
        for login in [login for login in user.login_details if login.type!='password']:
            janrain('activity', identifier=login.token, activity=content_json, location=location)
    else:
        log.info('janrain aggregation disabled: \n%s' % content_json)



def twitter_global(content):
    """
    Twitter content via Civicbooms global feed
    
    In the future should maybe be linked to the Civicboom user, and all users could have twitter keys stored
    """
    #if isinstance(content, Content):
    #    content = content.to_dict('full')
    #content_dict = aggregation_dict(content, safe_strings=True)

    if config['online'] and config['feature.aggregate.twitter_global']:
        link = tiny_url(content.__link__())
    else:
        link = 'http://tinyurl.com/xxxxxxx'

    # Create Twitter message with tiny URL
    if len(content.title) > 70:
        title           = truncate(content.title  , length=70)
        content_preview = truncate(content.content, length=30)
    else:
        title           = content.title
        content_preview = truncate(content.content, length=100-len(content.title))
    
    twitter_post = {}
    twitter_post['status'] = "%s: %s (%s)" % (title, content_preview, link)

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
    if config['online'] and config['feature.aggregate.twitter_global']:
        twitter_global_status(twitter_post)
    else:
        log.info('twitter_global aggregation disabled: \n%s' % twitter_post)

#-------------------------------------------------------------------------------
# Content Management
#-------------------------------------------------------------------------------


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
    if not config['online']                  : return
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



#-------------------------------------------------------------------------------
# Signin Actions
#-------------------------------------------------------------------------------


def get_action_objects_for_url(action_url=None):
    """
    If signing in and performing an action
    Will return ()
    
    """
    from civicboom.lib.web     import current_url
    from civicboom.lib.helpers import get_object_from_action_url
    from civicboom.controllers.members  import MembersController
    from civicboom.controllers.contents import ContentsController
    content_show = ContentsController().show
    member_show  = MembersController().show

    
    # If performing an action we may want to display a custom message with the login
    if not action_url:
        action_url = current_url()
    for action_identifyer, action_action, action_description in constants.actions_list:
        if action_identifyer in action_url:
            args, kwargs = get_object_from_action_url( action_url )
            if args and kwargs:
                # Generate action object frag URL
                kwargs['format'] = 'frag'
                action_object_frag_url = url(*args, **kwargs)
                # Find action object
                if 'content' in args and 'id' in kwargs:
                    action_object = content_show(id=kwargs['id']).get('data')
                if 'member' in args and 'id' in kwargs:
                    action_object = member_show(id=kwargs['id']).get('data')
            return dict(
                action        = action_action          ,
                description   = action_description     ,
                action_object = action_object          ,
                frag_url      = action_object_frag_url ,
            )
    return {}
