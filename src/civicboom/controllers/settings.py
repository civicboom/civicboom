"""
REST Settings controler

Settings are broken into named groups
These groups of settings can be view/editied using standard REST calls
"""
from civicboom.lib.base import *
import hashlib
import copy

import formencode
from civicboom.lib.form_validators.validator_factory import build_schema
from civicboom.lib.form_validators.registration      import UniqueEmailValidator
from formencode import validators

log = logging.getLogger(__name__)
user_log = logging.getLogger("user")



#Define settings groups, default values and display text
settings_units = dict(
    general=[
        dict(name='name'       , description=_('Display name' ), value=''),
        #{name:'location'   , description:_('Home location'), value:''},
        dict(name='description', description=_('Description'  ), value=''),
        dict(name='home_page'  , description=_('Home page'    ), value=''),
    ],
    email=[
        dict(name='email'      , description=_('Email Address'), value=''),
    ],
    password=[
        #dict(name='password'   , description=_('Password'), value=''),
    ],
    aggregation=[
        dict(name='twitter_username'       , value='', description=_('Twitter username')    ),
        dict(name='twitter_auth_key'       , value='', description=_('Twitter authkey' )    ),
        dict(name='broadcast_instant_news' , value='', description=_('Twitter instant news'), type='boolean'),
        dict(name='broadcast_content_posts', value='', description=_('Twitter content' )    , type='boolean'),
    ],
    avatar=[
        dict(name='avatar'       , description=_('Avatar' ), value='', info='leave blank to use a gravatar'),
    ],
    location=[
        dict(name='location'     , description=_('Home Location' ), value='', info='type in your town name or select a locaiton from the map'),
    ],
    message_routes=[
    ],
)


#Settings validators (for dynamic scema construction)
#  these are kept separte from the group definitions because the group defenitions dict is sent to clients, we do not want to contaminate that dict
import civicboom.lib.form_validators
settings_validators = dict(
    name        = formencode.validators.UnicodeString(),
    description = formencode.validators.UnicodeString(),
    home_page   = formencode.validators.URL(),
    
    email       = civicboom.lib.form_validators.registration.UniqueEmailValidator(),
    
    #password
    
    twitter_username        = formencode.validators.UnicodeString(),
    broadcast_instant_news  = formencode.validators.StringBool(),
    broadcast_content_posts = formencode.validators.StringBool(),
    
    avatar = formencode.validators.URL(),
    
    #location =
)
    
    

class SettingsController(BaseController):
    """
    REST controller for Settings
    
    http://wiki.pylonshq.com/display/pylonscookbook/How+map.resource+enables+controllers+as+services
    
    needs in config/routing.py -> map.resource('setting', 'settings')
    """
    
    def index(self):
        """GET /: All items in the collection."""
        return self.show(None)
    
    def create(self):
        """POST /: Create a new item."""
        response.status = 201 # 201 = Success Created
        return action_error(msg='operation not supported')
    
    def new(self):
        """GET /new: Form to create a new item."""
        response.status = 201 # 201 = Success Created
        return action_error(msg='operation not supported')
    
    @authorize(is_valid_user)
    @auto_format_output()
    def update(self, id):
        """
        PUT /id: Update an existing item.
        
        - Creates a custom validator schema for the inputed data that has changed from the db
        - Validates the request overlaying errors if generated
        - Saves update
        - Returns written object
        """
        edit_action = self.edit(id, format='python')
        settings    = edit_action['data']
        user        = c.logged_in_user
        
        def settings_list():
            """a function to allow iterating over all settings as if they were a single list"""
            for group in settings.keys():
                for setting in settings[group]:
                    yield setting        
        
        # Setup custom schema for this update
        validators = {}
        for validate_fieldname in [setting['name'] for setting in settings_list() if setting['name'] in settings_validators and setting['value'] != request.params[setting['name']]]:
            print "adding validator for: %s" % validate_fieldname
            validators[validate_fieldname] = settings_validators[validate_fieldname]
        
        # Form validation
        try: 
            schema = build_schema(**validators)             # Build a dynamic validation scema based on these required fields and validate the form
            form   = schema.to_python(dict(request.params)) # Validate
        except formencode.Invalid, error:
            # Form has failed validation
            form        = error.value
            form_errors = error.error_dict or {}
            
            # Set error property for each failed property
            for setting in settings_list():
                setting_fieldname = setting['name']                            # For each setting
                if setting_fieldname in form:                                  #   If in form 
                    setting['value'] = form[setting_fieldname]                 #     populate value with form data
                if setting_fieldname in form_errors:                           #   If error
                    e = form_errors[setting_fieldname]                         #     
                    del form_errors[setting_fieldname]                         #     delete error object (so we can see if any are outstanding/missing at the end)
                    if hasattr(e,'msg'): e = e.msg                             #     append error
                    setting['error'] = e                                       #
            
            # Report any missing fields (anything that is left in error.error_dict)
            if len(form_errors) > 0:
                settings['missing'] = []
                for missing_fieldname in form_errors.keys():
                    e = form_errors[missing_fieldname]
                    if hasattr(e,'msg') : e = e.msg
                    settings['missing'].append({'name':missing_fieldname, 'description':missing_fieldname, 'error':e, 'value':''})
            
            # Set error status
            edit_action['status']  = 'error'
            edit_action['message'] = error.msg #_('failed validation') #
            #response.status = 400 # 400 = Bad request # is this the correct HTTP code for this event? # This BREAKS html layout bigtime!
            return edit_action
        
        # Form has passed validation - continue to save/commit changes
        for setting in settings_list():
            setting_fieldname = setting['name']
            if setting_fieldname in form:                                    # For each setting
                #if setting['value'] != form[setting_fieldname]:              #   If value has changed # Unneeded as the form vaidators are built of feilds that have changed
                    user.config[setting_fieldname] = form[setting_fieldname] #     change the actual user object
                    setting['value'] = form[setting_fieldname]               #     update the return dict
        Session.commit()                                                     # save changes to database
        
        return edit_action

    
    def delete(self, id):
        """
        DELETE /id: Delete an existing item.
        """
        # h.form(h.url_for('message', id=ID), method='delete')
        # Rather than delete the setting this simple blanks the required fields - or removes the config dict entry
        response.status = 204 # 204 = Success No Content
        return action_error(msg='implement')

    def show(self, id):
        """GET /id: Show a specific item."""
        return self.edit(id)

    @authorize(is_valid_user)
    @auto_format_output()
    def edit(self, id, format='html'):
        """GET /id;edit: Form to edit an existing item."""
        
        # Generate base settings dictonary for ALL settings or SINGLE ID provided
        if id=="index" or id=="None": id=None
        if not id: settings =     copy.deepcopy(settings_units)
        else     : settings = {id:copy.deepcopy(settings_units[id])}
        
        user = c.logged_in_user
        c.viewing_user = c.logged_in_user # HACK - please remove when templates are refactored
        
        # Populate settings dictionary for this user
        for setting_group in settings.keys():
            for setting in settings[setting_group]:
                setting['value'] = user.config[setting['name']]
        
        return dict(data=settings, template="settings/settings")






    #---------------------------------------------------------------------------
    # Old Settings Reference
    #---------------------------------------------------------------------------

    @authorize(is_valid_user)
    def general(self, id=None):
        c.viewing_user = c.logged_in_user
        return render("web/settings/general.mako")

    @https()
    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def save_general(self, id=None, format="html"):
        c.viewing_user = c.logged_in_user
        u_config = c.viewing_user.config
        current_keys = u_config.keys()

        # handle special cases
        if "move_to_gravatar" in request.POST.keys():
            if request.POST["move_to_gravatar"] == "on":
                c.viewing_user.avatar = None
            del request.POST["move_to_gravatar"]

        # FIXME: helper function for "is valid display name", see feature #54
        if "name" in request.POST.keys():
            if len(request.POST["name"]) > 0:
                c.viewing_user.name = request.POST["name"]
            del request.POST["name"]

        # FIXME: check for validity before changing
        if "email" in request.POST.keys():
            if len(request.POST["email"]) > 0:
                c.viewing_user.email = request.POST["email"]
            del request.POST["email"]

        # TODO: figure out stuff for User.logins[].password
        if "current_password" in request.POST.keys():
            hex_curr = hashlib.sha1(request.POST["current_password"]).hexdigest()
            hex_new1 = hashlib.sha1(request.POST["new_password_1"]).hexdigest()
            hex_new2 = hashlib.sha1(request.POST["new_password_2"]).hexdigest()
            if False:
                if hex_curr == c.viewing_user.password:
                    if hex_new1 == hex_new2:
                        c.viewing_user.password = hex_new1
                    else:
                        error = action_error(_("New passwords don't match"))
                else:
                    error = action_error(_("Current password was wrong"))
            del request.POST["current_password"]
            del request.POST["new_password_1"]
            del request.POST["new_password_2"]

        # everything that's left is treated as a config value
        for key in request.POST.keys():
            if request.POST[key] == app_globals.user_defaults.get("settings", key):
                if key in current_keys:
                    del u_config[key]
            else:
                c.viewing_user.config[key] = request.POST[key]

        return action_ok(_("Settings saved"))#+", ".join(request.POST.keys())

    @authorize(is_valid_user)
    def messages(self, id=None):
        c.viewing_user = c.logged_in_user
        return render("web/settings/messages.mako")

    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def save_messages(self, id=None, format="html"):
        c.viewing_user = c.logged_in_user
        from civicboom.lib.communication.messages import generators
        for gen in generators:
            route_name = "route_"+gen[0]
            setting = "".join([
                request.POST.get(gen[0]+"_n", ""),
                request.POST.get(gen[0]+"_e", ""),
                request.POST.get(gen[0]+"_c", ""),
            ])
            if setting == gen[1]:
                if route_name in c.viewing_user.config:
                    del c.viewing_user.config[route_name]
            else:
                c.viewing_user.config[route_name] = setting

        return action_ok(_("Settings saved"))

    @authorize(is_valid_user)
    def location(self, id=None):
        c.viewing_user = c.logged_in_user
        return render("web/settings/location.mako")

    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def save_location(self, id=None, format="html"):
        if "location" in request.POST:
            try:
                (lon, lat) = [float(n) for n in request.POST["location"].split(",")]
            except Exception, e:
                user_log.exception("Unable to understand location '%s'" % str(request.POST["location"]))
                return action_error(_("Unable to understand location '%s'" % str(request.POST["location"])))
        elif "location_name" in request.POST:
            (lon, lat) = (0, 0) # FIXME: guess_lon_lat_from_name(request.POST["location_name"]), see Feature #47
        else:
            return action_error(_("No position specified"))
        c.viewing_user = c.logged_in_user
        c.viewing_user.location = "SRID=4326;POINT(%d %d)" % (lon, lat)
        Session.commit()

        return action_ok(_("Settings saved"))
        #return "Location saved: %s (%s)" % (
        #    request.params.get("location", "[pos]"),
         #   request.params.get("location_name", "[name]"),
        #)
