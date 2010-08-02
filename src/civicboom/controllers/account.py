from civicboom.lib.base import BaseController, render, request, url, abort, redirect, c, app_globals, session, flash_message

from civicboom.lib.authentication import get_user_from_openid_identifyer
from civicboom.lib.janrain import janrain
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
        if not request.environ.get('REMOTE_USER'):
            abort(401) #This triggers the AuthKit middleware into displaying the sign-in form
        else:
            #redirect(url(controller='misc', action='test'))
            user_log.info("logged in")
            return redirect(url('/'))

    def signout(self):
        """
        This function is pointed to from the ini config to trigger AuthKit to remove cookies
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
    
        if request.environ['REQUEST_METHOD']!='POST':
            c.janrain_return_url = urllib.quote_plus(url.current(host=app_globals.site_host))
            return render("/web/account/signin_janrain.mako")

        auth_info = janrain('auth_info', token=request.POST.get('token'))
        if auth_info:

            # Check user exisits
            c.logged_in_user = get_user_from_openid_identifyer(auth_info['profile']['identifier']) #Janrain guarntees the identifyer to be set

            # If user has existing account
            if c.logged_in_user:
                # Login
                user_log.info(c.logged_in_user)          # Log user login
                session['user_id'] = c.logged_in_user.id # Set server session variable to user.id
                
                # Redirect them back to where they were going
                login_redirect = session.get('login_redirect')
                if login_redirect:
                    # TODO: Check timestamp of login_redirect for expiry
                    del session['login_redirect']
                    return redirect(login_redirect)
                return redirect('/')
            else:
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

        flash_message(_('Unable to authenticate user'))
        return return redirect(url.current())