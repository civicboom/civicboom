"""
"""
# Base controller imports
from civicboom.lib.base                import BaseController, render, c, redirect, url, request, abort, _, app_globals, flash_message, redirect_to_referer, action_redirector
from civicboom.lib.authentication      import authorize, is_valid_user

from civicboom.lib.database.etag_manager import gen_cache_key
from civicboom.lib.database.get_cached   import get_user, get_content
from civicboom.lib.helpers import url_from_widget

import re
from urllib import quote_plus


# Logging setup
import logging
log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")

template_expire = 1800 # 30 min in seconds

app_globals.widget_variables = ['widget_theame', 'widget_title', 'widget_username', 'widget_width', 'widget_height']
widget_default_reporter_name = "widget demo"

prefix = '/widget/'

def setup_widget_env():
    def get_widget_varibles_from_env():
        def get_env_from_referer(var_name):
            try:
                # AllanC - when the Authkit intercepts an action to authenticate the current URL does not have the widget details to display properly
                #          in this case we may need to get the widget details from the referer
                #          this regex seeks a variable in the http_referer
                #          as a botch the variables are delimted by '&' and I have appended one to the end [because /b was not working in the regex :( ]
                return re.search(var_name+r'=(.+?)&',unquote_plus(c.http_referer)+'&').group(1).encode('utf-8')
            except:
                return None
        for var in app_globals.widget_variables:
            if var in request.params:
                setattr(c, var, request.params[var].encode('utf-8')) #Get variable from current request (override refferer if exist)
            else:
                setattr(c, var, get_env_from_referer(var)) # Get varible from referer
    def construct_widget_query_string():
        query_string = "?"
        for var in app_globals.widget_variables:
            if getattr(c,var) != None:
                query_string += var+'='+quote_plus(getattr(c,var))+'&'
        return query_string
    get_widget_varibles_from_env()
    c.widget_query_string = construct_widget_query_string() #construct a new query string based on current widget global variables (this is needed for intercepted signin pages to pass the variables on see widget_signin.mako FORM_ACTION)
    c.widget_owner        = get_user(c.widget_username)


class WidgetController(BaseController):

    def __before__(self, action, **params):
        BaseController.__before__(self)
        setup_widget_env() #this sets c.widget_owner and takes c.widget_ variables from url
        if not c.widget_owner:
            abort(400)
    
    #-----------------------------------------------------------------------------
    # Widget Pages
    #-----------------------------------------------------------------------------
    
    # Signin or sign up
    @authorize(is_valid_user)
    def signin(self):
        return redirect(url_from_widget(controller='widget', action='main'))
  
    # Main assignments list
    def main(self):
        cache_key = gen_cache_key(member=c.widget_owner.id, member_assignments_active=c.widget_owner.id)
        c.assignments = c.widget_owner.content_assignments #get_assignments_active(c.widget_owner)
        return render(prefix + 'widget_assignments.mako', cache_key=cache_key, cache_expire=template_expire)
    
    # Single assignment display
    def assignment(self, id):
        cache_key = gen_cache_key(member=c.widget_owner.id, content=id)
        c.absolute_links           = True
        c.links_open_in_new_window = True
        c.assignment = get_content(id)
        return render(prefix + 'widget_assignment.mako', cache_key=cache_key, cache_expire=template_expire)


    #-----------------------------------------------------------------------------
    # Static Pages
    #-----------------------------------------------------------------------------

    # About page
    def about(self):
        cache_key = gen_cache_key(member=c.widget_owner.id)
        return render(prefix + 'widget_about.mako', cache_key=cache_key, cache_expire=template_expire)
  
    # Static get widget page
    def get_widget(self):
        cache_key = gen_cache_key(member=c.widget_owner.id)
        c.absolute_links           = True
        c.links_open_in_new_window = True
        return render(prefix + 'widget_get_widget.mako', cache_key=cache_key, cache_expire=template_expire)
    
    # Static get mobile page
    def get_mobile(self):
        cache_key = gen_cache_key(member=c.widget_owner.id)
        c.absolute_links           = True
        c.links_open_in_new_window = True
        return render(prefix + 'widget_get_mobile.mako', cache_key=cache_key, cache_expire=template_expire)
