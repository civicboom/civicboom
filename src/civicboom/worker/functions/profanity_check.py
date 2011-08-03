import logging
log = logging.getLogger(__name__)

from civicboom.lib.database.get_cached import get_content

from cbutils.text import profanity_check as _profanity_check
from cbutils.worker import config

#from civicboom.lib.aggregation import twitter_global


def profanity_check(content_id, url_base):
    """
    Checks content for profanity using the CDYNE web service
    If there is a profanity, replace the content with the cleaned version
    """
    content = get_content(content_id)

    if not content:
        log.warning("Content not found: %s" % str(content_id))
        return False
    
    # maybe we could profanity check drafts and tell users that the content has raised an issue before they publish it?
    
    # Cydyne Profanity
    #profanity_response = civicboom.lib.services.cdyne_profanity.profanity_check(content.content)
    
    profanity_response = _profanity_check(content.content)
    
    if not profanity_response:
        log.debug("Profanity check failed")
        content.flag(comment=u"automatic profanity check failed, please manually inspect", url_base=url_base, moderator_address=config['email.moderator'])
    elif profanity_response['FoundProfanity']:
        log.debug("Profanity found")
        content.flag(comment=u"found %s profanities" % profanity_response['ProfanityCount'], url_base=url_base, delay_commit=True, moderator_address=config['email.moderator'])
        content.content = profanity_response['CleanText']
    else:
        log.debug("No profanity found")
        if content.__type__ != 'comment' and content.__type__ != 'draft':
            # TODO? diseminate new or updated content?
            # AllanC - really didnt want this crashing the live server, so wrapped it all in a try except
            try:
                from civicboom.lib.aggregation import twitter_global
                live = config['online'] and config['feature.aggregate.twitter_global']
                twitter_global(content, live)
            except Exception as e:
                log.exception('Global twitter failed')
    
    return True
