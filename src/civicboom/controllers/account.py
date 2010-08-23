from civicboom.lib.base import *

from civicboom.lib.authentication      import get_user_from_openid_identifyer, get_user_and_check_password, signin_user, signout_user, login_redirector
from civicboom.lib.database.get_cached import get_user
from civicboom.lib.services.janrain    import janrain
from civicboom.controllers.widget      import setup_widget_env
from civicboom.lib.helpers             import url_from_widget

# Import other controller actions
from civicboom.controllers.register import register_new_janrain_user
from civicboom.lib.civicboom_lib    import verify_email


import logging
log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class AccountController(BaseController):
    
    #-----------------------------------------------------------------------------
    # Signin and Signout
    #-----------------------------------------------------------------------------
    # Reference - "Definitive Guide to Pylons" (pg 439)
    # and http://pylonsbook.com/en/1.1/simplesite-tutorial-part-3.html#signing-in-and-signing-out

    @https()
    def _old_signin(self):
        """
        AuthKit implementation of signin
        NOTE: this is OVERRIDDEN by the definition below and is here should we need to degrade back to AuthKit
        """
        if not request.environ.get('REMOTE_USER'): #AuthKit stores the current username in the REMOTE_USER env
            abort(401) #This triggers the AuthKit middleware into displaying the sign-in form
        else:
            user_log.info("logged in")
            return redirect(url('/'))

    # while not massively dangerous, posting an image with eg <img src="http://civicboom.com/account/signout">
    # is a common prank
    @authenticate_form
    def signout(self):
        """
        This function is also pointed to from the ini config to trigger AuthKit to remove cookies
        """
        signout_user(c.logged_in_user)
        return redirect('/')


    #-----------------------------------------------------------------------------
    # Janrain Engage - http://www.janrain.com/products/engage
    #-----------------------------------------------------------------------------

    # To degrade back to AuthKit rename this method
    @https() # redirect to https for transfer of password
    def signin(self):

        # If no POST display signin template
        if request.environ['REQUEST_METHOD'] == 'GET':
            if 'widget_username' in request.params:
                setup_widget_env()
                return render("/widget/widget_signin.mako")
            #c.janrain_return_url = urllib.quote_plus(url.current(host=app_globals.site_host)) # AllanC moved to app_globals
            return render("/web/account/signin.mako")
        
        c.auth_info = None

        # Authenticate with Janrain
        if 'token' in request.POST:
            c.auth_info = janrain('auth_info', token=request.POST.get('token'))
            if c.auth_info:
                c.logged_in_user = get_user_from_openid_identifyer(c.auth_info['profile']['identifier']) #Janrain guarntees the identifyer to be set

        # Authenticate with standard username
        if 'username' in request.POST and 'password' in request.POST:
            c.logged_in_user = get_user_and_check_password(request.POST['username'], request.POST['password'])

        # If user has existing account: Login
        if c.logged_in_user:
            signin_user(c.logged_in_user)
        
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
            janrain('map', identifier=c.auth_info['profile']['identifier'], primaryKey=u.id) # Let janrain know this users primary key id, this is needed for agrigation posts
            signin_user(u)
            #redirect(url(controller='register', action='new_user', id=u.id)) #No need to redirect to register as the base controler will do this
            
        # If not authenticated or any janrain info then error
        flash_message(_('Unable to authenticate user'))
        return redirect_to_referer()


    #-----------------------------------------------------------------------------
    # Verify Email
    #-----------------------------------------------------------------------------
    def verify_email(self, id):
        """
        An email is generated for a user and a hash created for them in the URL
        see civicboom_lib for the send_verify_email that generates this if needed
        """
        if 'hash' in request.params :
            if verify_email(id, request.params['hash'], commit=True):
                flash_message(_('email address has been successfully validated'))
            else:
                flash_message(_('email validation failed, if you have changed any user settings since sending the validation email, please validate again'))
            redirect('/')
            
    #-----------------------------------------------------------------------------
    # Forgotten Password
    #-----------------------------------------------------------------------------
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
