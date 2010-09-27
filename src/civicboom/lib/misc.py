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
            if hasattr(field_value,'keys'):
                pass
            else:
                field_value = unicode(field_value)
        d[field_name] = field_value
    return d


class DictAsObj(UserDict.DictMixin):
    """
    Concept was to return a dictonary that also had it's elements accesiable as object fields
    This will recursivly do this to any sub dicts and lists
    """
    d = {}
    def __init__(self, src):
        d = src.copy()
        for key in d.keys():           # Recursivly Convert Dict's to DictAsObj
            if hasattr(d[key],'keys'): #
                d[key] = DictAsObj(d[key])
            elif hasattr(d[key], '__iter__'): # Iterate though any lists converting dicts to Dict as Obj
                for item in [item for item in d[key] if hasattr(item,'keys')]:
                    item = DictAsObj(item)
        self.d.update(d) # "self.d = d" = setattr, which breaks things
    def __getitem__(self, name):
        return self.d[name]
    def __setitem__(self, name, value):
        self.d[name] = value
    def __delitem__(self, name):
        del self.d[name]
    def keys(self):
        return self.d.keys()
    def __getattr__(self, name):
        return self.d[name]
    def __setattr__(self, name, value):
        self.d[name] = value
