import logging
log = logging.getLogger(__name__)

from civicboom.lib.database.get_cached import get_content

from cbutils.text import profanity_check as _profanity_check, get_diff_words, strip_html_tags
from cbutils.worker import config



class ProfanityCheckFailedException(Exception):
    pass


def profanity_check(content, url_base):
    """
    Checks content for profanity
    If there is a profanity
     - replace the content with the cleaned version
     - flag and list the removed words
     
    Todo idea? maybe we could profanity check drafts and tell users that the content has raised an issue before they publish it?
    """
    content = get_content(content)
    
    #if not content:
    #    log.warning("Content not found: %s" % str(content_id))
    #    return False
    assert content
    
    # Cydyne Profanity
    #profanity_response = civicboom.lib.services.cdyne_profanity.profanity_check(content.content)
    
    removed_words = []
    profanity_count = 0
    try:
        for field in ['title','content']:
            text_original      = getattr(content,field)
            profanity_response = _profanity_check(text_original)
            if not profanity_response:
                raise ProfanityCheckFailedException()
            elif profanity_response['FoundProfanity']:
                text_clean = profanity_response['CleanText']
                setattr(content, field, text_clean)
                removed_words += get_diff_words(strip_html_tags(text_original), strip_html_tags(text_clean))
                profanity_count += profanity_response['ProfanityCount']
    except ProfanityCheckFailedException:
        log.debug("Profanity check failed")
        content.flag(comment=u"automatic profanity check failed, please manually inspect", url_base=url_base, moderator_address=config['email.moderator'])
    
    if profanity_count:
        log.debug("Profanitys found")
        content.flag(comment=u"found %d profanities: %s" % (profanity_count, ','.join(removed_words)), url_base=url_base, moderator_address=config['email.moderator'])
    else:
        log.debug("No profanity found")
    
    return True