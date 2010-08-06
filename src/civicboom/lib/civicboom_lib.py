"""
Set of helpers specific to the Civicboom project
  (these are not part of misc because misc continas more genereal functions that could be used in a range of projects)
"""

from pylons import url, app_globals
from pylons.i18n.translation import _

from civicboom.model.meta import Session
from civicboom.lib.database.get_cached import get_user

from civicboom.lib.communication.email import send_email

from civicboom.model                   import DraftContent, CommentContent, Media, Tag
from civicboom.lib.database.get_cached import get_content, get_tag

from civicboom.lib.text          import clean_html_markup
from civicboom.lib.misc          import remove_where


from sets import Set # may not be needed in Python 2.7+
import hashlib
import random


#-------------------------------------------------------------------------------
# Pending Users Allowed URL
#-------------------------------------------------------------------------------
# Users in pending status are forced to complete the registration process.
#   some urls have to be made avalable to pending users (such as signout, etc)
pending_user_allowed_list = ['register/new_user','account/signout']
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
        message = _('verify this email address'):
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
    if not form: return content #If there is no form data there is nothing to overlay or do

    # Owner
    if "form_owner" in form:
        content.creator_id = form["form_owner"]
        # Although the form limits the user to a selectable list, any id can be passed here, it is possible that with an API call a user can give content to anyone.
        # FIXME: including people who don't want the content attributed to them...
    else:
        content.creator = c.logged_in_user

    
    # for key in form: print "%s:%s" % (key,form[key])
    
    # from most form values we need to escape '"' and "'" characters as these are used in HTML alt tags and value tags
    
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
        form_file     = form["form_media_file"]
        media = Media()
        media.load_from_file(tmp_file=form_file, original_name=form_file.filename, caption=form["form_media_caption"], credit=form["form_media_credit"])
        media.sync()
        content.attachments.append(media)
        #Session.add(media) # is this needed as it is appended to content and content is in the session?
    
    if 'form_licence' in form:
        content.license_id = form['form_licence']
    
    # Any left over fields that just need a simple set
    for field in ["title", "parent_id"]:
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
