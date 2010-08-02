from civicboom.lib.base import BaseController, render, request, url, abort, redirect, c, app_globals, session, flash_message, redirect_to_referer

from civicboom.lib.authentication import get_user_from_openid_identifyer, get_user_and_check_password
from civicboom.lib.janrain import janrain
from civicboom.lib.misc import session_remove, session_get

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

    def signin(self):

        # If no POST display signin template
        if request.environ['REQUEST_METHOD']!='POST':
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

        # If user has existing account
        if c.logged_in_user:
            # Login
            user_log.info("logged in")               # Log user login
            session['user_id'] = c.logged_in_user.id # Set server session variable to user.id
            
            # Redirect them back to where they were going if a redirect was set
            login_redirect = session_get('login_redirect')
            if login_redirect:
                session_remove('login_redirect')
                return redirect(login_redirect)
            return redirect('/')
            
        # If no user found but we have Janrain auth_info display registration
        if c.auth_info:
            # Register or link new user

            # if extended = true in API call, these fields could be avalable
            # accessCredentials = profile['accessCredentials'] #OAuth tokens for facebook and twitter
            # merged_poco # portable contacts dictonary
            # friends     # list of friends
   
            profile = auth_info['profile']
            name            = profile.get('displayName')
            email           = profile.get('email')
            profile_pic_url = profile.get('photo')

            return "User: %s, %s, %s\n<br/>Identifyer:%s" % (name, email, profile_pic_url, identifier)

        # If not authenticated or any janrain info then error
        flash_message(_('Unable to authenticate user'))
        return redirect_to_referer()
