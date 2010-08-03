from civicboom.lib.base import BaseController, render, request, url, abort, redirect, c, app_globals, _, session, flash_message, redirect_to_referer

from civicboom.lib.authentication   import get_user_from_openid_identifyer, get_user_and_check_password
from civicboom.lib.services.janrain import janrain
from civicboom.lib.web              import session_remove, session_get

from civicboom.model.member       import User, UserLogin
from civicboom.model.meta         import Session

import urllib

import logging
log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class AccountController(BaseController):
    
    #-----------------------------------------------------------------------------
    # Signin and Signout
    #-----------------------------------------------------------------------------
    # Reference - "Definitive Guide to Pylons" (pg 439)
    # and http://pylonsbook.com/en/1.1/simplesite-tutorial-part-3.html#signing-in-and-signing-out

    def signin(self):
        """
        AuthKit implementation of signin
        NOTE: this is OVERRIDDEN by the definition below and is here should we need to degrade back to AuthKit
        """
        if not request.environ.get('REMOTE_USER'): #AuthKit stores the current username in the REMOTE_USER env
            abort(401) #This triggers the AuthKit middleware into displaying the sign-in form
        else:
            user_log.info("logged in")
            return redirect(url('/'))

    def signout(self):
        """
        This function is also pointed to from the ini config to trigger AuthKit to remove cookies
        """
        user_log.info("logged out")
        session.clear()
        #session.save()
        #flash_message("Successfully signed out!")
        return redirect('/')


    #-----------------------------------------------------------------------------
    # Janrain Engage - http://www.janrain.com/products/engage
    #-----------------------------------------------------------------------------

    # To degrade back to AuthKit rename this method
    #@https # redirect to https for transfer of password
    def signin(self):

        # If no POST display signin template
        if request.environ['REQUEST_METHOD'] == 'GET':
            c.janrain_return_url = urllib.quote_plus(url.current(host=app_globals.site_host))
            return render("/web/account/signin.mako")
        
        c.auth_info = None

        # Authenticate with Janrain
        if 'token' in request.POST:
            c.auth_info = janrain('auth_info', token=request.POST.get('token'))
            if c.auth_info:
                c.logged_in_user = get_user_from_openid_identifyer(auth_info['profile']['identifier']) #Janrain guarntees the identifyer to be set

        # Authenticate with standard username
        if 'username' in request.POST and 'password' in request.POST:
            c.logged_in_user = get_user_and_check_password(request.POST['username'], request.POST['password'])

        # If user has existing account: Login
        if c.logged_in_user:
            user_log.info("logged in")               # Log user login
            session['user_id'] = c.logged_in_user.id # Set server session variable to user.id
            
            # Redirect them back to where they were going if a redirect was set
            login_redirect = session_get('login_redirect')
            if login_redirect:
                session_remove('login_redirect')
                return redirect(login_redirect)
            return redirect('/')
            
        # If no user found but we have Janrain auth_info - create user and redirect to complete regisration
        if c.auth_info:
            profile = auth_info['profile']
            
            u = User()
            u.status        = "pending"
            u.username      = valid_username(profile.get('displayName'))
            u.name          = profile.get('name').get('formatted')
            u.email         = profile.get('verifiedEmail') or profile.get('email')
            u.avatar        = profile.get('photo')
            u.webpage       = profile.get('url')
            #u.location      = get_location_from_json(profile.get('address'))
            
            u_login = UserLogin()
            u_login.user   = u()
            u_login.type   = profile['providerName']
            u_login.token  = profile['identifier']
            
            Session.addall([u,u_login])
            Session.commit()
            
            u.config['dob']  = profile.get('birthday')
            #u.config['url']  = profile.get('url')
            
            janrain('map', identifier=profile['identifier'], primaryKey=u.id) # Let janrain know this users primary key id, this is needed for agrigation posts

            # Future addition and enhancements
            #   with janrain we could get a list of friends/contnact and automatically follow them?
            #   Could we leverage twitter/facebook OAuth token?
            # Reference - https://rpxnow.com/docs#api_auth_info
            
            redirect(url(controller='register', action='new_user', id=u.id))
            

        # If not authenticated or any janrain info then error
        flash_message(_('Unable to authenticate user'))
        return redirect_to_referer()
