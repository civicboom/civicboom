from civicboom.lib.base import BaseController, render, request, url, abort, redirect

from civicboom.lib.misc import flash_message

import logging
log = logging.getLogger(__name__)

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
            return redirect(url('/'))

    def signout(self):
        flash_message("Successfully signed out!")
        return redirect('/')
