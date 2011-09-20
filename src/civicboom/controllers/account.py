from civicboom.lib.base import *
from cbutils.misc import make_username
from civicboom.model import User, Group

from civicboom.lib.authentication   import get_user_from_openid_identifyer, get_user_and_check_password, signin_user, signin_user_and_redirect, signout_user, login_redirector, set_persona
from civicboom.lib.services.janrain import janrain
from civicboom.lib.accounts         import verify_email_hash, associate_janrain_account, set_password, has_account_without_password, send_verifiy_email
from civicboom.lib.constants    import get_action_objects_for_url

from civicboom.controllers.register import register_new_janrain_user

import time


log      = logging.getLogger(__name__)


class AccountController(BaseController):
    """
    @title Accounts
    @doc account
    @desc controller for signing in and out
    """

    #---------------------------------------------------------------------------
    # Signout
    #---------------------------------------------------------------------------
    
    # while not massively dangerous, posting an image with eg <img src="http://civicboom.com/account/signout">
    # is a common prank, so this needs authenticating
    @web
    @auth
    #@authenticate_form
    def signout(self, **kwargs):
        """
        POST /account/signout: End the current session

        This function is also pointed to from the ini config to trigger AuthKit to remove cookies

        Redirect to a new URL so that the browser doesn't cache it (Shouldn't be necessary, but it
        seems that sometimes it is?)

        @api account 1.0 (WIP)

        @return 302   redirect to the front page
        """
        signout_user(c.logged_in_persona)
        return redirect(url(controller='misc', action='titlepage', ut=str(time.time())))


    #---------------------------------------------------------------------------
    # Janrain Engage - http://www.janrain.com/products/engage
    #---------------------------------------------------------------------------

    @web
    # mobile requires a valid cert, mobile.civicboom.com doesn't have one
    #@https() # redirect to https for transfer of password
    def signin(self, **kwargs):
        """
        POST /account/signin: Create a new session

        @api account 1.0 (WIP)

        @param username     the user's civicboom.com username
        @param password     the user's civicboom.com password

        @return 200         logged in ok
                auth_token  the token to be supplied with any data-modifying requests
        """

        # If no POST display signin template
        if request.environ['REQUEST_METHOD'] == 'GET':
            
            action_objects = get_action_objects_for_url(session_get('login_redirect') or '')
            if action_objects:
                c.action_objects = action_objects
                #return render("/html/web/account/signin_frag.mako")
            
            #return render("/html/web/account/signin.mako")
            return action_ok()

        # Without this line, a simple blank POST would see no janrain token,
        # and no username / password, so it would leave c.logged_in_user
        # as-is. Then, it would return the CSRF token. This is bad because
        # it means any random third-party site can automatically get the
        # token, generate a form, and submit it.
        #
        # Thus, we need to only give out the token if the user has supplied
        # valid auth credentials with the request.
        if c.logged_in_user and False: # Shish: temp hack, mobile relies on the old behaviour
            raise action_error("user is logged in already", code=400)
        
        c.auth_info    = None
        login_provider = None

        # Authenticate with Janrain
        if 'token' in kwargs:
            if config['test_mode'] and kwargs.get('fake_janrain_return'):
                import json
                c.auth_info = json.loads(kwargs.get('fake_janrain_return'))
            else:
                c.auth_info = janrain('auth_info', token=kwargs.get('token'))
            
            if c.auth_info:
                c.logged_in_user = get_user_from_openid_identifyer(c.auth_info['profile']['identifier']) #Janrain guarntees the identifyer to be set
                login_provider   = c.auth_info['profile']['providerName']

        # Authenticate with standard username
        if 'username' in kwargs and 'password' in kwargs:
            c.logged_in_user = get_user_and_check_password(kwargs['username'], kwargs['password'])
            login_provider = "password"

        # If user has existing account: Login
        if c.logged_in_user:
            if c.format in ["html", "redirect"]:
                signin_user_and_redirect(c.logged_in_user, login_provider=login_provider)
            else:
                signin_user(c.logged_in_user, "api-password")
                return action_ok("logged in ok", {"auth_token": authentication_token()})
        
        # If no user found but we have Janrain auth_info - create user and redirect to complete regisration
        if c.auth_info:
            #try   : existing_user = get_user(c.auth_info['profile']['displayName'])
            #except: pass
            #if existing_user:
                # TODO
                # If we have a user with the same username they may be the same user
                # prompt them to link accounts OR continue with new registration.
                # Currently if a username conflict appears then a random new username is created and the user is prompted to enter a new one
                #pass
            
            c.logged_in_user = register_new_janrain_user(c.auth_info['profile'])             # Create new user from Janrain profile data
            signin_user_and_redirect(c.logged_in_user, login_provider=login_provider, redirect_url=url(controller="profile", action="index"))
            
        # If not authenticated or any janrain info then error
        user_log.warning("Failed to log in as '%s'" % kwargs.get('username', ''))
        
        err = action_error(_('Unable to authenticate user'), code=403)
        # AllanC - TODO
        # Check if user does exisit but simply has no 'password' login record accociated with it
        if has_account_without_password(kwargs.get('username')):
            err = action_error(_('%s has not set up a _site_name password yet, please visit your settings on the website') % kwargs.get('username'), code=403)
        if c.format in ["html", "redirect"]:
            set_flash_message(err.original_dict)
            return redirect_to_referer() #AllanC - TODO .. humm .. this will remove the login_action_referer so if they fail a login first time they cant perform the action thats remembered. This need thinking about.
        else:
            raise err

    #---------------------------------------------------------------------------
    # Switch Persona
    #---------------------------------------------------------------------------
    @web
    @auth
    def set_persona(self, id, prompt_aggregate=None, **kwargs):
        """
        POST /account/set_persona/{id}: change the currently active persona

        @api account 1.0 (WIP)

        @return 200     switched ok
        @return 500     switch failed
        """
        if set_persona(id):
            user_log.info("Switched to persona %s" % id)
            # AllanC - not a sutable solution - I wanted an AJAX working version
            #          I have put a hack in here to force html requests to be redirected
            # GregM: addded prompt aggregate (internal use only) to the redirect
            if c.format=='html':
                if prompt_aggregate:
                    return redirect(url(controller='profile', action='index', prompt_aggregate=prompt_aggregate))
                else:
                    return redirect(url(controller='profile', action='index'))
            return action_ok("switched persona")
        else:
            user_log.info("Failed to switch to persona %s" % id)
            raise action_error("failed to swich persona")


    #---------------------------------------------------------------------------
    # Link Janrain Account
    #---------------------------------------------------------------------------
    @web
    @authorize
    def link_janrain(self, **kwargs):
        """
        A user can have their account linked to multiple external accounts
        The benefit of this is that all external accounts registered with us will
        allow a user to aggregate over those external services.
        
        Only currently logged in users can add additional janrain accounts
        """
        id = kwargs.get('id')
        username = id
        if not username or username == 'me':
            username = c.logged_in_persona.username
            id = 'me'
        user_type = 'group'
        user = get_member(username)
        if isinstance(user, User):
            user_type = 'member'
            if not user == c.logged_in_user:
                raise action_error(code=403, message="No permission")
        else:
            raise action_error(code=404, message="Not applicable to groups")
        
        redirect_url = ('/settings/'+id+'/link_janrain').encode('ascii','ignore')
        
        if request.environ['REQUEST_METHOD'] == 'GET':
            redirect(url(redirect_url))
        
        c.auth_info = None
        
        if 'token' in kwargs:
            c.auth_info = janrain('auth_info', token=kwargs.get('token'))
            
        if c.auth_info:
            user_log.info("linked account from %s" % c.auth_info['profile']['providerName'])
            associate_janrain_account(user, c.auth_info['profile']['providerName'], c.auth_info['profile']['identifier'])
            set_flash_message(action_ok("Account successfully linked to _site_name"))
        else:
            set_flash_message(action_error("Error linking accounts").original_dict)
            
        redirect(url(redirect_url))


    #---------------------------------------------------------------------------
    # Verify Email
    #---------------------------------------------------------------------------
    # AllanC - TODO needs to be updated to use web_params and auto format
    def verify_email(self, id):
        """
        An email is generated for a user and a hash created for them in the URL
        see civicboom_lib for the send_verify_email that generates this if needed
        """
        if 'hash' in request.params :
            if verify_email_hash(id, request.params['hash'], commit=True):
                set_flash_message(action_ok(_('email address has been successfully validated')))
            else:
                set_flash_message(action_error(_('email validation failed, if you have changed any user settings since sending the validation email, please validate again')).original_dict)
            redirect('/')


    #---------------------------------------------------------------------------
    # Forgotten Password
    #---------------------------------------------------------------------------
    @web
    def forgot_password(self, id=None, **kwargs):
        """
        Users can get new hash link set to there email address
        """
        c.hash = kwargs.get('hash')
        
        user = get_member(id or kwargs.get('username') or kwargs.get('email'), search_email=True)
        if user.__type__ == 'group':
            raise action_error('a _group cannot have a password set, please login as yourself and switch to the _group persona', code=404)
        
        # Step 1: User request link with hash to be sent via email
        if not c.hash:
            #send_forgot_password_email(user)
            send_verifiy_email(user, controller='account', action='forgot_password', message=_('reset your password'))
            return action_ok(_('Password reminder sent, please check your email'))
            
        if not verify_email_hash(user, c.hash): # abort if unable to verify user
            raise action_error(_('unable to verify user'), code=400)
            
        # Step 2: User identifed with hash, show form to enter new password
        if request.environ['REQUEST_METHOD'] == 'GET':
            # form to enter new password
            return render("/html/web/account/forgot_password.mako")
        
        # Step 3: Validate new password and set
        else:
            import civicboom.lib.form_validators.base
            import formencode.validators
            
            class SetPasswordSchema(civicboom.lib.form_validators.base.DefaultSchema):
                password_new         = civicboom.lib.form_validators.base.PasswordValidator(not_empty=True)
                password_new_confirm = civicboom.lib.form_validators.base.PasswordValidator(not_empty=True)
                chained_validators   = [formencode.validators.FieldsMatch('password_new', 'password_new_confirm')]
            
            # Validate new password
            try:
                kwargs = SetPasswordSchema().to_python(kwargs)
            # Validation Failed
            except formencode.Invalid as error:
                dict_validated        = error.value
                dict_validated_errors = error.error_dict or {}
                raise action_error(
                    status   = 'invalid' ,
                    code     = 400 ,
                    message  = _('failed validation') ,
                    template = 'account/forgot_password'
                )
            
            user_log.info('new password set for %s' % user)
            
            set_password(user, kwargs['password_new'])
            set_flash_message(_('password has been set'))
            redirect(url(controller='account', action='signin'))
