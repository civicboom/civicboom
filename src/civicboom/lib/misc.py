from datetime import date

"""
Low level miscilanious calls
"""

import random

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
    else:
        s += indent + str(d) + "\n"
    return s


def calculateAge(born):
    """
    Calculate the age of a user.
    http://www.fabent.co.uk/blog/2007/08/04/calculating-age-in-python/
    """
    today = date.today()
    
    try              : birthday = date(today.year, born.month, born.day    )
    except ValueError: birthday = date(today.year, born.month, born.day - 1) # Raised when person was born on 29 February and the current year is not a leap year.
    
    if birthday > today: return today.year - born.year - 1
    else               : return today.year - born.year
