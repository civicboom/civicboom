"""
Low level miscilanious calls
"""

import UserDict
import types

import random
import datetime
import pprint
import re

import logging
log = logging.getLogger(__name__)


now_override = None
def now():
    """
    A passthough to get now()
    We can override this so that automated tests can fake the current datetime
    """
    if now_override:
        return now_override
    return datetime.datetime.now()
def set_now(new_now_override=None):
    global now_override
    now_override = None
    if isinstance(new_now_override, datetime.datetime):
        now_override = new_now_override

def timedelta_str(string_args):
    """
    Convert a string containing comma separted timedelta kwargs into a timedeta object
    
    >>> timedelta_str(           "hours=10"  ) == datetime.timedelta(         hours=10)
    True
    >>> timedelta_str("days = 10, hours = 10") == datetime.timedelta(days=10, hours=10)
    True
    >>> timedelta_str(datetime.timedelta(minutes=1)) == datetime.timedelta(minutes=1)
    True
    """
    if isinstance(string_args, basestring):
        return datetime.timedelta(**dict([(kwarg.split('=')[0].strip(), int(kwarg.split('=')[1].strip())) for kwarg in string_args.split(',')]))
    return string_args

def random_string(length=8):
    """
    Generate a random string of a-z A-Z 0-9
    (Without vowels to stop bad words from being generated!)

    >>> len(random_string())
    8
    >>> len(random_string(10))
    10

    If random, it should compress pretty badly:

    >>> import zlib
    >>> len(zlib.compress(random_string(100))) > 50
    True
    """
    random_symbols = '1234567890bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
    r = ''
    for i in range(length):
        r += random_symbols[random.randint(0,len(random_symbols)-1)]
    return r


def str_to_int(text, default=0):
    """
    >>> str_to_int("3")
    3
    >>> str_to_int("moo")
    0
    >>> str_to_int(None)
    0
    >>> str_to_int(str_to_int)
    0
    >>> str_to_int("cake", default=6)
    6
    """
    try:
        return int(text)
    except (ValueError, TypeError):
        return default


def calculate_age(born):
    """
    Calculate the age of a user.
    http://www.fabent.co.uk/blog/2007/08/04/calculating-age-in-python/

    >>> today = datetime.date.today()
    >>> ten_ago = datetime.date(today.year-10, today.month, today.day)
    >>> calculate_age(ten_ago)
    10
    >>> calculate_age(ten_ago - datetime.timedelta(days=3))
    10
    >>> calculate_age(ten_ago + datetime.timedelta(days=3))
    9
    >>> calculate_age(datetime.date.today())
    0
    >>> born_odd = datetime.date(2000, 2, 29)
    >>> calculate_age(born_odd) > 0
    True
    """
    today = datetime.date.today()
    
    try:
        birthday = datetime.date(today.year, born.month, born.day    )
    except ValueError:
        birthday = datetime.date(today.year, born.month, born.day - 1) # Raised when person was born on 29 February and the current year is not a leap year.
    
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year


def update_dict(dict_a, dict_b):
    """
    Because dict.update(d) does not return the new dict

    >>> a = {'a': 1, 'b': 2}
    >>> update_dict(a, {'b': 3, 'c': 3})
    {'a': 1, 'c': 3, 'b': 3}
    """
    dict_a.update(dict_b)
    return dict_a


def obj_to_dict(obj, dict_fields):
    """
    Used to convert a python object to a python dict of strings, but only including requested fields
    dict_fields is a dictionary of functions
       if a key is set will a null function - it will check if it is a primitive type
       if a key is set with a function      - that function is used to convert the object to a primitive type
    TODO: currenly does not follow lists or dict, just string dumps .. could be useful in future to recusivly call obj_to_dict

    >>> class a:
    ...    foo = "bar"
    ...    def __unicode__(self):
    ...        raise Exception('asdf')
    ...
    >>> b = a()
    >>> b.c = a()
    >>> obj_to_dict(b, {'foo': None})
    {'foo': u'bar'}
    >>> obj_to_dict(b, {'c': None})
    Traceback (most recent call last):
        ...
    Exception: Object types are not allowed in object dictionaries [c]
    """
    d = {}
    for field_name in dict_fields:
        field_processor = dict_fields[field_name]
        field_value     = None
        if field_processor == None:
            field_value = getattr(obj,field_name,'')
        elif type(field_processor)==types.FunctionType:
            field_value = field_processor(obj)
        if field_value:
            if hasattr(field_value,'keys') or hasattr(field_value, '__iter__'):
                pass
            elif type(field_value)==types.IntType or type(field_value)==types.FloatType:
                pass
            elif type(field_value) == datetime.datetime:
                field_value = field_value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                try:
                    field_value = unicode(field_value)
                except:
                    raise Exception('Object types are not allowed in object dictionaries [%s]' % (field_name, ))
        d[field_name] = field_value
    return d


def args_to_tuple(*args, **kwargs):
    """
    >>> args_to_tuple()
    ((), {})

    >>> args_to_tuple("hello?")
    (('hello?',), {})

    >>> args_to_tuple("hello", name="dave")
    (('hello',), {'name': 'dave'})
    """
    return (args, kwargs)


def make_username(title):
    """
    turn a display name into a username

    >>> make_username("Bob's Cake Factory")
    'bob-s-cake-factory'
    """
    return re.sub("[^\w-]", "-", title.lower()).strip("-")
