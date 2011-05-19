from civicboom.tests import *

#from civicboom.lib.communication.email_log import getLastEmail, getNumEmails

#import re



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
        self.log_out()
        
        # Request new user email for user that already exisits - reject
        response = self.app.post(
            url(controller='register', action='email', format="json"),
            params={
                'username': u'unittest',
            },
            status=400,
        )
        
        response = self.app.post(
            url(controller='register', action='email', format="json"),
            params={
                'username': u'unittest2',
                'email'   : u'unittest@test.com'
            },
            status=400,
        )
        
        num_emails = getNumEmails()
        
        # Request new user email for new user
        response = self.app.post(
            url(controller='register', action='email', format="json"),
            params={
                'username': u'test_signup',
                'email'   : u'test@moose.com',
            },
        )
        
        # Get email generated by last event
        self.assertEqual(getNumEmails(), num_emails + 1)
        email_response = getLastEmail()
        self.assertTrue(email_response.content_text)
        
        # Check for link in email
        link = str(re.search(r'https?://(?:.*?)(/.*?)[\'"\s]', email_response.content_text+' ').group(1))
        self.assertIn('hash', link)
        
        # follow email link
        response = self.app.get(link)
        self.assertIn('password', response)
        self.assertIn('dob'     , response)
        self.assertIn('terms'   , response)
        
        # Fail validation
        response = self.app.post(
            link,
            params={
                'password'        : u'password',
                'password_confirm': u'password2', # Passwords dont match
                'dob'             : u'01-01-1980',
                'terms'           : u'checked'
            },
            status=400
        )
        
        response = self.app.post(
            link,
            params={
                'password'        : u'password',
                'password_confirm': u'password',
                'dob'             : u'2009-01-01', # Too young
                'terms'           : u'checked'
            },
            status=400
        )
        
        response = self.app.post(
            link,
            params={
                'password'        : u'password',
                'password_confirm': u'password',
                'dob'             : u'1980/01/01',
                                                   # No terms checked
            },
            status=400
        )
        
        num_emails = getNumEmails()
        response = self.app.post(
            link,
            params={
                'password'        : u'password',
                'password_confirm': u'password',
                'dob'             : u'1980-01-01',
                'terms'           : u'checked'
            },
        )
        self.assertEqual(getNumEmails(), num_emails + 1) # Check welcome email sent
        #email_response = getLastEmail()
        #self.assertIn('civicboom', email_response.content_text)
        
        self.log_in_as('test_signup', 'password')
        
        # Test lowercase normalisation
        self.log_in_as('TeSt_SiGnUp', 'password')

    #---------------------------------------------------------------------------
    # Signup & autofollow user
    #---------------------------------------------------------------------------
    def test_signup_and_follow_default_user(self):
        self.log_out()
        
        # Fake config setting
        
        default_auto_follow = self.config_var('setting.username_to_auto_follow_on_signup')
        self.config_var('setting.username_to_auto_follow_on_signup', 'unittest')
        
        num_emails = getNumEmails()
        
        # Request new user email for new user
        response = self.app.post(
            url(controller='register', action='email', format="json"),
            params={
                'username': u'test_signup_follow',
                'email'   : u'signup_autofollow@moose.com',
            },
        )
        
        # 2 emails should be generated, the welcome! and the 'new_follower' email to unittest
        self.assertEqual(getNumEmails(), num_emails + 2)

        from civicboom.lib.database.get_cached import get_member
        get_member('test_signup_follow').delete()

        # Set back the config var so tests run after this are not affected
        self.config_var('setting.username_to_auto_follow_on_signup', default_auto_follow)