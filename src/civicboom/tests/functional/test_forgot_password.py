from civicboom.tests import *

from civicboom.lib.communication.email_log import getLastEmail, getNumEmails

#import re



class TestForgotPasswordController(TestController):

    #---------------------------------------------------------------------------
    # Forgot Password Flow
    #---------------------------------------------------------------------------
    def test_forgot_password(self):
        """
        request email
        follow email link
        fail password validation
        set password
        attempt login with new password
        logout
        revert password back to normal for other tests
        """
        
        self.log_out()
        
        # Check for users that don't exisit
        response = self.app.post(
            url(controller='account', action='forgot_password'), #, format='json'
            params={
                #'_authentication_token': self.auth_token,
                'username': u'not.real.user',
            },
            status=404
        )
        
        response = self.app.post(
            url(controller='account', action='forgot_password'), #, format='json'
            params={
                #'_authentication_token': self.auth_token,
                'email': u'not.real.user@civicboom.com',
            },
            status=404
        )
        
        # Request forgotten password email - with email address
        num_emails = getNumEmails()
        response = self.app.post(
            url(controller='account', action='forgot_password'), #, format='json'
            params={
                #'_authentication_token': self.auth_token,
                'username': u'test+unittest@civicboom.com',
            }
        )
        self.assertEqual(getNumEmails(), num_emails + 1)
        
        # Request forgotten password email - with username
        num_emails = getNumEmails()
        response = self.app.post(
            url(controller='account', action='forgot_password'), #, format='json'
            params={
                #'_authentication_token': self.auth_token,
                'username': u'unittest',
            }
        )
        
        # Get email generated by last event
        self.assertEqual(getNumEmails(), num_emails + 1)
        email_response = getLastEmail()
        self.assertTrue(email_response.content_text)
        
        # Check for link in email
        # AllanC: annoyed here .. firstly a URL cant be unicode so we need the str()
        #         secondly I cant detect the end of string with \b or ' or " so I add a hack space to the end so \s triggers (\b is apparently a backspace)
        link = str(re.search(r'https?://(?:.*?)(/.*?)[\'"\s]', email_response.content_text+' ').group(1))
        self.assertIn('hash', link)
        
        # follow email link
        response = self.app.get(link)
        self.assertIn('password_new', response)
        
        # try and set invalid password
        response = self.app.post(
            link,
            params={
                'password_new'        : u'hello',
                'password_new_confirm': u'hello2',
            },
            status=400
        )
        
        response = self.app.post(
            link,
            params={
            },
            status=400
        )
        
        response = self.app.post(
            link,
            params={
                'password_new'        : u'hello',
                'password_new_confirm': u'hello',
            }
        )
        
        self.log_in_as('unittest', password='hello')
        
        # Set password back to 'password' for the remaining unit tests
        # (no need to self.assertIn(and perform deep tests as these are checked earlyer on, the flow))
        self.log_out()
        response = self.app.post(
            url(controller='account', action='forgot_password', format='json'),
            params={
                'username': u'unittest',
            }
        )
        email_response = getLastEmail()
        link           = str(re.search(r'https?://(?:.*?)(/.*?)[\'"\s]', email_response.content_text+' ').group(1))
        response = self.app.post(
            link,
            params={
                'password_new'        : u'password',
                'password_new_confirm': u'password',
            }
        )
        self.log_in_as('unittest')


    #---------------------------------------------------------------------------
    # Forgot Password Redirect + flash message
    #---------------------------------------------------------------------------
    def test_forgot_password_redirect_message(self):
        """
        when requesting password the .redirect format is used. Check the flash message has the appropriate details
        """
        self.log_out()
        
        response = self.app.post(
            url(controller='account', action='forgot_password', format='redirect'),
            params={
                'username': u'unittest',
            },
            extra_environ={'HTTP_REFERER': url(controller='account', action='signin', qualified=True)}
        )
        while response.status >= 300 and response.status <= 399:
            response_location = response.header_dict['location']
            response = response.follow()
        self.assertIn('Password reminder sent to unittest', response.body)
