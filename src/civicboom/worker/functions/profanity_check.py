import logging
log = logging.getLogger(__name__)

from civicboom.model.meta              import Session
from civicboom.lib.database.get_cached import get_content

from cbutils.text import profanity_check as _profanity_check


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
        content.flag(comment=u"automatic profanity check failed, please manually inspect", url_base=url_base)
    elif profanity_response['FoundProfanity']:
        content.content = profanity_response['CleanText']
        content.flag(comment=u"found %s" % profanity_response['ProfanityCount'], url_base=url_base, delay_commit=True)
    
    return True
