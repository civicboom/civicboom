"""
Low level miscilanious calls
"""

import random
from datetime import date
from decorator import decorator
import pprint

import logging
log = logging.getLogger(__name__)

random_symbols = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
def random_string(length=8):
    r = ''
    for i in range(length):
        r += random_symbols[random.randint(0,len(random_symbols)-1)]
    return r

# AllanC - cant this be removed and replaced with filter()? see python docs for more info on filter
def remove_where(list, check_for_removal_function):
    """
    Remove items from a list is the removal function returns True
    """
    for item in list:
        if check_for_removal_function(item):
            list.remove(item)


def dict_to_stringprint(d, indent=''):
    """
    Iterate though dictionatys and sub dictonarys creating a formatted plain text string
    Useful for debugging
    """
    s = ''
    if hasattr(d,'keys'):
      keylist = d.keys()
      keylist.sort()
      for key in keylist:
        s += key +"\n"+ dict_to_stringprint(d.get(key), indent=indent+'  ')
    elif hasattr(d, '__iter__'):
        for i in d:
            s += dict_to_stringprint(i, indent=indent+'  ')
    elif isinstance(d, basestring):
        s += indent + d.encode("utf-8") + "\n"
    return s


def calculate_age(born):
    """
    Calculate the age of a user.
    http://www.fabent.co.uk/blog/2007/08/04/calculating-age-in-python/
    """
    today = date.today()
    
    try              : birthday = date(today.year, born.month, born.day    )
    except ValueError: birthday = date(today.year, born.month, born.day - 1) # Raised when person was born on 29 February and the current year is not a leap year.
    
    if birthday > today: return today.year - born.year - 1
    else               : return today.year - born.year


def cacheable(time=60*60*24*365, anon_only=True):
    def _cacheable(func, *args, **kwargs):
        from pylons import request, response
        if not anon_only or 'civicboom_logged_in' not in request.cookies: # no cache for logged in users
            response.headers["Cache-Control"] = "public,max-age=%d" % time
            response.headers["Vary"] = "cookie"
            if "Pragma" in response.headers: del response.headers["Pragma"]
            #log.info(pprint.pformat(response.headers))
        return func(*args, **kwargs)
    return decorator(_cacheable)


def obj_to_dict(obj, dict_fields):
    """
    Used to convert a python object to a python dict of strings, but only including requested fields
    TODO: currenly dose not follow lists or dict, just string dumps .. could be useful in future to recusivly call obj_to_dict
    """
    d = {}
    for field_name in dict_fields.keys():
        field_processor = dict_fields[field_name]
        if field_processor == None:
            d[field_name] = unicode(getattr(obj,field_name,''))
        elif type(field_processor)=='function':
            d[field_name] = unicode(field_processor(obj))
    return d

class DictAsObj:
    def __init__(self, d):
        self.__dict__.update(d)