"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""

#from webhelpers.html.tags import checkbox, password
from webhelpers.pylonslib.secure_form import authentication_token, secure_form

from pylons import config, app_globals, tmpl_context as c, request
#from pylons.i18n.translation import _
from webhelpers.html import HTML, literal
from webhelpers.text import truncate
from webhelpers.html.tags import end_form
from webhelpers.date import time_ago_in_words

from cbutils.text import strip_html_tags, scan_for_embedable_view_and_autolink
from cbutils.misc import args_to_tuple, make_username, now
from civicboom.lib.web import current_url, url, current_protocol

from civicboom.config.routing import action_single_map

import webhelpers.html.tags as html

#import recaptcha.client.captcha as librecaptcha
from civicboom.lib.services.reCAPTCHA import reCAPTCHA_html
import os
import re
import urllib
import hashlib
import simplejson as json
import copy
import time
import datetime
import logging

user_log = logging.getLogger("user")

# Regex to match absolute urls and allow removing of proto/host/domain name
link_matcher = re.compile(r'\A(http[s]{0,1}://[\w\.\-\_]*)/{0,1}')
# Regex to match any non html id/class safe chars
funky_chars  = re.compile(r'[^\w]+')


def guess_hcard_name(name):
    """
    Looks at a string and attempts to return the best hCard formatted representation

    >>> guess_hcard_name("Unit Testson")
    literal(u"<span class='given-name'>Unit</span> <span class='family-name'>Testson</span>")
    >>> guess_hcard_name("Mr. U. Test")
    literal(u"<span class='honorific-prefix'>Mr.</span> <span class='given-name'>U.</span> <span class='family-name'>Test</span>")
    >>> guess_hcard_name("The Waffle Eater")
    literal(u"<span class='given-name'>The Waffle Eater</span>")
    """
    parts = name.split()
    if len(parts) == 2:
        return (
            literal("<span class='given-name'>")+
            parts[0]+
            literal("</span> <span class='family-name'>")+
            parts[1]+
            literal("</span>")
        )
    elif len(parts) == 3 and parts[0].lower().strip(".") in ["mr", "mrs", "sir", "ms", "lord"]:
        return (
            literal("<span class='honorific-prefix'>")+
            parts[0]+
            literal("</span> <span class='given-name'>")+
            parts[1]+
            literal("</span> <span class='family-name'>")+
            parts[2]+
            literal("</span>")
        )
    else:
        return (
            literal("<span class='given-name'>")+
            name+
            literal("</span>")
        )


def get_captcha(lang='en', theme='red'):
    """
    Generate reCAPTCHA html
    """
    return literal(reCAPTCHA_html(lang, theme))
    # Old use of pythonrecaptcha
    # (currently the python-recaptcha API does not support the lang or theme option, but these are fields in the html, maybe we need a modifyed version, see the django example for more info)
    # http://k0001.wordpress.com/2007/11/15/using-recaptcha-with-python-and-django/
    #return literal(librecaptcha.displayhtml(config['api_key.reCAPTCHA.public'])) #, lang="es", theme='white'


def get_janrain(lang='en', theme='', return_url=None, **kargs):
    """
    Generate Janrain IFRAME component
    """
    if not return_url:
        return_url = urllib.quote_plus(url('current', host=c.host, protocol='https')) #controller='account', action='signin',
    query_params = ""
    for karg in kargs:
        query_params += karg+"="+str(kargs[karg])
    if query_params != "":
        query_params = urllib.quote_plus("?"+query_params)
    scheme = current_protocol()
    return literal(
        """<iframe src="%s://civicboom.rpxnow.com/openid/embed?token_url=%s&language_preference=%s"  scrolling="no"  frameBorder="no"  allowtransparency="true"  style="width:400px;height:240px"></iframe>""" % (scheme, return_url+query_params, lang)
    )


def shorten_url(url):
    """
    Return a URL which is shorter but still useful, for
    being displayed in logs

    >>> shorten_url("https://www.civicboom.com/i/like/bacon")
    '/i/like/bacon'

    doesn't affect urls that are already short:

    >>> shorten_url("/waffo/waffo")
    '/waffo/waffo'

    also set an absolute length limit
    >>> len(shorten_url("a"*1000))
    100
    """
    return re.sub("https?://[^/]+", "", url)[:100]


def shorten_module(mod):
    """
    Return a module name that is shorter but still useful, for
    being displayed in logs

    >>> shorten_module("civicboom/lib/helpers.py")
    'lib.helpers'
    """
    return re.sub("civicboom/(.*).py", "\\1", mod).replace("/", ".")


def nicen_url(url):
    """
    Make a URL nicer for human readers

    >>> nicen_url("http://www.shishnet.org/~shish")
    'shishnet.org/~shish'
    >>> nicen_url("http://www.shishnet.org/")
    'shishnet.org'
    >>> nicen_url("http://www.shishnet.org")
    'shishnet.org'
    >>> nicen_url("http://shishnet.org")
    'shishnet.org'
    >>> nicen_url("shishnet.org")
    'shishnet.org'
    """
    return re.sub("^(http://|)?(www\.|)?(.*?)/?$", "\\3", url)


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


def wh_url(folder, filename):
    # see /docs/cdn.rst for an explanation of our CDN setup
    proto = current_protocol()+"://"
    if folder == "public":
        if app_globals.version:
            # in production, serve from a domain without cookies, with package version as cache breaker
            cdn_url = config['cdn.url']
            if proto == "https://": # rackspace CDN uses different hostnames for SSL and regular
                cdn_url = re.sub("\.r\d\d\.", ".ssl.", cdn_url)
            return proto+cdn_url+"/"+app_globals.version+"/"+filename
        else:  # pragma: no cover - only the production setup is tested
            # in development, serve locally, with update time as cache breaker
            path = os.path.join("civicboom", "public", filename)
            ut = str(int(os.stat(path).st_mtime))
            return proto+request.environ.get("HTTP_HOST")+"/"+filename+"?ut="+ut
    # all other folders (media, avatars) are served from our beefy-but-slow-to
    # update warehouse (currently amazon S3)
    else:
        if config['warehouse.type'] == "local":
            return proto+request.environ.get("HTTP_HOST")+config["warehouse.url"]+"/"+folder+"/"+filename
        else:
            return proto+config["warehouse.url"]+"/"+folder+"/"+filename


def uniqueish_id(*args):
    """
    A unique ID for use in HTML, for example giving two minimap()s different IDs

    For a better unique ID, use python's UUID/GUID libraries
    """
    largs = list(args)
    largs.append(str(int(time.time() * 1e9)))
    return "_".join([str(a) for a in largs])


def objs_to_linked_formatted_dict(**kargs):
    """
    Takes a dict of string:string that correspond to python tmpl_context global e.g:
      'member':'creator_member' would refer to c.creator_member
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
    for key, val in kargs.iteritems():
        if isinstance(val, basestring) and hasattr(c, val): # if val is text then check to see if it is a key in teml_context
            val = c[val]
        links[key] = gen_link(val)
    return links


# AllanC - not happy with this ... see register template for example ...
# htmlfill does not support HTML5 - so I created a cusom way of getting invalid data into the template
# in the future when htmlfill is fixed then we can swich back to it
def get_data_value(field_name, sub_dict_name=None, default_value=''):
    if sub_dict_name in c.result['data'] and field_name in c.result['data'][sub_dict_name]:
        return c.result['data'][sub_dict_name][field_name]
    else:
        return default_value


# AllanC - TODO: HACK ALERT!!!
# I wanted a helper to create icons in a standard way that would degrade without a CSS style.
#  e.g. when no style sheet is used (or a screen reader) it will have the text "approved" rather than just the icon
# I wanted the text description to be on the hover "title" and in a hidden-degradable <span>
# Problem!!!!
# cant have it8n in helpers ... ****!
# so I created a dumby _ method ... this needs considering
# Could be moved to common.mako template?
#def _(s):
#    return s
icon_type_descriptions = {
#    'approved'    : _('approved by parent owner') ,
#    'seen'        : _('parent owner has seen this content') ,
#    'edit_lock'   : _('edit lock') ,
#    'dissacociate': _('parent owner has disassociated this content') ,
#    'group'       : _('group') ,
#    'account_plus': _('plus account') ,
#    'account_corp': _('corporate account') ,
}


def icon(icon_type, description=None, class_=''):
    if not description and icon_type in icon_type_descriptions:
        description = icon_type_descriptions[icon_type]
    return HTML.div(HTML.span(description), class_=class_+" icon16 i_"+icon_type, title=description)


#-------------------------------------------------------------------------------
# Date Management
#-------------------------------------------------------------------------------

def api_datestr_to_datetime(date_str):
    if not date_str:
        return None
    try:
        return datetime.datetime.strptime(date_str[0:19], "%Y-%m-%d %H:%M:%S")
    except:
        return datetime.datetime.strptime(date_str[0:10], "%Y-%m-%d")


def date_to_rss(date):
    """
    Turns an ISO date (as used by our API) into an RSS one

    >>> date_to_rss('2010-05-21 16:30:10')
    'Fri, 21 May 2010 16:30:10 +0000'
    """
    if isinstance(date, basestring):
        date = api_datestr_to_datetime(date)
    return date.strftime("%a, %d %b %Y %H:%M:%S +0000")

def time_ago(from_time):
    if not from_time:
        return None
    if isinstance(from_time, basestring):
        from_time = api_datestr_to_datetime(from_time)
    time_ago = time_ago_in_words(from_time, granularity='minute', round=True)
    match = re.match("^(less than ){0,1}\d+ [a-z]+", time_ago)
    if match:
        part = match.group(0)
        part = part.replace("minute", "min")
        part = part.replace("second", "sec")
        return part
    else:
        user_log.error("Failed to shorten time_ago:"+time_ago)
        return time_ago


#-------------------------------------------------------------------------------
# Standard and JSON URL generation
#-------------------------------------------------------------------------------

def url_pair(*args, **kwargs):
    # Defensive copying
    #args   = copy.copy(args)
    #kwargs = copy.copy(kwargs)
    gen_format = kwargs.pop('gen_format')

    href             = url(*args, **kwargs)
    kwargs['format'] = gen_format
    href_formatted   = url(*args, **kwargs)
    
    return (href, href_formatted)


## AllanC - TODO - need to specify frag size as an optional arg
def frag_link(value, title='', class_='', href_tuple=([], {})): #*args, **kwargs
    href, href_frag = url_pair(gen_format='frag', *href_tuple[0], **href_tuple[1]) # generate standard and frag URL's
    return HTML.a(
        value ,
        href    = href ,
        class_  = 'link_new_frag ' + class_ ,
        title   = title if title else value,
        ##onClick ="cb_frag($(this), '%s'); return false;" % href_frag ,
        **{'data-frag' : href_frag}
    )


#-------------------------------------------------------------------------------
# Secure Form
#-------------------------------------------------------------------------------
# If the form is given it's first href arg as a tuple then we can create the URL from the tuple for both JSON and Standard URL's
def form(*args, **kwargs):
    href_tuple = None
    
    json_form_complete_actions = kwargs.pop('json_form_complete_actions', '')
    pre_onsubmit               = kwargs.pop('pre_onsubmit', '')
    
    # GregM: Although secure_link does this we call form directly
    # Actually, FIXME: Insert ajaxy stuff here, then both are covered by magic
    data_dict                  = kwargs.pop('data', {})
    for key, value in data_dict.items():
        kwargs['data-%s' % key.replace('_','-')] = value
        
    if not kwargs.get('data-json-complete'):
        kwargs['data-json-complete'] = "[ ['update'] ]"
        pass
    
    # Look for href as a tuple in the form (args,kwargs)
    if len(args)>0 and isinstance(args[0], tuple):
        href_tuple = args[0]
    if isinstance(kwargs.get('href'), tuple):
        href_tuple = kwargs['href']

    # if href=tuple then generate 2 URL's from tuple 1.) Standard  2.) JSON
    if href_tuple:
        href, href_json = url_pair(gen_format='json', *href_tuple[0], **href_tuple[1]) # generate standard and JSON URL's
        kwargs['data-json'] = href_json

    kwargs['novalidate'] = 'novalidate'

    # put the href generated url back in the right place
    if len(args)>0 and isinstance(args[0], tuple):
        args = list(args)
        args[0] = href
    if isinstance(kwargs.get('href'), tuple):
        kwargs['href'] = href
    
    return secure_form(*args, **kwargs)


#-------------------------------------------------------------------------------
# Secure Link - Form Submit or Styled link (for JS browsers)
#-------------------------------------------------------------------------------

def secure_link(href, value='Submit', value_formatted=None, title=None, method='POST', form_data=None, link_data=None, link_class='', parent_id=None, force_profile=False):
#def secure_link(href, value='Submit', value_formatted=None, css_class='', title=None, rel=None, confirm_text=None, method='POST', json_form_complete_actions='', modal_params=None, data={}):
    """
    Create two things:
      - A visible HTML form which POSTs some data along with an auth token
      - An invisible pretty-looking plain-text link which calls form.submit()
    Then use javascript to hide the form and show the pretty link
    
    @param href      - can be supplied as a string or a tuple in the format (args, kwargs), this tuple will then be used to automatically create href_json
    @param href_json - an optional JSON url to post to can be provided, this will then activate an AJAX call, this is normally set automatically by providing a tuple for href (see above)
    @param javascript_json_complete_actions - a string of javascript that is activated on a successful AJAX call. Normally used to refresh parts of the page that have been updated from the successful AJAX call.
    """
    if not value_formatted:
        value_formatted = value
    else:
        value_formatted = literal(value_formatted)
    if not form_data:
        form_data = {}
    if not link_data:
        link_data = {}
    
    # Setup Get string href ----
    # the href could be passed a a tuple of (args,kwargs) for form() to create a JSON version to submit to
    # we need a text compatable href reguardless
    href_original = copy.deepcopy(href)
    if isinstance(href, tuple):
        args = href[0]
        kwargs = href[1]
        form_href = url(*args, **kwargs)
        kwargs['format'] = 'json'
        data_json = url(*args, **kwargs)
        #form_data = dict([(key.replace('_', '-' if '_' in key else key, form_data[key])) for key in form_data.keys()])
        
        # GregM: Work out what to do is json_complete has not been defined manually, this could and will fail on odd cercumstances
        if not form_data.get('json_complete'):
            args = list(args)
            args[0] = action_single_map.get(args[0], args[0])
            if kwargs.get('format'):
                del kwargs['format']
            kwargs['action'] = 'show'
            action1 = ['remove'] if method == 'DELETE' else ['update']
            action2 = ['update', [url(*args, **kwargs)], None, None]
            if parent_id:
                kwargs['id'] = parent_id
                action2[1].append(url(*args, **kwargs))
            if args[0] == 'member' or force_profile:
                action2[1].append('/profile')
            form_data['json_complete'] = json.dumps([action1, action2]).replace('"',"'")
    # Do magic to convert all form & link _data to kwargs
    form_data = dict([ ('data-%s' % k.replace('_','-'), v if isinstance(v, basestring) else json.dumps(v)) for (k,v) in form_data.items() ])
    link_data = dict([ ('data-%s' % k.replace('_','-'), v if isinstance(v, basestring) else json.dumps(v)) for (k,v) in link_data.items() ])
            
        

    # Keep track of number of secure links created so they can all have unique hash's
    #hhash = hashlib.md5(uniqueish_id(href, value, vals)).hexdigest()[0:6]
    # GregM: Semi-unique ids required for selenium, these will be unique to every action (multiple of same action can exist)
#    hhash = re.sub(funky_chars, '_', re.sub(link_matcher, '', href)) + '_' + method

    # Create Form --------
    #AllanC: without the name attribute here the AJAX/JSON does not function, WTF! took me ages to track down :( NOTE: if the name="submit" jQuery wont submit! a known problem!?
    hf = form(href_original, method=method, class_='hide_if_js', **form_data) + \
            HTML.input(type="submit", value=value, name=value) + \
        end_form() #,

    hl = HTML.a(
        value_formatted ,
        href    = '#',
        class_  = link_class + ' hide_if_nojs link_secure', # GregM: secure_show means js will show element and remove class (to stop dup processing of same element)
        title   = title,
        **link_data
    )
    
    return HTML.span(hf+hl, class_="secure_link") #+json_submit_script


# This will create an html a link with our popup.
#def confirmed_link (title, icon='', **kwargs):
#    modal_params = kwargs.get('modal_params', {})
#    
#    buttons = [
#        {
#            'title': modal_params.get('buttons', {}).get('yes', 'Yes'),
#            'href': kwargs.get('href', ''),
#            'onClick': "$.modal.close();",
#        },
#        {
#            'title': modal_params.get('buttons', {}).get('no', 'No'),
#            'href': '#',
#            'onClick': "$.modal.close(); return false;",
#        },
#    ]
#    modal_params['buttons'] = buttons
#    
#    kwargs['onClick'] = '$(this).parents(\'.confirmed_link\').find(\'.popup-modal\').modal({appendTo: $(this).parents(\'.confirmed_link\')}); return false'
#    
#    if icon:
#        icon = HTML.span(class_="icon16 i_"+icon)
#    
#    confirm = modal_dialog_confirm (**modal_params)
#    link = HTML.a(icon+title, **kwargs)
#    
#    return HTML.span(link+confirm, class_='confirmed_link')

# GregM: At last! Gone!
#def modal_dialog_confirm (title, message, icon=None, icon_image=None, width = None, buttons = [{'href':'#', 'onClick':'', 'title':'Yes' }, {'href':'#', 'onClick':'$.modal.close(); return false;', 'title':'No'}] ):
#    content = ''
#    if icon:
#        content = content + HTML.div(HTML.span('', class_="icon32 ic_" + icon), class_="popup-icon")
#    elif icon_image:
#        content = content + HTML.div(HTML.image(src=icon_image), class_="popup-icon")
#    content = content + HTML.div(title or '', class_="popup-title")
#    
#    if message:
#        content = content + HTML.div(message, class_="popup-message")
#    
#    popup_actions_content = None
#    for button in buttons:
#        if not button.get('class_'):
#            button['class_'] = ''
#        classes = button['class_'].split(' ')
#        classes.extend(['button', 'fl'])
#        button['class_'] = ' '.join(classes)
#        button_element = HTML.a(
#            button.get('title', ''),
#            **button
#        )
#        if not popup_actions_content:
#            popup_actions_content = button_element
#        else:
#            popup_actions_content += button_element
#    
#    content = content + HTML.div(popup_actions_content+HTML.div(class_="cb"), class_="popup-actions")
#    
#    content = HTML.div(content, class_="information")
#    
#    content = HTML.div(content, class_="popup_content")
#    
#    content = HTML.div(content + HTML.div(class_='cb'), class_="popup-modal", style="width: %s;" % (width or '35em'))
#    
#    return HTML.div(content, class_="popup_hidden")


#-------------------------------------------------------------------------------
# Frag DIV's and Links - for Static and AJAX compatability
#-------------------------------------------------------------------------------

# GregM: Lets start ripping unused stuff out, rework is underway; commented for now to check dependancies!

# AllanC - These are currently not used on the site
#          they were to enable the static and dynamic generation of a page
#          The fragment system currently duplicates lots of info for both static and dynamic,
#          in future we could refine the system below to maybe tidy up the fragment system
#
#          NOTE: setSingleCSSClass is depricated and not implemtned anymore, the method below will need to be fixed

#def parse_url_args_kwargs(url_args_kwargs):
#    url_args = []
#    url_kwargs = {}
#    if isinstance(url_args_kwargs, dict):
#        url_kwargs = url_args_kwargs
#    elif isinstance(url_args_kwargs, list):
#        url_args = url_args_kwargs
#    elif isinstance(url_args_kwargs, tuple):
#        url_args = url_args_kwargs[0]
#        url_kwargs = url_args_kwargs[1]
#    return (url_args, url_kwargs)

#def link_secure(url_args_kwargs, value='Submit', value_formatted=None, vals=[], css_class='', title=None, rel=None, confirm_text=None, method='POST', json_form_complete_actions='', modal_params=None):
#    url_args ,url_kwargs = parse_url_args_kwargs(url_args_kwargs)
#    if not value_formatted:
#        value_formatted = value
#    href = url(*url_args, **url_kwargs)
#    
#    html = HTML.form(href_original, id="form_"+hhash, method=method, json_form_complete_actions=json_form_complete_actions)
#    html = HTML.input(type='submit', value=value, name=value)
#    html = HTML.form(html, )
#    
#    html = HTML.span()
#    
#    pass

#def link_frag(url_args_kwargs, value, title='', css_class=''):
#    """
#    Creates a link with the new-style boom.frags.events class
#    """
#    url_args ,url_kwargs = parse_url_args_kwargs(url_args_kwargs)
#        
#    href = url(*url_args, **url_kwargs)
#    url_args_kwargs['format'] = 'frag'
#    if url_args_kwargs.get('title'):
#        del url_args_kwargs['title']
#    return HTML.a(
#        literal(value),
#        href = href,
#        class_ = 'link_new_frag ' + css_class,
#        title = title,
#        **{'data-frag' : url(*url_args, **url_kwargs)}
#        )

#def frag_link__(id, frag_url, value, title='', css_class=''):
#    """
#    Populate an id destination with a fragments source using AJAX
#    If AJAX not avalable then provide a static URL that will populate the fragments
#    """
#    
#    # Re-create query sting dictionary with the new frag_url set
#    # This is used in static URL's to view the existing page with the new fragment
#    url_kwargs = {}
#    url_kwargs.update(request.GET)
#    url_kwargs[id]                  = frag_url
#    url_kwargs['selected_fragment_link'] = id
#
#    # Add selected class if this element is selected
#    if request.GET.get('selected_fragment_link')==id:
#        css_class += " selected_fragment_link"
#    
#    # As the link has an onClick event the link is never followed if javascript is enabled
#    # If javascript is disabled the link functionas as normal
#    static_link = HTML.a(
#        value ,
#        href    = url('current', **url_kwargs) ,
#        class_  = css_class ,
#        title   = title ,
#        onClick = literal("setSingleCSSClass(this,'selected_fragment_link'); $('#%(id)s').html('<img src=\\\'/images/media_placeholder.gif\\\'>'); $('#%(id)s').load('%(url)s');  return false;" % {'id':id, 'url': frag_url}) ,
#    )
#    
#    return static_link #HTML.span(static_link, class_="frag_link")
#
#
#def frag_div__(id, default_frag_url=None, class_=None):
#    """
#    Create an HTML div linked to a fragment
#    Look in request query sting to populate the div with a fragment (if viewed staticly)
#    optional the div's content can automatically be populated with a default fragment source - the default is always overridden with query sting version
#    NOTE: SSI must be setup on the server (im unsure if paster supports it? it seems to work though nginx on my currentl setup - AllanC)
#    """
#    frag_url      = default_frag_url
#    frag_contents = ""
#    if id in request.GET:
#        frag_url = request.GET[id]
#    if frag_url:
#        frag_contents = literal('<!--#include file="%s"-->' % frag_url)
#    return HTML.div(frag_contents, id=id, class_=class_)


#-------------------------------------------------------------------------------
# Civicboom Fragment Object HTML Block
#-------------------------------------------------------------------------------

#def cb_frag_link(*args, **kwargs):
#    # AllanC - hang on double check needed, where is this used? ... surely href is the static link? surely we want to use url_pair under the hood to generate the json version?
#    kwargs['onclick'] = "cb_frag($(this), '%s'); return false;"  % kwargs['href']
#    return HTML.a(*args, **kwargs)



#-------------------------------------------------------------------------------
# Get object from Civicboom URL
#-------------------------------------------------------------------------------
regex_urls = [
    ('content', re.compile(r'(?:.*?)/contents(?:.*?)parent_id=(\d+)')), #OLD - only for responses  - (?:.*?)/contents/new\?(?:.*?)parent_id=(\d+)
    ('content', re.compile(r'(?:.*?)/contents/(\d+)')                ),
    ('member' , re.compile(r'(?:.*?)/members/(.*?)[/&?#\n. "$]')     ),
]


def get_object_from_action_url(action_url=None):
    """
    Creates a tuple to be used with url(*tuple[0], **tuple[1])
    """
    if not action_url:
        action_url = current_url()

    for (object_type, re_url) in regex_urls:
        m = re.match(re_url, action_url)
        if m:
            return ( [object_type], dict(id=m.group(1)) )
    return (None, None)

#-------------------------------------------------------------------------------
# Notification "Links" to "Frag Links"
#-------------------------------------------------------------------------------

regex_content_links = re.compile(r'<a(?:[^<>]*?)href="(?:[^<>]*?)/contents/(.*?)[/&?#\n. "](?:[^<>]*?)>(.*?)</a>') # \1 = content id \2 = text
regex_member_links  = re.compile(r'<a(?:[^<>]*?)href="(?:[^<>]*?)/members/(.*?)[/&?#\n. "](?:[^<>]*?)>(.*?)</a>') # \1 = member id \2 = text


def links_to_frag_links(content):
    """
    Notification messages have content and members linked to as <a href="http://www.civicboom.com/contents/17>THING</a>"
    These would break the fragment flow.
    Identifying these links and replacing them with the correct JS relative links
    """
    
    def replace_content_link(matchobj):
        return """<a href="%(url)s" onclick="cb_frag($(this), '%(url_frag)s'); return false;">%(text)s</a>""" % {\
            'url'     : url('content', id=matchobj.group(1)               ) ,
            'url_frag': url('content', id=matchobj.group(1), format='frag') ,
            'text'    : matchobj.group(2) ,
        }

    def replace_member_link(matchobj):
        return """<a href="%(url)s" onclick="cb_frag($(this), '%(url_frag)s'); return false;">%(text)s</a>""" % {\
            'url'     : url('member', id=matchobj.group(1)               ) ,
            'url_frag': url('member', id=matchobj.group(1), format='frag') ,
            'text'    : matchobj.group(2) ,
        }

    content = re.sub(regex_content_links, replace_content_link, content)
    content = re.sub(regex_member_links , replace_member_link , content)

    return content
