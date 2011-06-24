"""
REST Settings controler

Settings are broken into named groups
These groups of settings can be view/editied using standard REST calls

The principle is that each settings has a validator associated with it
Only the form fields that are sent are validated and saved
(this is an issue for realted fields such as password, that creates a bit of a mess, see code below)
"""

from civicboom.lib.base import *
from civicboom.model import User

from civicboom.model.member import group_member_roles, group_join_mode, group_member_visibility, group_content_visibility

from civicboom.lib.constants import setting_titles

import cbutils.warehouse as wh

import copy
import tempfile
import Image
import formencode

from civicboom.lib.communication.messages import generators

from civicboom.lib.form_validators.validator_factory import build_schema
from civicboom.lib.form_validators.dict_overlay import validate_dict

from civicboom.lib.accounts import set_password, send_verifiy_email
from civicboom.model.meta import location_to_string

from civicboom.lib.web import _find_template_basic

log = logging.getLogger(__name__)


# This also appears in Group Controller
class PrivateGroupValidator(formencode.validators.FancyValidator):
    messages = {
        'invalid'           : _('Value must be one of: public; private'),
        'require_upgrade'   : _('You require a paid account to use this feature, please contact us!'),
        }

    def _to_python(self, value, state):
        if value not in ['public', 'private']:
            raise formencode.Invalid(self.message('invalid', state), value, state)
        if value == "private" and not c.logged_in_persona.has_account_required('plus'):
            raise formencode.Invalid(self.message('require_upgrade', state), value, state)
        return value


#---------------------------------------------------------------------------
# Setting Units
#---------------------------------------------------------------------------
# Define settings groups, default values and display text

settings_base = {}


def add_setting(name, description, value='', group=None, **kwargs):
    setting = dict(name=name, description=description, value=value, group=group, **kwargs)
    settings_base[setting['name']]=setting


add_setting('name'                      , _('Display name' )             , group='general/general'    , weight=0  , type='string'                                                                            )
add_setting('username'                  , _('Username' )                 , group='general/general'    , weight=1  , type='display'         , who='user'                                                      )
add_setting('description'               , _('Description'  )             , group='general/general'    , weight=2  , type='longstring'      , info=_('Tell the world about you and your interests.')          )

add_setting('default_role'              , _('Default Role')              , group='general/group'      , weight=3  , type='enum'            , who='group' , value=group_member_roles.enums                    )
add_setting('join_mode'                 , _('Join Mode')                 , group='general/group'      , weight=4  , type='enum'            , who='group' , value=group_join_mode.enums                       )
add_setting('member_visibility'         , _('Member Visibility')         , group='general/group'      , weight=5  , type='enum'            , who='group' , value=group_member_visibility.enums               )
add_setting('default_content_visibility', _('Default Content Visibility'), group='general/group'      , weight=6  , type='enum'            , who='group' , value=group_content_visibility.enums              )

add_setting('website'                   , _('Website'      )             , group='general/contact'    , weight=7  , type='url'             , info=_('Optional: add your website or blog etc. to your profile'))
add_setting('email'                     , _('Email Address')             , group='general/contact'    , weight=8  , type='email'           , who='user'                                                      )
#add_setting('twitter_username'          , _('Twitter username')          , group='aggregation')
#add_setting('twitter_auth_key'          , _('Twitter authkey' )          , group='aggregation')
#add_setting('broadcast_instant_news'    , _('Twitter instant news')      , group='aggregation', type='boolean')
#add_setting('broadcast_content_posts'   , _('Twitter content' )          , group='aggregation', type='boolean')
add_setting('avatar'                    , _('Avatar' )                   , group='general/avatar'     , weight=9 , type='file'                                                                              )

add_setting('password_current'          , _('Current password')          , group='password/password'  , weight=100, type='password_current', who='user'                                                      )
add_setting('password_new'              , _('New password')              , group='password/password'  , weight=101, type='password'        , who='user'                                                      )
add_setting('password_new_confirm'      , _('New password again')        , group='password/password'  , weight=102, type='password'        , who='user'                                                      )

# Ignore these messages generators!
ignore_generators = ['msg_test',
                     'assignment_response_mobile',
                     'syndicate_accept',
                     'syndicate_decline',
                     'syndicate_expire',
                    ]
i = 200
for gen in generators:
    if not gen[0] in ignore_generators:
        add_setting('route_'+gen[0], str(gen[2]).capitalize(), group='notifications/notifications', weight=i, type="set", value=('n','e'), default=gen[1])
        i = i + 1

add_setting('location_home'             , _('Home Location' )            , group='location/location'  , weight=300, type='location' )
add_setting('location_home_name'        , _('Home Location' )            , group='location/location'  , weight=301, type='string_location' )

add_setting('help_popup_created_user', _('Hide the help popup shown upon login to the site'), group='help_adverts/help_popups', weight=400, type='boolean')
add_setting('help_popup_created_group', _('Hide the help popup shown upon switching to a group'), group='help_adverts/help_popups', weight=401, type='boolean')
add_setting('help_popup_created_assignment', _('Hide the help popup shown upon creating an assignment'), group='help_adverts/help_popups', weight=402, type='boolean')

add_setting('advert_profile_mobile', _('Hide the info box encouraging the use of the mobile app'), group='help_adverts/adverts', weight=403, type='boolean')
add_setting('advert_profile_group', _('Hide the info box encouraging the use of _groups'), group='help_adverts/adverts', weight=404, type='boolean')

add_setting('auto_follow_on_accept', _('Automatically follow the user or _group who created a request on accepting it'), group='advanced/follower_settings', weight=1000, type='boolean')
add_setting('allow_registration_follows', _('Allow this user or _group to automatically follow users when they register'), group='advanced/follower_settings', weight=1001, type='boolean', info=_('Please speak to our team before you change this option!'))

#---------------------------------------------------------------------------
# Setting Validators (for dynamic scema construction)
#---------------------------------------------------------------------------
#  these are kept separte from the group definitions because the group defenitions dict is sent to clients, we do not want to contaminate that dict

import formencode
import civicboom.lib.form_validators
import civicboom.lib.form_validators.base
import civicboom.lib.form_validators.registration

# Type validators, convert from our from type to validators
type_validators = { 'string':           formencode.validators.UnicodeString(),
                    'longstring':       formencode.validators.UnicodeString(),
                    'url':              formencode.validators.URL(),
                    'email':            civicboom.lib.form_validators.registration.UniqueEmailValidator(),
                    'password':         civicboom.lib.form_validators.base.PasswordValidator(),
                    'password_current': civicboom.lib.form_validators.base.CurrentUserPasswordValidator(),
                    'file':             formencode.validators.FieldStorageUploadConverter(),
                    'location':         civicboom.lib.form_validators.base.LocationValidator(),
                    'string_location':  formencode.validators.UnicodeString(),
                    'boolean':          formencode.validators.UnicodeString(max=10, strip=True),
}

settings_validators = {}

for setting in settings_base.values():
    # Special handling for sets (custom Set validator and also separated so we can handle form submissions
    if setting['type'] == 'set':
        for val in setting['value']:
            settings_validators[setting['name']+'-'+val] = formencode.validators.OneOf((val, ''))
        settings_validators[setting['name']] = civicboom.lib.form_validators.base.SetValidator(set=setting['value']) #formencode.validators.Set(setting['value'].split(','))
    # Special handling for enums
    elif setting['type'] == 'enum':
        # HACK ALERT: GregM: Stupid Validator needed for private content
        if setting['name'] in ['default_content_visibility', 'member_visibility']:
            settings_validators[setting['name']] = PrivateGroupValidator()
        else:
            settings_validators[setting['name']] = formencode.validators.OneOf(setting['value'])
    # Anything else from default type_validators
    else:
        settings_validators[setting['name']] = type_validators.get(setting['type'])

def build_meta(user, user_type, panel):
    settings_meta = dict( [ (setting['name'], setting ) for setting in copy.deepcopy(settings_base).values() if setting.get('who', user_type) == user_type and setting['group'].split('/')[0] == panel ] )
    panels = dict( [ ( setting['group'].split('/')[0], {'panel':setting['group'].split('/')[0], 'weight':setting['weight'], 'title': setting_titles.get(setting['group'].split('/')[0]) if setting_titles.get(setting['group'].split('/')[0]) else setting['group'].split('/')[0]} ) for setting in settings_base.values() if setting.get('who', user_type) == user_type ] )
    
    settings_hints = {}
    # Populate settings dictionary for this user
    for setting_name in settings_meta.keys():
        if settings_meta[setting_name].get('who', user_type) == user_type:
            if setting_name == 'email' and user.email_unverified != None:
                settings_hints['email'] = _( 'You have an unverified email address. This could be for two reasons:') + '<ol>' + \
                                             '<li>' + _('You have signed up to Civicboom via Twitter, Facebook, LinkedIn, etc.') + '</li>' + \
                                             '<li>' + _('You have changed your email address and not verified it.') + '</li>' + \
                                             '</ol>' + _('To verify your email: please check your email account (%s) and follow instructions.') % user.email_unverified + '<br />' + \
                                             _('OR enter new email address below and check your email.')
                #_('You have an unverified email address (%s), please check your email. If this address is incorrect please update and save, then check your email.') % user.email_unverified
            if setting_name == 'password_current' and 'password_current' in settings_meta and not 'password' in [login.type for login in user.login_details]:
                del settings_meta[setting_name]
                settings_hints['password_new'] = _("You have signed up via Twitter, Facebook, LinkedIn, etc. In order to login to our mobile app, please create a Civicboom password here. (You will use this password and your username to login to the app.)")
            if 'password' in setting_name and user.email_unverified != None:
                if setting_name in settings_meta:
                    if not '_readonly' in settings_meta[setting_name]['type']:
                        settings_meta[setting_name]['type'] = settings_meta[setting_name]['type'] + '_readonly'
                    if not 'password' in [login.type for login in user.login_details]:
                        settings_hints['password_new'] = _("If you want to change your Civicboom password, please verify your email address (see above). You will need to verify your address and create a password to use our mobile app.")
                    else:
                        settings_hints['password_current'] = _("If you want to change your Civicboom password, please verify your email address (see above).")
    data = dict( settings_meta=settings_meta,
                 settings_hints=settings_hints,
                 panels=panels,
                 panel=panel
    )
    return data


def find_template(panel, user_type):
    try:
        # panel_user_type?
        _find_template_basic(action='panel/'+panel+'_'+user_type)
        template = panel+'_'+user_type
    except:
        try:
            # panel?
            _find_template_basic(action='panel/'+panel)
            template = panel
        except:
            # default to generic
            template = 'generic'
    return template


def copy_user_settings(settings_meta, user, user_type):
    settings = {}
    for setting_name in settings_meta.keys():
        setting_name_repl = setting_name.replace('_read_only', '')
        if settings_meta[setting_name_repl].get('who', user_type) == user_type:
            if hasattr(user, setting_name_repl):
                v = getattr(user, setting_name_repl)
            else:
                v = user.config.get(setting_name_repl, settings_meta[setting_name].get('default'))
            # Special case for email addresses, if the user has no email address but has unverified, show that instead.
            if v == None and setting_name == 'email' and user.email_unverified != None:
                v = user.email_unverified
            if isinstance(v, basestring): # ugly hack
                settings[setting_name_repl] = v
            else:
                settings[setting_name_repl] = location_to_string(v)
    return settings


#---------------------------------------------------------------------------
# REST Controller
#---------------------------------------------------------------------------

class SettingsController(BaseController):
    """
    @t-itle Settings
    @d-oc settings
    @d-esc REST controller for Settings
    """

    #http://wiki.pylonshq.com/display/pylonscookbook/How+map.resource+enables+controllers+as+services    
    #needs in config/routing.py -> map.resource('setting', 'settings')
    
    #---------------------------------------------------------------------------
    # REST Actions - simple passthrough actions
    #---------------------------------------------------------------------------
    
    def index(self):
        """GET /settings: All items in the collection."""
        return self.panel() #self.show(None)
    
    @auto_format_output
    def create(self):
        """POST /settings: Create a new item."""
        raise action_error(_('operation not supported'), code=501)
    
    @auto_format_output
    def new(self):
        """GET /settings/new: Form to create a new item."""
        raise action_error(_('operation not supported'), code=501)
    
    @auto_format_output
    def delete(self, id):
        """
        DELETE /settings/id: Delete an existing item.
        """
        # h.form(h.url_for('message', id=ID), method='delete')
        # Rather than delete the setting this simple blanks the required fields - or removes the config dict entry
        raise action_error(_('operation not supported (yet)'), code=501)

    def show(self, id, **kwargs):
        """GET /settings/id: Show a specific item."""
        return self.panel(id=id, **kwargs) #self.edit(id)

    @web
    @authorize
    def panel(self, id='me', panel='general', **kwargs):
#        print url('settings',action='show',id="me", panel="generic")
        if panel=="general" and not c.action in ("panel", "show", "index", "edit"):
            panel=c.action
        #username = id
        #if not username or username == 'me':
        #     username = c.logged_in_persona.username
        #     id = 'me'
        #user_type = 'group'
        #user = get_member(username)  
        #if isinstance(user, User):
        #    user_type = 'member'
        user = get_member(id)
        
        
        raise_if_current_role_insufficent('admin', group=user)
        
        data = build_meta(user, user.__type__, panel)
        
        # Janrain HACK
        if user.__type__ == 'user' and panel == 'link_janrain':
            return action_ok(
                data=data,
                username=id,
                user_type=user.__type__,
                template="settings/panel/link_janrain",
            )
            
        if panel not in data['panels']:
            raise action_error(code=404, message="This panel is not applicable for a " + user.__type__)
        
        settings_meta  = data['settings_meta']
        # Populate settings dictionary for this user
        settings       = copy_user_settings(settings_meta, user, user.__type__)
                    
        data['settings'] = settings
        
        template = find_template(panel, user.__type__)
        
        return action_ok(
            data     = data,
            panel    = panel,
            username = id,
            user_type= user.__type__,
            template = "settings/panel/"+template,
        )

    #---------------------------------------------------------------------------
    # REST Action - EDIT/SHOW
    #---------------------------------------------------------------------------
    
    @web
    @authorize
    @role_required('admin')
    def edit(self, id, **kwargs):
        """GET /settings/id/edit: Form to edit an existing item."""
        
        # Return panel instead of old settings template!
        return self.panel(id=id, panel=kwargs.get('panel'))
#        
#        # special case
#        if id == "messages":
#            return action_ok(
#                template='settings/messages' ,
#            )
#        
#        user = c.logged_in_persona
#        
#        # Generate base settings dictionary for ALL settings
#        settings_meta = copy.deepcopy(settings_base)
#        settings      = {}
#        
#        # Populate settings dictionary for this user
#        for setting_name in settings_meta.keys():
#            v = user.config.get(setting_name)
#            if type(v) in [str, unicode]: # ugly hack
#                settings[setting_name] = v
#            else:
#                settings[setting_name] = location_to_string(v)
#        
#        return action_ok(
#            data={
#                'settings_meta' : settings_meta ,
#                'settings'      : settings ,
#            },
#            template='settings/settings' ,
#        )


    #---------------------------------------------------------------------------
    # REST Action - UPDATE
    #---------------------------------------------------------------------------
    
    @web
    @authorize
    def update(self, id='me', **kwargs):
        """
        PUT /id: Update an existing item.
        
        - Creates a custom validator schema for the input data that has changed from the DB
        - Validates the request overlaying errors if generated
        - Saves update
        - Returns written object
        """
        # Check permissions on object, find actual username and store in username
        # id will always contain me if it was passed
        
        private = kwargs.get('private')
        if private: del kwargs['private']
        #username = id
        #if not username or username == 'me':
        #    username = c.logged_in_persona.username
        #    id = 'me'
        #user_type = 'group'
        #user = get_member(username)
        
        user = get_member(id)
        
        if user.username != c.logged_in_user.username:
            raise_if_current_role_insufficent('admin', group=user)

        user_log.info("Saving general settings")
        
        # User panel if there else use general
        panel = kwargs['panel'] if 'panel' in kwargs and kwargs['panel'] != '' else 'general'
        if 'panel' in kwargs:
            del kwargs['panel']
        
        # Find template from panel and user_type
        template = find_template(panel, user.__type__)
        
        # variables to store template and redirect urel
        panel_template = ('settings/panel/'+template).encode('ascii','ignore')
        
        if c.action=='create' and c.controller=='groups' and c.format=='html':
            panel_redirect = url('member', id=id)
        else:
            panel_redirect = url('setting', id=id, panel=panel)
            
        # If no new password set disregard (delete) all password fields!
        if kwargs.get('password_new') == '':
            del kwargs['password_new']
            try:
                del kwargs['password_current']
            except:
                pass
            try:
                del kwargs['password_new_confirm']
            except:
                pass
                
        # GregM: Patched to remove avatar kwarg if blank (keeping current avatar on settings save!)
        if kwargs.get('avatar') == '':
            del kwargs['avatar']
        
        data = build_meta(user, user.__type__, panel)
        
        data['settings'] = copy_user_settings(data['settings_meta'], user, user.__type__)
        
        data['settings'].update(kwargs)
        
        settings = kwargs
        
        for delete in ['action', 'controller', 'sub_domain', 'format', '_authentication_token', 'submit', '_method']:
            try:
                del settings[delete]
            except:
                pass
        
        if len(settings) == 0:
            raise action_error(code=400, message=_("No settings to update"))
        
        # Setup custom schema for this update
        # List validators required
        validators = {}
        if len(set(settings.keys()) - set(settings_validators.keys())) > 0:
            raise action_error(code=400, message=_("You are trying to update a setting that does not exist!"))
        for validate_fieldname in [setting_name for setting_name in settings.keys() if setting_name in settings_validators and setting_name in kwargs and settings_base[setting_name.split('-')[0]].get('who', user.__type__) == user.__type__]:
            log.debug("adding validator: %s" % validate_fieldname)
            validators[validate_fieldname] = settings_validators[validate_fieldname]
        # Build a dynamic validation schema based on these required fields and validate the form
        schema = build_schema(**validators)
        # Add any additional validators for custom fields
        if 'password_new' in validators:
            if 'password' in [login.type for login in user.login_details]:
                schema.fields['password_current'] = settings_validators['password_current'] # This is never added in the
            schema.chained_validators.append(formencode.validators.FieldsMatch('password_new', 'password_new_confirm'))
            if user.email_unverified != None:
                schema.fields['password_new'] = civicboom.lib.form_validators.base.EmptyValidator()
        
        validate_dict(data, schema, dict_to_validate_key='settings', template_error=panel_template)
        
        # Form has passed validation - continue to save/commit changes
        settings    = data['settings']
        
        # Save special properties that need special processing
        # (could have a dictionary of special processors here rather than having this code cludge this controller action up)
        # GregM: check kwargs as if no new avatar and has current avatar this FAILS!
        if kwargs.get('avatar') != None:
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
            if user.email != settings['email']:
                user.email_unverified = settings['email']
                send_verifiy_email(user, message=_("please verify your email address"))
            del settings['email']
            # AllanC - todo - need message to say check email
        
        # Save validated Sets: Needs cleaning up!
        for setting_set in [(setting_name, settings_base[setting_name].get('value',[])) for setting_name in settings_base.keys() if settings_base[setting_name].get('type') == 'set']:
            setting_name = setting_set[0]
            # If storing using the api route_this = 'en', route_that = 'n', etc.
            if setting_name in settings:
                if setting_name in validators:
                    if hasattr(user, setting_name):
                        setattr(user, setting_name, settings[setting_name])
                    else:
                        if settings[setting_name] == None:
                            settings[setting_name] = ['']
                        user.config[setting_name] = ''.join(settings[setting_name])
                                                                                    
                    del settings[setting_name]
                    for setting_value in setting_set[1]:
                        if setting_name+'-'+setting_value in settings:
                            del settings[setting_name+'-'+setting_value]
            # If storing using the web route_this-e = 'e', route_this-n = 'n', etc.
            else:
                setting_new_value = ''
                setting_count = 0
                for setting_value in setting_set[1]:
                    if setting_name+'-'+setting_value in settings:
                        setting_count = setting_count + 1
                        setting_new_value = setting_new_value + (settings[setting_name+'-'+setting_value] or '')
                        del settings[setting_name+'-'+setting_value]
                if setting_count == len(setting_set[1]):
                    if validators.get(setting_name+'-'+setting_value):
                        if hasattr(user, setting_name):
                                setattr(user, setting_name, setting_new_value)
                        else:
                            user.config[setting_name] = setting_new_value
        
        # Save all remaining validated(!) properties
        for setting_name in settings.keys():
            log.debug("saving setting %s" % setting_name)
            if setting_name in validators:
                if hasattr(user, setting_name):
                    setattr(user, setting_name, settings[setting_name])
                else:
                    if settings[setting_name] == None:
                        try:
                            del user.config[setting_name]
                        except:
                            pass
                    else:
                        user.config[setting_name] = settings[setting_name]
        
        Session.commit()
        
        if private:
            return
        
        if c.format == 'html':
            set_flash_message(action_ok(_('Settings updated')))
            return redirect(url(panel_redirect))
        
        return action_ok(
            message = _('Settings updated') ,
            data    = data ,
            panel   = panel,
            template= panel_template ,
        )
