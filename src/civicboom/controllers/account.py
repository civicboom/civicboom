from civicboom.lib.base import *

from civicboom.lib.authentication   import get_user_from_openid_identifyer, get_user_and_check_password, signin_user_and_redirect, signout_user, login_redirector
from civicboom.lib.services.janrain import janrain
from civicboom.controllers.widget   import setup_widget_env
from civicboom.lib.helpers          import url_from_widget

# Import other controller actions
from civicboom.controllers.register import register_new_janrain_user
from civicboom.lib.civicboom_lib    import verify_email, associate_janrain_account


log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class AccountController(BaseController):

    #---------------------------------------------------------------------------
    # Signout
    #---------------------------------------------------------------------------
    
    # while not massively dangerous, posting an image with eg <img src="http://civicboom.com/account/signout">
    # is a common prank, so this needs authenticating
    @authenticate_form
    def signout(self, format="json"):
        """
        This function is also pointed to from the ini config to trigger AuthKit to remove cookies
        """
        signout_user(c.logged_in_user)
        return redirect('/')


    #---------------------------------------------------------------------------
    # Janrain Engage - http://www.janrain.com/products/engage
    #---------------------------------------------------------------------------

    @auto_format_output()
    @https() # redirect to https for transfer of password
    def signin(self, format="json"):

        # If no POST display signin template
        if request.environ['REQUEST_METHOD'] == 'GET':
            if 'widget_username' in request.params:
                setup_widget_env()
                return render("/widget/widget_signin.mako")
            return render("/web/account/signin.mako")
        
        c.auth_info    = None
        login_provider = None

        # Authenticate with Janrain
        if 'token' in request.POST:
            c.auth_info = janrain('auth_info', token=request.POST.get('token'))
            if c.auth_info:
                c.logged_in_user = get_user_from_openid_identifyer(c.auth_info['profile']['identifier']) #Janrain guarntees the identifyer to be set
                login_provider = c.auth_info['profile']['providerName']

        # Authenticate with standard username
        if 'username' in request.POST and 'password' in request.POST:
            c.logged_in_user = get_user_and_check_password(request.POST['username'], request.POST['password'])
            login_provider = "password"

        # If user has existing account: Login
        if c.logged_in_user:
            if format in ["html", "redirect"]:
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
            
            u = register_new_janrain_user(c.auth_info['profile'])             # Create new user from Janrain profile data
            # added to assiciate_janrain civicboomlib call #janrain('map', identifier=c.auth_info['profile']['identifier'], primaryKey=u.id) # Let janrain know this users primary key id, this is needed for agrigation posts
            signin_user_and_redirect(u, login_provider=c.auth_info['profile']['identifier'])
            #redirect(url(controller='register', action='new_user', id=u.id)) #No need to redirect to register as the base controler will do this
            
        # If not authenticated or any janrain info then error
        err = action_error(_('Unable to authenticate user'), code=403)
        if format == "html":
            set_flash_message(err)
            return redirect_to_referer()
        else:
            return err

    #---------------------------------------------------------------------------
    # Link Janrain Account
    #---------------------------------------------------------------------------
    @authorize(is_valid_user)
    def link_janrain(self):
        """
        A user can have there account linked to multiple external accounts
        The benefit of this is that all external accounts registered with us will
        allow a user to aggregate over those external services.
        
        Only currently logged in users can add additional janrain accounts
        """
        if request.environ['REQUEST_METHOD'] == 'GET':
            return render("/web/account/link_janrain.mako")
        
        c.auth_info = None
        
        if 'token' in request.POST:
            c.auth_info = janrain('auth_info', token=request.POST.get('token'))
            
        if c.auth_info:
            associate_janrain_account(c.logged_in_user, c.auth_info['profile']['providerName'], c.auth_info['profile']['identifier'])
            set_flash_message(action_ok("Account successfully linked to _site_name"))
        else:
            set_flash_message(action_error("Error linking accounts"))
            
        redirect(url.current())


    #---------------------------------------------------------------------------
    # Verify Email
    #---------------------------------------------------------------------------
    def verify_email(self, id):
        """
        An email is generated for a user and a hash created for them in the URL
        see civicboom_lib for the send_verify_email that generates this if needed
        """
        if 'hash' in request.params :
            if verify_email(id, request.params['hash'], commit=True):
                set_flash_message(action_ok(_('email address has been successfully validated')))
            else:
                set_flash_message(action_error(_('email validation failed, if you have changed any user settings since sending the validation email, please validate again')))
            redirect('/')


    #---------------------------------------------------------------------------
    # Forgotten Password
    #---------------------------------------------------------------------------
    def forgotten_password(self):
        """
        Placeholder for forgotten password feature
        """
        pass
    



    #-----------------------------------------------------------------------------
    # Standalone Login Redirector action
    #-----------------------------------------------------------------------------    
    def login_redirect(self):
        """
        During the signin process the login redirector is followed automatically
        However
        With signing over the widget the signin process if fragmented and differnt popup windows need to be closed
        The original frame that needs to perform the original action is separte from the login frame
        When the login frame closes it fires a javascript event that causese the widget to refresh
        When this widget refreshes it will follow this login redirector call to point it in the right direction
        """

        login_redirector()
        #If this method returns then there has been no login redirector

        setup_widget_env() #This will get widget env's from the referer url
        redirect(url_from_widget(controller='widget', action='main'))
