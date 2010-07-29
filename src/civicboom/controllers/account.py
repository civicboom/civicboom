from civicboom.lib.base import BaseController, render, request, url, abort, redirect

from civicboom.lib.misc import flash_message

import urllib
import urllib2
import json

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

    def signin_janrain(self):
        if request.environ['REQUEST_METHOD']!='POST':
            return render("/web/account/signin_janrain.mako")
            
        token = request.POST.get('token')
        api_params = {'token': token,
                      'apiKey':'2f93094487a2e2af9f60725670e8cbd5bdc9fe8a',
                      'format': 'json',
                      }
        http_response  = urllib2.urlopen('https://rpxnow.com/api/v2/auth_info', urllib.urlencode(api_params))
        auth_info_json = http_response.read()
        auth_info      = json.loads(auth_info_json)
        
        if auth_info['stat'] != 'ok':
            print 'An error occured: ' + auth_info['err']['msg']
        else:
            profile = auth_info['profile']
   
            # 'identifier' will always be in the payload this is the unique idenfifier that you use to sign the user in to your site
            identifier = profile['identifier']
   
            # these fields MAY be in the profile, but are not guaranteed. it depends on the provider and their implementation.
            name            = profile.get('displayName')
            email           = profile.get('email')
            profile_pic_url = profile.get('photo')

            # actually sign the user in. this implementation depends highly on your platform, and is up to you.
            #sign_in_user(identifier, name, email, profile_pic_url)
            print "User: %s, %s, %s" % (name, email, profile_pic_url)