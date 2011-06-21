"""
CDYNE Profanity Web Service
http://wiki.cdyne.com/wiki/index.php?title=Profanity_Filter
http://www.webserviceshare.com/reference/language/tools/service/CDYNE-Profanity-Filter-FREE.htm
"""

import urllib
import urllib2
from paste.deploy.converters import asbool

from cbutils.cbxml import readXMLStringtoDic

import logging
log = logging.getLogger(__name__)

filter_operation_address = "http://ws.cdyne.com/ProfanityWS/Profanity.asmx/SimpleProfanityFilter"
#filter_operation_address = "http://ws.cdyne.com/ProfanityWS/Profanity.asmx/ProfanityFilter"


def profanity_check(content):  # pragma: no cover - online services aren't active in test mode
    """
    Try to check if there is profanity
    if the server is not available return None and log error
    
    SimpleProfanityFilter - Basic profanity filter that will replace profanity with "[Explicit]"
        Input:
         Text            : String of text to have filtered.
         LevelToClean    : int between 1 and 100.
         UseNumberFilter : True/False
        
        Output:
         FoundProfanity: Returns Boolean
         ProfanityCount: Returns Integer
         CleanText     : Returns the clean text. profanitys replaced with [Explicit]
    """
    if not content:
        return

    try:
        content = content.encode('utf-8')
    except UnicodeError:
        pass

    data  = urllib.urlencode({
        'Text'           : content ,
        #'LevelToClean'   : '1'     ,
        #'UseNumberFilter': 'True'  ,
    })
    request = urllib2.Request(filter_operation_address, data)

    def do_request(request):
        try:
            response = urllib2.urlopen(request, timeout=10)
        except (urllib2.HTTPError, urllib2.URLError) as e:
            log.error("The CDYNE server couldn't fulfill the request: Error code: %s", e)
            return None
        return response
        
    response = do_request(request)
    if not response:
        response = do_request(request)
    if not response:
        return None

    profanity_response = readXMLStringtoDic(response.read())
    profanity_response = profanity_response['FilterReturn']
    profanity_response['FoundProfanity'] =              asbool(profanity_response['FoundProfanity'])
    profanity_response['ProfanityCount'] =                 int(profanity_response['ProfanityCount'])
    #profanity_response['CleanText']      = urllib.unquote_plus(profanity_response['CleanText']     )

    #if profanity_response['FoundProfanity']:
    return profanity_response
    #return None
