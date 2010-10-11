"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""

#from webhelpers.html.tags import checkbox, password
from webhelpers.pylonslib.secure_form import authentication_token, secure_form as form

from pylons import url, config, app_globals, tmpl_context as c, request
from webhelpers.html import HTML, literal
from webhelpers.text import truncate
from webhelpers.html.tags import end_form

from civicboom.lib.text import scan_for_embedable_view_and_autolink

import webhelpers.html.tags as html

import recaptcha.client.captcha as librecaptcha
import re
import urllib
import hashlib
import json

def get_captcha(lang='en', theme='white'):
    """
    Generate reCAPTCHA html
    (currently the python-recaptcha API does not support the lang or theme option, but these are fields in the html, maybe we need a modifyed version, see the django example for more info)
    http://k0001.wordpress.com/2007/11/15/using-recaptcha-with-python-and-django/
    """
    return literal(librecaptcha.displayhtml(config['api_key.reCAPTCHA.public'])) #, lang="es", theme='white'


def get_janrain(lang='en', theme='', return_url=None, **kargs):
    """
    Generate Janrain IFRAME component
    """
    if not return_url: return_url = urllib.quote_plus(url.current(host=app_globals.site_host, protocol='https')) #controller='account', action='signin',
    query_params = ""
    for karg in kargs:
        query_params += karg+"="+str(kargs[karg])
    if query_params != "":
        query_params = urllib.quote_plus("?"+query_params)
    return literal(
        """<iframe src="http://civicboom.rpxnow.com/openid/embed?token_url=%s&language_preference=%s"  scrolling="no"  frameBorder="no"  allowtransparency="true"  style="width:400px;height:240px"></iframe>""" % (return_url+query_params,lang)
    )

#def get_frag(func, format="frag", *args, **kwargs):
def call_action(func, format="frag", *args, **kwargs):
    """
    Example of use:
      h.call_action(MessagesController().index)
    """
    old_format = c.format
    c.format = format
    try:
        data = func(*args, **kwargs)
    finally:
        c.format = old_format
    return data

def shorten_url(url):
    return re.sub("https?://[^/]+", "", url)

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

#-------------------------------------------------------------------------------
# Secure Link - Form Submit or Styled link (for JS browsers)
#-------------------------------------------------------------------------------

def secure_link(href, value='Submit', vals=[], css_class='', title='', confirm_text=None, method='POST'):
    """
    Create two things:
      - A visible HTML form which POSTs some data along with an auth token
      - An invisible pretty-looking plain-text link which calls form.submit()

    Then use javascript to hide the form and show the pretty link
    """
    hhash = hashlib.md5(str([href, value, vals])).hexdigest()[0:4]

    # form version
    values = ''
    for k, v in vals:
        values = values + HTML.input(type="hidden", name=k, value=v)
    hf = HTML.span(
        form(href, id="form_"+hhash, method=method) +
            values +
            HTML.input(type="submit", value=value) +
        end_form(),
        id='span_'+hhash)

    # link version
    ## Some links could require a user confirmation before continueing, wrap the confirm text in the javascript confirm call
    if confirm_text:
        confirm_text = "confirm('%s')" % confirm_text
    else:
        confirm_text = "true"
    
    hl = HTML.a(
        value,
        id="link_"+hhash,
        style="display: none;",
        href=href,
        class_=css_class,
        title=title,
        onClick="if("+confirm_text+") {$('#form_"+hhash+"').submit();} return false;"
    )

    # form vs link switcher
    hs = HTML.script(literal('$("#span_'+hhash+'").hide(); $("#link_'+hhash+'").show();'))

    return HTML.span(hf+hl+hs, class_="secure_link")


#-------------------------------------------------------------------------------
# Frag DIV's and Links - for Static and AJAX compatability
#-------------------------------------------------------------------------------

def frag_link(id, frag_url, value, title='', css_class=''):
    """
    Populate an id destination with a fragments source using AJAX
    If AJAX not avalable then provide a static URL that will populate the fragments
    """
    
    # Re-create query sting dictionary with the new frag_url set
    # This is used in static URL's to view the existing page with the new fragment
    url_kwargs = {}
    url_kwargs.update(request.GET)
    url_kwargs[id]                  = frag_url
    url_kwargs['selected_fragment_link'] = id

    # Add selected class if this element is selected
    if request.GET.get('selected_fragment_link')==id:
        css_class += " selected_fragment_link"
    
    # As the link has an onClick event the link is never followed if javascript is enabled
    # If javascript is disabled the link functionas as normal
    static_link = HTML.a(
        value ,
        href    = url.current(**url_kwargs) ,
        class_  = css_class ,
        title   = title ,
        onClick = literal("setSingleCSSClass(this,'selected_fragment_link'); document.getElementById('%(id)s').innerHTML='<img src=\\\'/images/media_placeholder.gif\\\'>'; $('#%(id)s').load('%(url)s');  return false;" % {'id':id, 'url': frag_url}) ,
    )
    
    return static_link #HTML.span(static_link, class_="frag_link")

def frag_div(id, default_frag_url=None):
    """
    Create an HTML div linked to a fragment
    Look in request query sting to populate the div with a fragment (if viewed staticly)
    optional the div's content can automatically be populated with a default fragment source - the default is always overridden with query sting version
    NOTE: SSI must be setup on the server (im unsure if paster supports it? it seems to work though nginx on my currentl setup - AllanC)
    """
    frag_url      = default_frag_url
    frag_contents = ""
    if id in request.GET:
        frag_url = request.GET[id]
    if frag_url:
        frag_contents = literal('<!--#include file="%s"-->' % frag_url)
    return HTML.div(frag_contents, id=id)