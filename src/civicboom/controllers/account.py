from civicboom.lib.base import BaseController, render, request, url, abort, redirect, c, app_globals

from civicboom.lib.misc    import flash_message
from civicboom.lib.janrain import janrain
from civicboom.lib.misc    import dict_to_stringprint

import urllib

import logging
log = logging.getLogger(__name__)
user_log = logging.getLogger("user")

#signin_page = url_for(controller='account', action='signin')

class AccountController(BaseController):
    #-----------------------------------------------------------------------------
    # Signin and Signout
    #-----------------------------------------------------------------------------
    # Reference - "Definitive Guide to Pylons" (pg 439)
    # and http://pylonsbook.com/en/1.1/simplesite-tutorial-part-3.html#signing-in-and-signing-out

    def signin(self):
        if not request.environ.get('REMOTE_USER'):
            abort(401) #This triggers the AuthKit middleware into displaying the sign-in form
        else:
            #redirect(url(controller='misc', action='test'))
            user_log.info("logged in")
            return redirect(url('/'))

    def signout(self):
        flash_message("Successfully signed out!")
        user_log.info("logged out")
        return redirect('/')

    #-----------------------------------------------------------------------------
    # Janrain Test - http://www.janrain.com/products/engage
    #-----------------------------------------------------------------------------

    def signin_janrain(self):
    
        if request.environ['REQUEST_METHOD']!='POST':
            c.janrain_return_url = urllib.quote_plus(url.current(host=app_globals.site_host))
            return render("/web/account/signin_janrain.mako")

        auth_info = janrain('auth_info', token=request.POST.get('token'))
        
        if auth_info:

            identifier = profile['identifier'] # 'identifier' will always be in the payload this is the unique idenfifier that you use to sign the user in to your site
            
            # if extended = true in API call, these fields could be avalable
            # accessCredentials = profile['accessCredentials'] #OAuth tokens for facebook and twitter
            # merged_poco # portable contacts dictonary
            # friends     # list of friends
   
            profile = auth_info['profile']
            name            = profile.get('displayName')
            email           = profile.get('email')
            profile_pic_url = profile.get('photo')

            # actually sign the user in. this implementation depends highly on your platform, and is up to you.
            return "User: %s, %s, %s\n<br/>Identifyer:%s" % (name, email, profile_pic_url, identifier)

        return "error"