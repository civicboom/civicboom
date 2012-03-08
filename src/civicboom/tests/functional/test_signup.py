# -*- coding: utf-8 -*-

from civicboom.tests import *

#from civicboom.lib.communication.email_log import getLastEmail, getNumEmails

#import re


# See http://documentation.janrain.com/profiledata for more info
fake_janrain_return = json.dumps({
    u'profile': {
        u'preferredUsername': u'janrain_test',
        u'displayName'      : u'janrain_test',
        u'name'             : {
            u'givenName' : u'Janrain',
            u'formatted' : u'Janrain Test',
            u'familyName': u'Test'
        },
        u'providerName' : u'Google',
        u'googleUserId' : u'000000000000000000000',
        u'url'          : u'https://www.google.com/profiles/000000000000000000000',
        u'email'        : u'janrain_test@civicboom.com',
        #u'verifiedEmail': u'janrain_test@civicboom.com',
        u'identifier'   : u'https://www.google.com/profiles/000000000000000000000',
        u'primaryKey'   : u'janrain_test',
        u'photo'        : u'https://www.civicboom.com/images/logo.png',
        u'birthday'     : u'1980-01-01',
    },
    u'stat': u'ok',
})



class TestSignup(TestController):

    def setUp(self):
        pass # Dont log in by default


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
        
        # Request new user email for user that already exisits - reject
        response = self.app.post(
            url(controller='register', action='email', format="json"),
            params={
                'username': u'unittest', # reject existing username
            },
            status=400,
        )
        
        response = self.app.post(
            url(controller='register', action='email', format="json"),
            params={
                'username': u'unittest2',
                'email'   : u'test+unittest@civicboom.com' # reject existing email address
            },
            status=400,
        )
        
        num_emails = getNumEmails()
        
        # Request new user email for new user
        response = self.app.post(
            url(controller='register', action='email', format="json"),
            params={
                'username': u'test_signup',
                'email'   : u'test+test@civicboom.com',
            },
        )
        
        # Get email generated by last event
        self.assertEqual(getNumEmails(), num_emails + 1) # Follow email on signup
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
                'password_confirm': u'password',
                'dob'             : u'01-01-1980',
                'terms'           : u'checked',
                #'help_type'       : u'ind', # Must have a help_type
            },
            status=400
        )
        self.assertIn   ('help_type', response)

        response = self.app.post(
            link,
            params={
                'password'        : u'password',
                'password_confirm': u'password', 
                'dob'             : u'01-01-1980',
                'terms'           : u'checked',
                'help_type'       : u'individual', # Must have a help_type ind or org
            },
            status=400
        )
        self.assertIn   ('help_type', response)

        response = self.app.post(
            link,
            params={
                'password'        : 'ßßßßßßßß',
                'password_confirm': 'ßßßßßßßß', # Passwords should not contain entirely of a single repeated character
                'dob'             : u'01-01-1980',
                'terms'           : u'checked',
                'help_type'       : u'ind',
            },
            status=400
        )
        self.assertIn('repeated', response)
        
        response = self.app.post(
            link,
            params={
                'password'        : u'password',
                'password_confirm': u'password2', # Passwords dont match
                'dob'             : u'01-01-1980',
                'terms'           : u'checked',
                'help_type'       : u'ind',
            },
            status=400
        )
        self.assertNotIn('Invalid date'      , response)
        self.assertIn   ('do not match'      , response)
        
        response = self.app.post(
            link,
            params={
                'password'        : u'$password', # passwords should allow for non alpha newmeric characters
                'password_confirm': u'$password',
                'dob'             : u'2009-01-01', # Too young
                'terms'           : u'checked',
                'help_type'       : u'ind',
            },
            status=400
        )
        self.assertNotIn('Invalid date'   , response)
        self.assertIn   ('have to be over', response)
        
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
        self.assertNotIn('Invalid date'   , response)
        self.assertIn('agree to the terms', response)

        response = self.app.post(
            link,
            params={
                'password'        : u'password',
                'password_confirm': u'password',
                'dob'             : u'1980-01-01',
                'terms'           : u'checked',
                'help_type'       : u'ind',
            },
            status=400
        )
        self.assertIn('Please give us your full name', response)

        num_emails = getNumEmails()
        response = self.app.post(
            link,
            params={
                'password'        : 'passwordß', # AllanC - allow unicode passwords in signup
                'password_confirm': 'passwordß',
                'dob'             : u'1980-01-01',
                'name'            : u'This is my full name',
                'terms'           : u'checked',
                'help_type'       : u'ind',
            },
        )
        
        # Check redirect to 'how_to' after registration
        while response.status >= 300 and response.status <= 399:
            response_location = response.header_dict['location']
            response = response.follow()
        self.assertIn('how_to', response_location)
        
        self.assertEqual(getNumEmails(), num_emails + 2) # Check welcome email sent # and lizzies email for every member signup
        #email_response = getLastEmail()
        #self.assertIn('civicboom', email_response.content_text)
        
        self.log_in_as('test_signup', 'passwordß')
        
        # Test lowercase normalisation
        self.log_in_as('TeSt_SiGnUp', 'passwordß')

    #---------------------------------------------------------------------------
    # Signup & autofollow user
    #---------------------------------------------------------------------------
    def test_signup_and_follow_default_user(self):

        default_auto_follow = self.config_var('setting.username_to_auto_follow_on_signup') # Remeber auto follow config var to reset at end of test
        
        # Fake config setting
        self.config_var('setting.username_to_auto_follow_on_signup', 'puppy') # Change auto follow on signup config var
        
        # Setup unitfriend to allow mutual registration follows
        self.log_in_as('unitfriend')
        response = self.app.post(
            url('setting',id="me",format="json"),
            params={
                '_method': 'put',
                '_authentication_token': self.auth_token,
                'allow_registration_follows' : 'true',
            },
            status=200
        )
        self.log_out()
        
        
        # Request new user email for new user
        response = self.app.post(
            url(controller='register', action='email', format="json"),
            params={
                'username'     : u'test_signup_follow',
                'email'        : u'test+signup_autofollow@civicboom.com',
                'follow'       : '  bunny,  kitten   ',
                'follow_mutual': 'unitfriend',
            },
        )
        
        # Check for link in email
        link = str(re.search(r'https?://(?:.*?)(/.*?)[\'"\s]', getLastEmail().content_text+' ').group(1))
        self.assertIn('hash', link)
        
        num_notifications = self.getNumNotificationsInDB()
        # Complete the registration process - this will trigger the new_follower noifications
        response = self.app.post(
            link,
            params={
                'password'        : 'password',
                'password_confirm': 'password',
                'dob'             : u'1980-01-01',
                'name'            : u'This is my full name',
                'terms'           : u'checked',
                'help_type'       : u'ind',
            },
        )
        
        self.assertEquals(self.getNumNotificationsInDB(), num_notifications + 5) # test_signup_follow has - 4 new_follower notifications. unitfriend has 1 new_follower notification
        # Check contents of notifcications generated
        notifications = self.getNotificationsFromDB(5)
        notification_targets  = [n.target_id for n in notifications]
        notification_subjects = [n.subject   for n in notifications]
        for member in ['puppy','bunny','kitten','unitfriend','test_signup_follow']:
            self.assertIn(member, notification_targets)
        for subject in notification_subjects:
            self.assertEquals('new follower', subject)
        
        # Cleanup
        self.delete_member('test_signup_follow')
        
        # Set back the config var so tests run after this are not affected
        self.config_var('setting.username_to_auto_follow_on_signup', default_auto_follow)
        self.config_var('setting.username_to_auto_follow_on_signup', '')


    #---------------------------------------------------------------------------
    # Signup with the same unverifyed email address multiple times
    #---------------------------------------------------------------------------
    def test_signup_multiple_unveifyed(self):
        """
        Signup with the same unverifyed email address multiple times
        This should not create new users but send the email again
        """
        from civicboom.model import User
        from civicboom.model.meta import Session
        
        num_users  = Session.query(User).count()
        num_emails = getNumEmails()
        response = self.app.post(
            url(controller='register', action='email'),
            params={
                'username': u'test_signup_multiple',
                'email'   : u'test+multiple@civicboom.com',
            },
        )
        self.assertEqual(Session.query(User).count(), num_users  + 1)
        self.assertEqual(getNumEmails()             , num_emails + 1)
        
        num_users  = Session.query(User).count()
        num_emails = getNumEmails()
        response = self.app.post(
            url(controller='register', action='email'),
            params={
                'username': u'test_signup_multiple_again', # Username should be updated
                'email'   : u'test+multiple@civicboom.com',
            },
        )
        self.assertEqual(Session.query(User).count(), num_users     ) # No new user should be generated
        self.assertEqual(getNumEmails()             , num_emails + 1) # signup email should be resent
        self.assertIsNone   (Session.query(User).get('test_signup_multiple')      ) # Check old user not exists and has been renamed
        self.assertIsNotNone(Session.query(User).get('test_signup_multiple_again')) # Check user exists
        
        # Cleanup
        self.delete_member('test_signup_multiple_again')

    #---------------------------------------------------------------------------
    # Signup with Janrain
    #---------------------------------------------------------------------------
    def test_signup_janrain(self):
        
        response = self.app.post(
            url(controller='account', action='signin'),
            params={
                'token'              :'00000000000000000000000000000000',
                'fake_janrain_return': fake_janrain_return,
            },
        )
        while response.status >= 300 and response.status <= 399:
            response_location = response.header_dict['location']
            response = response.follow()
        self.assertIn('id="reg_form"', response.body) # Check that we have arrived at the registration page
        
        # Complete the registration
        response = self.app.post(
            response_location,
            params={
                'name'            : u'Janrain Test Display Name', # This is automatically filled in on the regisration form
                'terms'           : u'checked',
                'help_type'       : u'ind',
            },
        )
        
        # Logout
        self.log_out()
        
        # Attempt Login
        response = self.app.post(
            url(controller='account', action='signin'),
            params={
                'token'              :'00000000000000000000000000000000',
                'fake_janrain_return': fake_janrain_return,
            },
        )
        # Check redirect to profile
        while response.status >= 300 and response.status <= 399:
            response_location = response.header_dict['location']
            response = response.follow()
        self.assertIn('profile'                  , response_location)
        self.assertIn('Janrain Test Display Name', response.body    ) # Check that we have arrived at profile page. Should have display name
        
        self.delete_member('janrain_test')


    #---------------------------------------------------------------------------
    # Pending User
    #---------------------------------------------------------------------------
    def test_pending_user(self):
        """
        When a user has a member record but has not completed registration
        If that user access's most pages they will be given a "complete registration message"
        This happens under multiple formats
        """
        response = self.app.post(
            url(controller='account', action='signin'),
            params={
                'token'              :'00000000000000000000000000000000',
                'fake_janrain_return': fake_janrain_return,
            },
        )
        
        response = self.app.get(url(controller='profile', action='index'                    ), status=302)
        response = self.app.get(url(controller='profile', action='index'     , format='json'), status=403)
        #response_json = json.loads(response.body)
        #self.assertIn(response_json['message'], 'pending')
        
        response = self.app.get(url(controller='misc'   , action='opensearch', format='xml' ), status=200)

        self.delete_member('janrain_test')