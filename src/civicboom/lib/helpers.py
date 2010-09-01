"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""

#from webhelpers.html.tags import checkbox, password
from webhelpers.pylonslib.secure_form import authentication_token

from pylons import url, config, app_globals, tmpl_context as c, request
from webhelpers.html import HTML, literal
from webhelpers.text import truncate

from civicboom.lib.text import scan_for_embedable_view_and_autolink

import recaptcha.client.captcha as librecaptcha
import re
import urllib

def get_captcha(lang='en', theme='white'):
    """
    Generate reCAPTCHA html
    (currently the python-recaptcha API does not support the lang or theme option, but these are fields in the html, maybe we need a modifyed version, see the django example for more info)
    http://k0001.wordpress.com/2007/11/15/using-recaptcha-with-python-and-django/
    """
    return literal(librecaptcha.displayhtml(config['api_key.reCAPTCHA.public'])) #, lang="es", theme='white'

def get_janrain(lang='en', theme='', **kargs):
    query_params = ""
    for karg in kargs:
        query_params += karg+"="+str(kargs[karg])
    if query_params != "":
        query_params = urllib.quote_plus("?"+query_params)
    return literal(
        """<iframe src="http://civicboom.rpxnow.com/openid/embed?token_url=%s&language_preference=%s"  scrolling="no"  frameBorder="no"  allowtransparency="true"  style="width:400px;height:240px"></iframe>""" % (app_globals.janrain_signin_url+query_params,lang)
    )

def shorten_url(url):
    return re.sub("http://[^/]+", "", url)

def shorten_module(mod):
    return re.sub("civicboom/(.*).py", "\\1", mod).replace("/", ".")

def link_to_objects(text):
    """
    Scan a string for "blah blah Content #42 blah blah" and replace
    "Content #42" with a link to the object editor
    """
    output = HTML.literal()
    prev_word = None
    for word in text.split():
        if prev_word:
            id_match = re.match("#(\d+)", word)
            if id_match:
                output = output + HTML.a(
                        prev_word+" #"+id_match.group(1),
                        href="/admin/"+prev_word+"/models/"+id_match.group(1)+"/edit")
                word = None
            else:
                output = output + HTML.literal(prev_word)
            output = output + HTML.literal(" ")
        prev_word = word
    if prev_word:
        output = output + HTML.literal(prev_word)
    return output

def wh_public(filename):
    return "http://"+config["s3_bucket_name"]+".s3.amazonaws.com/public/"+filename
    # we are always using s3
    #if config["warehouse"] == "s3":
    #    return "http://"+config["s3_bucket_name"]+".s3.amazonaws.com/public/"+filename
    #else:
    #    return "/"+filename

def url_from_widget(*args, **kargs):
    if hasattr(app_globals,'widget_variables'):
        for var in app_globals.widget_variables:    
            if var in request.params:
                kargs[var] = request.params[var]
            #if hasattr(c,var) and getattr(c,var) != None and var not in kargs:
            #    kargs[var] = getattr(c,var)
    return url(*args,**kargs)

def truncate(text, length=100, indicator='...', whole_word=True):
    # FIXME: stub, see bug #49
    return text[0:length]

def objs_to_linked_formatted_dict(**kargs):
    """
    Takes a dict of string:string that correspond to python tmpl_context global e.g:
      'member':'creator_reporter' would refer to c.creator_reporter
      'member': member_obj_ref 
    Then, See's if the object has a '__link___' attribute to generate a HTML <a> tag for this object
    """
    def gen_link(o):
        # AllanC - code inspired from Shish's Message link framework in lib/communication/messages.py
        if hasattr(o, "__link__"):
            return HTML.a(unicode(o), href=o.__link__())
        else:
            return HTML.span(unicode(o)) # the span here is for security, it does HTML escaping
    links = {}
    for key in kargs:
        val = kargs[key]
        if isinstance(val, basestring) and hasattr(c, val): # if val is text then check to see if it is a key in teml_context
            val = c[val]
        links[key] = gen_link(val)
    return links
