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
    """
    Scan a string for "blah blah Content #42 blah blah" and replace
    "Content #42" with a link to the object editor
    """
    active_word = None
    output = HTML.literal()
    for word in text.split():
        id_match = re.match("#(\d+)", word)
        if active_word and id_match:
            output = output + HTML.a(active_word + " " + word, href="/admin/"+active_word+"/models/"+id_match.group(1)+"/edit")
        elif word[0] == word[0].capitalize(): # if the word starts with a capital
            active_word = word
        else:
            output = output + HTML.literal(word)
            active_word = None
        output = output + HTML.literal(" ")
    return output
