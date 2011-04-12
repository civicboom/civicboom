from civicboom.tests import *
from base64 import b64encode, b64decode
import warnings


class TestSettingsController(TestController):
    
#    def test_index(self):
#        self.log_in_as('unittest')
#        response = self.app.get(url('settings'))

    def test_invalid_user(self):
        self.log_in_as('unittest')
        # Fail validation
        response = self.app.post(
            url('setting',id="thisuserdoesnotexist"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'panel'               : u'general',
                'password_current'    : u'password',
                'password_new'        : u'password1',
                'password_new_confirm': u'password2', # Passwords dont match
            },
            status=404
        )
        
    def test_invalid_user(self):
        self.log_in_as('unittest')
        # Fail validation
        response = self.app.post(
            url('setting',id="unitfriend"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'panel'               : u'general',
                'password_current'    : u'password',
                'password_new'        : u'password1',
                'password_new_confirm': u'password2', # Passwords dont match
            },
            status=403
        )
        
    def test_password_change(self):
        self.log_in_as('unittest')
        # Fail validation
        response = self.app.post(
            url('setting',id="me"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'panel'               : u'general',
                'password_current'    : u'password',
                'password_new'        : u'password1',
                'password_new_confirm': u'password2', # Passwords dont match
            },
            status=400
        )
        self.assertIn('Fields do not match', response)
        #Change password
        response = self.app.post(
            url('setting',id="me"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'panel'               : u'general',
                'password_current'    : u'password',
                'password_new'        : u'password2',
                'password_new_confirm': u'password2', # Passwords match
            },
        )
        self.log_in_as('unittest', password='password2')
        # Change password back!
        response = self.app.post(
            url('setting',id="me"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'panel'               : u'general',
                'password_current'    : u'password2',
                'password_new'        : u'password',
                'password_new_confirm': u'password', # Passwords match
            },
        )
        self.log_in_as('unittest')
    
    def test_change_email(self):
        self.log_in_as('unittest')
        num_emails = getNumEmails()
        #Get current email address
        response = self.app.get(url('settings', id='me', format='json')) #url(controller='settings', action="show", format='json')
        response_json = json.loads(response.body)
        self.email_address = response_json['data']['settings']['email']
        self.assertTrue(self.email_address)
        
        #Change email address no AT
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'email'    : u'test',
            },
            status=400
        )
        self.assertIn('An email address must contain a single @', response)
        
#        BROKEN: domain check not active in test mode!
#        #Change email address invalid domain
#        response = self.app.post(
#            url(controller='settings', action='update'),
#            params={
#                '_method': 'PUT',
#                '_authentication_token': self.auth_token,
#                'email'    : u'test@idonotexistontheinternets.io',
#            },
#            status=400
#        )
#        self.assertIn('The domain of the email address does not exist', response)

#        BROKEN: allows blank email addresses
        #Change email address invalid blank
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'email'    : u'',
            },
            status=400
        )
        #Problem, can change to blank, not verified correctly!
        
        #Change email address
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'email'    : u'test@example.com',
            },
            status=200
        )
        #Should send an email
        self.assertEqual(getNumEmails(), num_emails + 1)
        email_response = getLastEmail()
        #Email should be sent to new address
        self.assertIn('test@example.com', email_response.email_to)
        link = str(re.search(r'https?://(?:.*?)(/.*?)[\'"\s]', email_response.content_text+' ').group(1))
        self.assertIn('hash', link)
        response = self.app.get(link,status=302)
        #Check changed
        response = self.app.get(url('settings', id='me', format='json'))
        response_json = json.loads(response.body)
        self.assertIn('test@example.com', response) # Email address has changed
        
        num_emails = getNumEmails()
        
        #Change email back
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'email'    : self.email_address,
            },
            status=200
        )
        #Should send an email
        self.assertEqual(getNumEmails(), num_emails + 1)
        email_response = getLastEmail()
        #Email should be sent to new address
        self.assertIn(self.email_address, email_response.email_to)
        link = str(re.search(r'https?://(?:.*?)(/.*?)[\'"\s]', email_response.content_text+' ').group(1))
        self.assertIn('hash', link)
        response = self.app.get(link,status=302)
        #Check changed
        response = self.app.get(url('settings', id='me', format='json'))
        response_json = json.loads(response.body)
        self.assertIn(self.email_address, response) # Email address has changed
        
    def test_change_avatar(self):
        self.png1x1 = b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAAAXNSR0IArs4c6QAAAApJREFUCNdj+AcAAQAA/8I+2MAAAAAASUVORK5CYII=')
        self.log_in_as('unittest')
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
            },
            upload_files = [("avatar", "1x1.png", self.png1x1)],
            status=200
        )
        
    def test_change_description(self):
        self.log_in_as('unittest')
        #Get current
        response = self.app.get(url('settings', id="me", format='json'))
        response_json = json.loads(response.body)
        self.old_description = response_json['data']['settings']['description']
        self.assertTrue(self.old_description)
        #Change
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'description'    : 'This is a new test description, with some sort of weird dot: \xe2\x80\xa2',
            },
            status=200
        )
        #Check changed
        response = self.app.get(url('settings', id="me", format='json'))
        response_json = json.loads(response.body)
        self.assertNotEqual(self.old_description, response_json['data']['settings']['description'])
        #Change
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'description'    : self.old_description,
            },
            status=200
        )

    def test_invalid_location(self):
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'location_home_name': 'blah',
                'location_home'    : 'biscuits',
            },
            status=400
        )

    def test_change_location(self):
        from random import random
        self.log_in_as('unittest')
        #Get current
        response = self.app.get(url('settings', id="me", panel="location", format='json'))
        response_json = json.loads(response.body)
        self.old_location = response_json['data']['settings']['location_home']
        self.assertTrue(self.old_location)
        #Change
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'location_home_name': 'blah',
                'location_home'    : '%f %f' % (1+random(), 51+random()), # non-deterministic testing, yay
            },
            status=200
        )
        #Check changed
        response = self.app.get(url('settings', id="me", panel="location", format='json'))
        response_json = json.loads(response.body)
        self.assertNotEqual(self.old_location, response_json['data']['settings']['location_home'])
        #Change
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'location_home'    : self.old_location,
            },
            status=200
        )
        
    def test_change_name(self):
        self.log_in_as('unittest')
        #Get current
        response = self.app.get(url('settings', id="me", format='json'))
        response_json = json.loads(response.body)
        self.old_name = response_json['data']['settings']['name']
        #Change
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'name'    : u'Testing User Testing User',
            },
            status=200
        )
        #Check changed
        response = self.app.get(url('settings', id="me", format='json'))
        response_json = json.loads(response.body)
        self.assertNotEqual(self.old_name, response_json['data']['settings']['name'])
        #Change
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'description'    : self.old_name,
            },
            status=200
        )
        
    def test_change_website(self):
        self.log_in_as('unittest')
        #Get current
        response = self.app.get(url('settings', id="me", format='json'))
        response_json = json.loads(response.body)
        self.old_website = response_json['data']['settings']['website']
        #Change incorrect url
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'website'    : u'mailto:test@example.com',
            },
            status=400
        )
        self.assertIn('That is not a valid URL', response)
        
        #Change
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'website'    : u'http://cb.example.com',
            },
            status=200
        )
        
        #Check changed
        response = self.app.get(url('settings', id="me", format='json'))
        response_json = json.loads(response.body)
        self.assertNotEqual(self.old_website, response_json['data']['settings']['website'])
        #Change
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'website'    : self.old_website,
            },
            status=200
        )
