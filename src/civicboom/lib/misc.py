"""
Low level miscilanious calls
"""

import UserDict
import types

import random
from datetime import date
import pprint

import logging
log = logging.getLogger(__name__)

random_symbols = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
def random_string(length=8):
    r = ''
    for i in range(length):
        r += random_symbols[random.randint(0,len(random_symbols)-1)]
    return r


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


def obj_to_dict(obj, dict_fields):
    """
    Used to convert a python object to a python dict of strings, but only including requested fields
    TODO: currenly dose not follow lists or dict, just string dumps .. could be useful in future to recusivly call obj_to_dict
    """
    d = {}
    for field_name in dict_fields.keys():
        field_processor = dict_fields[field_name]
        field_value     = None
        if field_processor == None:
            field_value = getattr(obj,field_name,'')
        elif type(field_processor)==types.FunctionType:
            field_value = field_processor(obj)
        if field_value: #or type(field_value)==types.IntType
            if hasattr(field_value,'keys') or hasattr(field_value, '__iter__'):
                pass
            else:
                field_value = unicode(field_value)
        d[field_name] = field_value
    return d




