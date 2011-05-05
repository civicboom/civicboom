import logging
log = logging.getLogger(__name__)

#import civicboom.lib.services.cdyne_profanity

from civicboom.lib.database.get_cached import get_content
from civicboom.lib.text import profanity_check as _profanity_check

# TODO: this could fire off a thead to perform the profanity checking? (Raised as Feature #55)


def profanity_check(content, url_base):
    """
    Checks content for profanity using the CDYNE web service
    If there is a profanity, replace the content with the cleaned version
    """
    content = get_content(content)
    if not content:
        log.warn('unable to find content to profanity check')
    
    # maybe we could profanity check drafts and tell users that the content has raised an issue before they publish it?
    
    # Cydyne Profanity
    #profanity_response = civicboom.lib.services.cdyne_profanity.profanity_check(content.content)
    
    profanity_response = None # _profanity_check(content.content)
    
    if not profanity_response:
        content.flag(comment=u"automatic profanity check failed, please manually inspect", url_base=url_base)
    elif profanity_response['FoundProfanity']:
        print "found"
        content.content = profanity_response['CleanText']
        content.flag(comment=u"found %s" % profanity_response['ProfanityCount'], url_base=url_base)
