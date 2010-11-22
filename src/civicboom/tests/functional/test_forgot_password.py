from civicboom.tests import *

from civicboom.lib.communication.email_log import getLastEmail, getNumEmails

import json
import datetime



class TestForgotPasswordController(TestController):

    #---------------------------------------------------------------------------
    # Forgot Password Flow
    #---------------------------------------------------------------------------
    def test_open_assignment(self):
        """
        request email
        follow email link
        fail password validation
        set password
        attempt login with new password
        """
        
        # Check for users that don't exisit
        response = self.app.post(
            url(controller='account', action='forgot_password', format='json'),
            params={
                #'_authentication_token': self.auth_token,
                'username': u'not.real.user',
            },
            status=404
        )
        
        response = self.app.post(
            url(controller='account', action='forgot_password', format='json'),
            params={
                #'_authentication_token': self.auth_token,
                'email': u'not.real.user@civicboom.com',
            },
            status=404
        )
        
        # Request forgotten password email
        
        num_emails = getNumEmails()
        
        response = self.app.post(
            url(controller='account', action='forgot_password', format='json'),
            params={
                #'_authentication_token': self.auth_token,
                'username': u'unittest',
            },
            status=200
        )
        
        assert getNumEmails() == num_emails + 1
        email_response = getLastEmail()
        
        # Check for link in email
        
        # search in email_response.content_text for link (use regex)
        # follow link