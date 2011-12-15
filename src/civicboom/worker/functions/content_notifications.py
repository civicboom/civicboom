from cbutils.worker import config

from cbutils.misc   import now, debug_type

from civicboom.lib.database.get_cached import get_content
from civicboom.lib.database.actions    import respond_assignment
from civicboom.lib.communication       import messages

import datetime


def content_notifications(content, publishing_for_first_time=True):
    content = get_content(content)
    
    assert content
    
    # Comments just notify parent creator --------------------------------------
    if content.__type__ == "comment":
        content.parent.creator.send_notification(
            messages.comment(member=content.creator, content=content, you=content.parent.creator)
        )
        return
    
    # -- Civicboom Notifications -----------------------------------------------
    
    message_to_all_creator_followers = None
    
    # Send notifications about NEW published content
    if publishing_for_first_time:
        
        if   content.__type__ == "article"   :
            message_to_all_creator_followers = messages.article_published_by_followed(creator=content.creator, article   =content)
        elif content.__type__ == "assignment":
            message_to_all_creator_followers = messages.assignment_created           (creator=content.creator, assignment=content)
        
        # if this is a response - notify parent content creator
        if content.parent:
            content.parent.creator.send_notification(
                messages.new_response(member=content.creator, content=content, parent=content.parent, you=content.parent.creator)
            )
            
            # if it is a response, mark the accepted status as 'responded'
            respond_assignment(content.parent, content.creator, delay_commit=True)
        
    # Send notifications about previously published content has been UPDATED
    else:
        if content.__type__ == "assignment":
            if content.update_date < (now()-datetime.timedelta(days=1)): # AllanC - if last updated > 24 hours ago then send an update notification - this is to stop notification spam as users update there assignment 10 times in a row
                message_to_all_creator_followers = messages.assignment_updated(creator=content.creator, assignment=content)
    
    if message_to_all_creator_followers:
        content.creator.send_notification_to_followers(message_to_all_creator_followers, private=content.private)
    
    
    # -- External Aggregation --------------------------------------------------
    
    # Aggregate new content over external services
    if publishing_for_first_time and not content.private:
        content.aggregate_via_creator() # Agrigate content over creators known providers
        twitter_global(content)




def twitter_global(content):
    content = get_content(content)
    
    assert content.__type__  not in ['comment','draft']
    
    # TODO? diseminate new or updated content? This could be done in the originator of this worker
    
    live = config['online'] and config['feature.aggregate.twitter_global']
    from civicboom.lib.aggregation import twitter_global_status
    twitter_global_status(content, live)
