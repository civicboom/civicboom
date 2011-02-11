"""
REST Settings controler

Settings are broken into named groups
These groups of settings can be view/editied using standard REST calls

The principle is that each settings has a validator associated with it
Only the form fields that are sent are validated and saved
(this is an issue for realted fields such as password, that creates a bit of a mess, see code below)
"""

from civicboom.lib.base import *
import civicboom.lib.services.warehouse as wh
import hashlib
import copy
import tempfile
import Image

from civicboom.lib.form_validators.validator_factory import build_schema
from civicboom.lib.form_validators.dict_overlay import validate_dict

from civicboom.lib.civicboom_lib import set_password, send_verifiy_email
from civicboom.model.meta import location_to_string

log = logging.getLogger(__name__)
user_log = logging.getLogger("user")


#---------------------------------------------------------------------------
# Setting Units
#---------------------------------------------------------------------------
# Define settings groups, default values and display text

settings_base = {}
def add_setting(name, description, value='', group=None, **kwargs):
    setting = dict(name=name, description=description, value=value, group=group, **kwargs)
    settings_base[setting['name']]=setting
    
add_setting('name'                   , _('Display name' )       , group='general'                     )
add_setting('description'            , _('Description'  )       , group='general'    , type='textarea')
add_setting('website'                , _('Website'      )       , group='general'                     )
add_setting('email'                  , _('Email Address')       , group='contact'                     )
add_setting('password_new'           , _('New password')        , group='password'   , type='password')
add_setting('password_new_confirm'   , _('New password again')  , group='password'   , type='password')
add_setting('password_current'       , _('Current password')    , group='password'   , type='password')
#add_setting('twitter_username'       , _('Twitter username')    , group='aggregation')
#add_setting('twitter_auth_key'       , _('Twitter authkey' )    , group='aggregation')
#add_setting('broadcast_instant_news' , _('Twitter instant news'), group='aggregation', type='boolean')
#add_setting('broadcast_content_posts', _('Twitter content' )    , group='aggregation', type='boolean')
add_setting('avatar'                 , _('Avatar' )             , group='avatar'     , type='file')
add_setting('location_home'          , _('Home Location' )      , group='location'   , type='location', info='type in your town name or select a locaiton from the map')




#---------------------------------------------------------------------------
# Setting Validators (for dynamic scema construction)
#---------------------------------------------------------------------------
#  these are kept separte from the group definitions because the group defenitions dict is sent to clients, we do not want to contaminate that dict

import formencode
import civicboom.lib.form_validators
import civicboom.lib.form_validators.base
import civicboom.lib.form_validators.registration

settings_validators = dict(
    name        = formencode.validators.UnicodeString(),
    description = formencode.validators.UnicodeString(),
    website     = formencode.validators.URL(),
    
    email       = civicboom.lib.form_validators.registration.UniqueEmailValidator(),
    
    password_new         = civicboom.lib.form_validators.base.PasswordValidator(),
    password_new_confirm = civicboom.lib.form_validators.base.PasswordValidator(),
    password_current     = civicboom.lib.form_validators.base.CurrentUserPasswordValidator(),
    
    #twitter_username        = formencode.validators.UnicodeString(),
    #twitter_auth_key        = formencode.validators.UnicodeString(),
    #broadcast_instant_news  = formencode.validators.StringBool(if_missing=False),
    #broadcast_content_posts = formencode.validators.StringBool(if_missing=False),
    
    avatar = formencode.validators.FieldStorageUploadConverter(),
    
    location_home = civicboom.lib.form_validators.base.LocationValidator(),
    location_current = civicboom.lib.form_validators.base.LocationValidator(),
)

    
#---------------------------------------------------------------------------
# REST Controller
#---------------------------------------------------------------------------

class SettingsController(BaseController):
    """
    REST controller for Settings
    
    http://wiki.pylonshq.com/display/pylonscookbook/How+map.resource+enables+controllers+as+services
    
    needs in config/routing.py -> map.resource('setting', 'settings')
    """
    
    #---------------------------------------------------------------------------
    # REST Actions - simple passthrough actions
    #---------------------------------------------------------------------------
    
    def index(self):
        """GET /: All items in the collection."""
        return self.show(None)
    
    @auto_format_output
    def create(self):
        """POST /: Create a new item."""
        raise action_error(_('operation not supported'), code=501)
    
    @auto_format_output
    def new(self):
        """GET /new: Form to create a new item."""
        raise action_error(_('operation not supported'), code=501)
    
    @auto_format_output
    def delete(self, id):
        """
        DELETE /id: Delete an existing item.
        """
        # h.form(h.url_for('message', id=ID), method='delete')
        # Rather than delete the setting this simple blanks the required fields - or removes the config dict entry
        raise action_error(_('operation not supported (yet)'), code=501)

    def show(self, id):
        """GET /id: Show a specific item."""
        return self.edit(id)


    #---------------------------------------------------------------------------
    # REST Action - EDIT/SHOW
    #---------------------------------------------------------------------------
    @web
    @authorize
    def edit(self, id, **kwargs):
        """GET /id;edit: Form to edit an existing item."""
        
        # special case
        if id == "messages":
            return action_ok(
                template='settings/messages' ,
            )
        
        user = c.logged_in_persona
        
        # Generate base settings dictonary for ALL settings
        settings_meta = copy.deepcopy(settings_base)
        settings      = {}
        
        # Populate settings dictionary for this user
        for setting_name in settings_meta.keys():
            v = user.config.get(setting_name)
            if type(v) in [str, unicode]: # ugly hack
                settings[setting_name] = v
            else:
                settings[setting_name] = location_to_string(v)
        
        return action_ok(
            data={
                'settings_meta' : settings_meta ,
                'settings'      : settings ,
            },
            template='settings/settings' ,
        )


    #---------------------------------------------------------------------------
    # REST Action - UPDATE
    #---------------------------------------------------------------------------
    
    @web
    @authorize
    def update(self, id, **kwargs):
        """
        PUT /id: Update an existing item.
        
        - Creates a custom validator schema for the inputed data that has changed from the db
        - Validates the request overlaying errors if generated
        - Saves update
        - Returns written object
        """

        # special case for generators
        if id == "messages":
            from civicboom.lib.communication.messages import generators
            for gen in generators:
                route_name = "route_"+gen[0]

                # setting = eg "ne", "c", "nec"
                setting = "".join([
                    request.POST.get(gen[0]+"_n", ""),
                    request.POST.get(gen[0]+"_e", ""),
                    request.POST.get(gen[0]+"_c", ""),
                ])

                # if setting = default, delete the key
                if setting == gen[1]:
                    if route_name in c.logged_in_persona.config:
                        del c.logged_in_persona.config[route_name]
                # if setting is non-default, set it
                else:
                    c.logged_in_persona.config[route_name] = setting

            Session.commit()
            return action_ok(
                message = _('settings updated') ,
                template='settings/messages' ,
            )

        data        = self.edit(id=id)['data']
        settings    = data['settings']
        
        # Setup custom schema for this update
        # List validators required
        validators = {}
        for validate_fieldname in [setting_name for setting_name in settings.keys() if setting_name in settings_validators and setting_name in kwargs and settings[setting_name] != kwargs[setting_name] ]:
            #print "adding validator: %s" % validate_fieldname
            validators[validate_fieldname] = settings_validators[validate_fieldname]
        # Build a dynamic validation scema based on these required fields and validate the form
        schema = build_schema(**validators)
        # Add any additional validators for custom fields
        if 'password_new' in validators:
            schema.fields['password_current'] = settings_validators['password_current'] # This is never added in the 
            schema.chained_validators.append(formencode.validators.FieldsMatch('password_new', 'password_new_confirm'))
        
        settings.update(kwargs)
        
        validate_dict(data, schema, dict_to_validate_key='settings', template_error='settings/settings')
        
        # Form has passed validation - continue to save/commit changes
        user        = c.logged_in_persona
        settings    = data['settings']
        
        # Save special properties that need special processing
        # (could have a dictionary of special processors here rather than having this code cludge this controller action up)
        if settings.get('avatar') != None:
            with tempfile.NamedTemporaryFile(suffix=".jpg") as original:
                a = settings['avatar']
                wh.copy_cgi_file(a, original.name)
                h = wh.hash_file(original.name)
                wh.copy_to_warehouse(original.name, "avatars-original", h, a.filename)

                with tempfile.NamedTemporaryFile(suffix=".jpg") as processed:
                    size = (160, 160)
                    im = Image.open(original.name)
                    if im.mode != "RGB":
                        im = im.convert("RGB")
                    im.thumbnail(size, Image.ANTIALIAS)
                    im.save(processed.name, "JPEG")
                    wh.copy_to_warehouse(processed.name, "avatars", h, a.filename)

            user.avatar = h
            del settings['avatar']

        if settings.get('location_home'):
            # translation to PostGIS format is done in the validator
            user.location_home = settings.get('location_home')
            del settings['location_home']
        elif settings.get("location_home_name"):
            user.location = "SRID=4326;POINT(%d %d)" % (0, 0) # FIXME: guess_lon_lat_from_name(request.POST["location_home_name"]), see Feature #47
            del settings['location_home_name']

        if settings.get('location_current'):
            user.location_current = settings.get('location_current')
            del settings['location_current']
        elif settings.get("location_current_name"):
            user.location = "SRID=4326;POINT(%d %d)" % (0, 0)
            del settings['location_current_name']

        if 'password_new' in settings:
            # OLD: We could put this in settings.py manager, have a dictionarys with special cases and functions to process/save them, therefor the code is transparent in the background. an idea?
            set_password(user, settings['password_new'], delay_commit=True)
            del settings['password_new'        ] # We dont want these saved
        if 'password_new_confirm' in settings:
            del settings['password_new_confirm']
        if 'password_current' in settings:
            del settings['password_current'    ]
        
        if 'email' in settings:
            user.email_unverified = settings['email']
            send_verifiy_email(user, message=_("please verify your email address"))
            del settings['email']
            # AllanC - todo - need message to say check email
        
        # Save all remaining properties
        for setting_name in settings.keys():
            log.debug("saving setting %s" % setting_name)
            user.config[setting_name] = settings[setting_name]
            
        Session.commit()
        
        if c.format == 'html':
            return redirect(url('settings'))
        
        return action_ok(
            message = _('settings updated') ,
            data    = data ,
            template='settings/settings' ,
        )


#---------------------------------------------------------------------------
# Old Settings Reference
#---------------------------------------------------------------------------
"""
    @authorize
    def messages(self, id=None):
        c.viewing_user = c.logged_in_persona
        return render("html/web/settings/messages.mako")

    @authorize
    @authenticate_form
    def save_messages(self, id=None, format="html"):
        c.viewing_user = c.logged_in_persona
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
"""
