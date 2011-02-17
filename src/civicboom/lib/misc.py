"""
Low level miscilanious calls
"""

import UserDict
import types

import random
from datetime import date
import pprint
import re

import logging
log = logging.getLogger(__name__)

random_symbols = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
def random_string(length=8):
    """
    Generate a random string of a-z A-Z 0-9

    >>> a = random_string()
    >>> len(a)
    8
    >>> b = random_string(10)
    >>> len(b)
    10

    If random, it should compress pretty badly:

    >>> import zlib
    >>> len(zlib.compress(random_string(100))) > 50
    True
    """
    r = ''
    for i in range(length):
        r += random_symbols[random.randint(0,len(random_symbols)-1)]
    return r

def str_to_int(text, default=0):
    try:
        return int(text)
    except:
        pass
    return default

def calculate_age(born):
    """
    Calculate the age of a user.
    http://www.fabent.co.uk/blog/2007/08/04/calculating-age-in-python/

    >>> today = date.today()
    >>> ten_ago = date(today.year-10, today.month, today.day)
    >>> calculate_age(ten_ago)
    10
    >>> born_today = date(today.year, today.month, today.day)
    >>> calculate_age(born_today)
    0
    >>> born_odd = date(2000, 2, 29)
    >>> calculate_age(born_odd) > 0
    True
    """
    today = date.today()
    
    try              : birthday = date(today.year, born.month, born.day    )
    except ValueError: birthday = date(today.year, born.month, born.day - 1) # Raised when person was born on 29 February and the current year is not a leap year.
    
    if birthday > today: return today.year - born.year - 1
    else               : return today.year - born.year

def update_dict(dict_a, dict_b):
    """
    Because dict.update(d) does not return the new dict
    """
    dict_a.update(dict_b)
    return dict_a

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
        if field_value:
            if hasattr(field_value,'keys') or hasattr(field_value, '__iter__'):
                pass
            elif type(field_value)==types.IntType:
                pass
            elif type(field_value)==types.FloatType:
                pass
            else:
                try:
                    field_value = unicode(field_value)
                except:
                    raise Exception('Object types are not allowed in object dictionarys %s %s' % (field_name,field_value))
        d[field_name] = field_value
    return d

def args_to_tuple(*args, **kwargs):
    return (args, kwargs)

def make_username(title):
    """
    turn a display name into a username

    >>> make_username("Bob's Cake Factory")
    'bob-s-cake-factory'
    """
    return re.sub("[^\w-]", "-", title.lower()).strip("-")

