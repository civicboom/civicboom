from pylons import tmpl_context as c, config, request
from paste.deploy.converters import asbool


#-------------------------------------------------------------------------------
# Constant - defaults
#-------------------------------------------------------------------------------
#  these dicts are to be cloned


widget_defaults = {}

widget_defaults['basic'] = dict(
    width      = 160 ,
    height     = 200 ,
    title      = 'Get involved'  ,
    base_list  = 'content_and_boomed',
    owner      = '' ,
    color_font       = '000' ,
    color_border     = 'ccc' ,
    color_header     = 'ccc' ,
    color_action_bar = 'ddd' ,
    color_content    = 'eee' ,
    theme            = 'basic',
    show_responses   = False,
    button_respond   = 'Respond with your text, images and video now!'
)

widget_defaults['gradient'] = dict(
    width      = 280 ,
    height     = 180 ,
    title      = 'See the latest requests'  ,
    base_list  = 'assignments_active',
    owner      = '' ,
    theme      = 'gradient',
)


#-------------------------------------------------------------------------------
# Setup Widget Env - from query string
#-------------------------------------------------------------------------------


def setup_widget_env():
    """
    Take QUERY_STRING params and setup widget globals for widget templates
    """
    from civicboom.lib.database.get_cached import get_member as _get_member
    widget_var_prefix = config["setting.widget.var_prefix"]
    #referer = current_referer()
    #if referer:
    #    referer = unquote_plus(referer)+'&'

    def get_widget_varibles_from_env():
        #def get_env_from_referer(var_name):
        #    try:
        #        # AllanC - when the Authkit intercepts an action to authenticate the current URL does not have the widget details to display properly
        #        #          in this case we may need to get the widget details from the referer
        #        #          this regex seeks a variable in the http_referer
        #        #          as a botch the variables are delimted by '&' and I have appended one to the end [because /b was not working in the regex :( ]
        #        return re.search(var_name+r'=(.+?)&',referer).group(1).encode('utf-8')
        #    except:
        #        return None
        for key in [key for key in c.widget.keys() if widget_var_prefix+key in request.params]:  #app_globals.widget_variables:
            value = request.params[widget_var_prefix+key]#.encode('utf-8')
            if isinstance(c.widget[key], bool): # keep widget bools as bools
                try:
                    c.widget[key] = asbool(value)
                except:
                    pass
            elif isinstance(c.widget[key], int): # keep widget int's as ints
                try:
                    c.widget[key] = int(value)
                except:
                    pass
            else:
                c.widget[key] = value
                #setattr(c, var, request.params[var].encode('utf-8')) #Get variable from current request (override refferer if exist)
            #elif referer:
            #    setattr(c, var, get_env_from_referer(var)) # Get varible from referer
    get_widget_varibles_from_env()
    if c.widget['owner']:
        owner = _get_member(c.widget['owner'])
        if owner:
            c.widget['owner'] = owner.to_dict(include_fields='push_assignment')
