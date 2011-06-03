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
                'email'    : u'test+settings@civicboom.com',
            },
            status=200
        )
        #Should send an email
        self.assertEqual(getNumEmails(), num_emails + 1)
        email_response = getLastEmail()
        #Email should be sent to new address
        self.assertIn('test+settings@civicboom.com', email_response.email_to)
        link = str(re.search(r'https?://(?:.*?)(/.*?)[\'"\s]', email_response.content_text+' ').group(1))
        self.assertIn('hash', link)
        response = self.app.get(link,status=302)
        #Check changed
        response = self.app.get(url('settings', id='me', format='json'))
        response_json = json.loads(response.body)
        self.assertIn('test+settings@civicboom.com', response) # Email address has changed
        
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
        
    def test_change_password_unverified(self):
        self.log_in_as('unittest')
        num_emails = getNumEmails()
        #Get current email address
        response = self.app.get(url('settings', id='me', format='json')) #url(controller='settings', action="show", format='json')
        response_json = json.loads(response.body)
        self.email_address = response_json['data']['settings']['email']
        self.assertTrue(self.email_address)
        
        #Change email address
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'email'    : u'test+settings@civicboom.com',
            },
            status=200
        )
        #Should send an email
        self.assertEqual(getNumEmails(), num_emails + 1)
        email_response = getLastEmail()
        #Email should be sent to new address, get link
        self.assertIn('test+settings@civicboom.com', email_response.email_to)
        link = str(re.search(r'https?://(?:.*?)(/.*?)[\'"\s]', email_response.content_text+' ').group(1))
        
        response = self.app.get(url('settings', id='me', format='json')) #url(controller='settings', action="show", format='json')
        
        # Try changing password
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
            status=400
        )
        
        # Click link
        self.assertIn('hash', link)
        response = self.app.get(link,status=302)
        #Check changed
        response = self.app.get(url('settings', id='me', format='json'))
        response_json = json.loads(response.body)
        self.assertIn('test+settings@civicboom.com', response) # Email address has changed
        
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
                'website'    : u'mailto:test+settings@civicboom.com',
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
                'website'    : u'http://cb.shishnet.org',
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
        
    def test_501_actions(self):
        self.log_in_as('unittest')
        #Change incorrect url
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'DELETE',
                '_authentication_token': self.auth_token,
            },
            status=501
        )
        response = self.app.post(
            url('setting',id="new",format="frag"),
            params={
                '_method': 'NEW',
                '_authentication_token': self.auth_token,
            },
            status=501
        )
        response = self.app.post(
            url('setting',id="create",format="frag"),
            params={
                '_method': 'CREATE',
                '_authentication_token': self.auth_token,
            },
            status=501
        )
        
    def test_messages(self):
        self.log_in_as('unittest')
        #Get current
        response = self.app.get(url('settings', id="me", panel="messages", format='json'))
        response_json = json.loads(response.body)
        
        self.old_route = response_json['data']['settings']['route_assignment_interest_withdrawn']
        
        self.old_route = ",".join(list(self.old_route))
        
        for route in ['', 'e', 'n', 'n,e']:
            print '##', route
            response = self.app.post(
                url('setting',id="me",format="frag"),
                params={
                    '_method': 'PUT',
                    '_authentication_token': self.auth_token,
                    'panel': 'messages',
                    'route_assignment_interest_withdrawn': route,
                },
                status=200
            )
            response = self.app.get(url('settings', id="me", panel="messages", format='json'))
            response_json = json.loads(response.body)
            assert response_json['data']['settings']['route_assignment_interest_withdrawn'] == route.replace(',','')
            print self.old_route
        response = self.app.post(
            url('setting',id="me",format="frag"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'panel': 'messages',
                'route_assignment_interest_withdrawn': self.old_route,
            },
            status=200
        )
        
    def test_janrain_page(self):
        self.log_in_as('unittest')
        response = self.app.get(url('settings', id="me", panel="link_janrain", format='json'), status=200)
        
    def test_reflected_action(self):
        self.log_in_as('unittest')
        response = self.app.get(url('setting_action', id="me", action="general", format='json'), status=200)
        
    def test_set_popup_seen(self):
        response = self.app.post(
            url('setting',id="me",format="json"),
            params={
                '_method': 'PUT',
                '_authentication_token': self.auth_token,
                'panel': 'messages',
                'help_popup_created_user': 'True',
            },
            status=200
        )
        
    def test_group_settings(self):
        # general_group settings 200
        # "general" action 200
        # edit action 200 (panel & id)
        # config_var_list
        
        self.log_in_as('unittest')
        # Create Group
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username'     : 'test_settings_group',
                'name'         : 'Test group for settings unit tests' ,
                'description'  : 'This group should not be visible once the tests have completed because it will be removed' ,
                'default_role' : 'editor' ,
                'join_mode'    : 'invite_and_request' ,
                'member_visibility'         : 'public' , #required to test join request later
                'default_content_visibility': 'public' ,
            },
            status=201
        )
        self.set_persona('test_settings_group')
        # Check no janrain
        response = self.app.get(url('settings', id="me", panel="link_janrain", format='json'), status=404)
        # Check general settings are correct
        response = self.app.get(url('setting_action', id="me", action="general", format='json'), status=200)
        assert 'member_visibility' in response.body
        
        response = self.app.delete(
            url('group', id='test_settings_group', format='json'),
            params={
                '_authentication_token': self.auth_token
            },
            status=200
        )
        
#    def these_tests_are_old(self):
#        return """
#    def test_need_signin(self):
#        self.log_out()
#        response = self.app.get(url(controller='settings', action='general', id='unittest'), status=302)
#        response.follow()
#        self.assertIn("Sign in", response)
#
#    def test_general(self):
#        # test that with no ID, we get our own user page
#        response = self.app.get(url(controller='settings', action='general'))
#        self.assertIn("Display name", response)
#
#        response = self.app.post(
#            url(controller='settings', action='save_general', id='unittest'),
#            extra_environ={'HTTP_X_URL_SCHEME': 'https'},
#            params={
#                '_authentication_token': self.auth_token
#            }
#        )
#
#    def test_location(self):
#        # test that with no ID, we get our own user page
#        response = self.app.get(url(controller='settings', action='location'))
#        # FIXME: location page has no text to test for
#
#        # test for error
#        response = self.app.post(
#            url(controller='settings', action='save_location', id='unittest'),
#            params={
#                '_authentication_token': self.auth_token
#            }
#        )
#
#        # test guess-coordinates-by-name
#        response = self.app.post(
#            url(controller='settings', action='save_location', id='unittest'),
#            params={
#                '_authentication_token': self.auth_token,
#                'location_name': "Canterbury"
#            }
#        )
#
#        # test specified coordinates
#        response = self.app.post(
#            url(controller='settings', action='save_location', id='unittest'),
#            params={
#                '_authentication_token': self.auth_token,
#                'location_name': "Canterbury",
#                'location': '1.28,51.28'
#            }
#        )
#
#        # test specified coordinates with json output
#        response = self.app.post(
#            url(controller='settings', action='save_location', id='unittest', format='json'),
#            params={
#                '_authentication_token': self.auth_token,
#                'location_name': "Canterbury",
#                'location': '1.28,51.28'
#            }
#        )
#        # FIXME: test response["status"] == "ok"
#
#        # test bad location
#        response = self.app.post(
#            url(controller='settings', action='save_location', id='unittest', format='json'),
#            params={
#                '_authentication_token': self.auth_token,
#                'location_name': "Canterbury",
#                'location': 'arf arf I am a waffle'
#            }
#        )
#        # FIXME: test response["status"] == "error"
#
#    def test_messages(self):
#        # test that with no ID, we get our own user page
#        response = self.app.get(url(controller='settings', action='messages'))
#        self.assertIn("a test message", response)
#
#        response = self.app.post(
#            url(controller='settings', action='save_messages', id='unittest'),
#            params={
#                '_authentication_token': self.auth_token
#            }
#        )
#
#    def test_csrf(self):
#        # test that a setting without CSRF protection is rejected
#        response = self.app.post(
#            url(controller='settings', action='save_general'),
#            extra_environ={'HTTP_X_URL_SCHEME': 'https'},
#            params={
#                'email': u'waffle@iamtesting.com',
#            },
#            status = 403
#        )
#        self.assertIn("Hold it!", response)
#        # FIXME: test with CSRF protection passed
#        # FIXME: check for session['flash'] = "Settings changed: email"
#        # FIXME: check that we're redirected back to the settings page
#        # FIXME: check that the new settings appear on the new page
#
#    def test_edit_other_person_fails(self):
#        response = self.app.get(url(controller='settings', action='general'))
#
#        # test that we can't edit other people's profiles
#        # FIXME: for now, the 'id' paramater is ignored
#        #response = self.app.post(
#        #    url(controller='settings', action='save_general', id='unitfriend'),
#        #    params={'_authentication_token': self.auth_token},
#        #    status=403,
#        #)
#        # FIXME: test
#
#    def test_avatar():
#        upload avatar
#        upload invalid image
#        upload None
#        """
