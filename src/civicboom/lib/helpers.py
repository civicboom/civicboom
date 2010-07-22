"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password
from webhelpers.html import HTML
from pylons import url
import re


def shorten_url(url):
    return re.sub("http://[^/]+", "", url)

def shorten_module(mod):
    return re.sub("civicboom/(.*).py", "\\1", mod).replace("/", ".")

def username_plus_ip(username, address):
    if username == "None":
        return address
    return HTML.span(username, title=address)

def link_to_objects(text):
    matches = re.match("(.*)(Content) #(\d+)(.*)", text)
    if matches:
        return HTML.literal(matches.group(1)) + HTML.a(
            matches.group(2)+" #"+matches.group(3),
            href="/admin/"+matches.group(2)+"/models/"+matches.group(3)+"/edit"
        ) + HTML.literal(matches.group(4))
    return text
