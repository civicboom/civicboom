""" Das rude library """
import urllib, urllib2, string, logging

from xml.dom import minidom

log = logging.getLogger(__name__)

def get_profanity_count(content):
    """ Try to check if there is profanity - if the server is not available return -1,
    saying that there is and log it! """

    address = "http://ws.cdyne.com/ProfanityWS/Profanity.asmx/SimpleProfanityFilter"
    data = urllib.urlencode({'Text':content})
    request = urllib2.Request(address, data)

    def do_request(request):
        try:
            website = urllib2.urlopen(request)
        except (urllib2.HTTPError, urllib2.URLError), e:
            log.error('The server couldn\'t fulfill the request: Error code: %s', e)
            return False
        return website

    website = do_request(request)
    if website is False:
        #Just try again
        log.debug('trying again')
        website = do_request(request)
        if website is False:
            #give up
            log.debug('giving up')
            return -1

    xml = minidom.parseString(website.read())
    countxml = xml.getElementsByTagName('ProfanityCount')[0]
    count = int(countxml.firstChild.data)
    if count is not 0:
        log.debug('profanity count: %s'%(count))
    return count

