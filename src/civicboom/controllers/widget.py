"""
Widget Controller

The widget is an HTML iFrame that members can place on there own webpages reflecting Civicboom content
"""
# Base controller imports
from civicboom.lib.base import *

from civicboom.lib.web     import current_referer
from civicboom.lib.helpers import url_from_widget

from civicboom.controllers.contents       import ContentsController
from civicboom.controllers.member_actions import MemberActionsController
content_controller        = ContentsController()
member_actions_controller = MemberActionsController()

import re
from urllib import quote_plus, unquote_plus

# Logging setup
log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")

template_expire = 1800 # 30 min in seconds

widget_default_reporter_name = "widget demo"

prefix = '/widget/'

#-------------------------------------------------------------------------------
# Setup Widget Env - from query string
#-------------------------------------------------------------------------------

def setup_widget_env():
    """
    Take QUERY_STRING params and setup widget globals for widget templates
    """
    referer = current_referer()
    if referer:
        referer = unquote_plus(referer)+'&'
    def get_widget_varibles_from_env():
        def get_env_from_referer(var_name):
            try:
                # AllanC - when the Authkit intercepts an action to authenticate the current URL does not have the widget details to display properly
                #          in this case we may need to get the widget details from the referer
                #          this regex seeks a variable in the http_referer
                #          as a botch the variables are delimted by '&' and I have appended one to the end [because /b was not working in the regex :( ]
                return re.search(var_name+r'=(.+?)&',referer).group(1).encode('utf-8')
            except:
                return None
        for var in app_globals.widget_variables:
            if var in request.params:
                setattr(c, var, request.params[var].encode('utf-8')) #Get variable from current request (override refferer if exist)
            elif referer:
                setattr(c, var, get_env_from_referer(var)) # Get varible from referer
    def construct_widget_query_string():
        query_string = "?"
        for var in app_globals.widget_variables:
            if getattr(c,var) != None:
                query_string += var+'='+quote_plus(getattr(c,var))+'&'
        return query_string
    get_widget_varibles_from_env()
    c.widget_query_string = construct_widget_query_string() #construct a new query string based on current widget global variables (this is needed for intercepted signin pages to pass the variables on see widget_signin.mako FORM_ACTION)
    c.widget_owner        = get_member(c.widget_username)
    # Set defaults from config if not set
    c.widget_theme        = c.widget_theme  or 'light'
    try:
        c.widget_width  = int(c.widget_width ) or 240
        c.widget_height = int(c.widget_height) or 320
    except:
        pass


#-------------------------------------------------------------------------------
# Widget Controller
#-------------------------------------------------------------------------------

class WidgetController(BaseController):

    def __before__(self, action, **params):
        """
        Every widget action must have accompanying widget owner information
        Take this additional information from the query string and init c. variables
        If the required env has not been set send a bad request error
        """
        BaseController.__before__(self)
        setup_widget_env() #this sets c.widget_owner and takes c.widget_ variables from url
        if not c.widget_owner: # a widget must be owned by someone
            abort(400)

    #-----------------------------------------------------------------------------
    # Widget Pages
    #-----------------------------------------------------------------------------
    
    # Signin or sign up
    @auto_format_output       # the auto format is needed to set the c.format variable for the authorize decorator to take effect
    @authorize # authorisze decorator triggers render of signin widget page
    def signin(self):
        return redirect(url_from_widget(controller='widget', action='main'))

    # Main assignments list
    @auto_format_output
    def main(self):
        cache_key = gen_cache_key(member=c.widget_owner.id, member_assignments_active=c.widget_owner.id)
        #c.assignments = c.widget_owner.content_assignments
        c.result = member_actions_controller.content(c.widget_owner.id, list='assignments_active')
        return render(prefix + 'widget_assignments.mako', cache_key=cache_key, cache_expire=template_expire)
    
    # Single assignment display
    @auto_format_output #not really approriate, but needed for the recursive calls
    def assignment(self, id):
        cache_key = gen_cache_key(member=c.widget_owner.id, content=id)
        c.absolute_links           = True
        c.links_open_in_new_window = True
        overlay_status_message(c.result, content_controller.show(id))
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
