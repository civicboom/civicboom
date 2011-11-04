from civicboom.lib.base import url, config, _

from civicboom.lib.services.twitter_global import status as twitter_global_status
from civicboom.lib.services.janrain        import janrain
from civicboom.lib.helpers                 import truncate
from civicboom.model.meta import Session
from cbutils.tiny_url import tiny_url
from cbutils.text     import strip_html_tags, safe_python_strings

import simplejson as json

import logging
log      = logging.getLogger(__name__)


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
    
    content_url          = url('content', id=content['id'], sub_domain='www', qualified=True)
    content_creator_name = content.get('creator', {}).get('name', '')

    def action(content):
        if content.get('type') == "assignment":
            return content_creator_name + _("Created a _assignment")
        elif content.get('parent'):
            return content_creator_name + _("Wrote a response"  )
        elif content.get('type') == "article":
            return content_creator_name + _("Wrote _article" )
    
    def description(content):
        return "%s: %s" % (action(content), content.get('title'))

    def action_links(content):
        action_links = []
        action_links.append(    {'href':url('new_content'   ,                  parent_id=content['id'], sub_domain='www', qualified=True), 'text':_('Write a response')  })
        if content.get('type') == "assignment":
            action_links.append({'href':url('content_action', action='accept', id       =content['id'], sub_domain='www', qualified=True), 'text':_('Accept _assignment')})
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
        for login in [login for login in user.login_details if login.type != 'password']:
            janrain('activity', identifier=login.token, activity=content_json, location=location)
    else:
        log.info('janrain aggregation disabled: \n%s' % content_json)



def twitter_global(content, live=False):
    """
    Twitter content via Civicbooms global feed
    
    In the future should maybe be linked to the Civicboom user, and all users could have twitter keys stored
    """
    #if isinstance(content, Content):
    #    content = content.to_dict('full')
    #content_dict = aggregation_dict(content, safe_strings=True)

    if live:
        link = tiny_url(content.__link__())
    else:
        link = 'http://tinyurl.com/xxxxxxx'

    title           = strip_html_tags(content.title  )
    content_preview = strip_html_tags(content.content)
    
    # Create Twitter message with tiny URL
    if len(title) > 70:
        title           = truncate(title          , length=70)
        content_preview = truncate(content_preview, length=30)
    else:
        content_preview = truncate(content_preview, length=100-len(title))
    
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
    if live:
        twitter_global_status(**twitter_post)
    else:
        log.info('twitter_global aggregation disabled: \n%s' % twitter_post)
