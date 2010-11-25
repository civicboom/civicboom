from civicboom.tests import *

from civicboom.lib.communication.email_log import getLastEmail, getNumEmails

import re



class TestSignup(TestController):

    #---------------------------------------------------------------------------
    # Signup
    #---------------------------------------------------------------------------
    def test_signup(self):
        """
        request signup email
        follow link in email
        complete signup process
        logout
        login
        """
        #TODO: implement
        pass