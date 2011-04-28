"""Pylons application test package

This package assumes the Pylons environment is already loaded, such as
when this script is imported from the `nosetests --with-pylons=test.ini`
command.

This module initializes the application via ``websetup`` (`paster
setup-app`) and provides the base testing objects.
"""
from unittest2 import TestCase

from paste.deploy import loadapp
from paste.script.appinstall import SetupCommand
from pylons import url
#from pylons import url as url_pylons
#from civicboom.lib.web import url
from routes.util import URLGenerator

# XXX: Paste's TestApp supports app.delete() with params
#from webtest import TestApp
from paste.fixture import TestApp
from civicboom.lib import worker

from civicboom.lib.communication.email_log import getLastEmail, getNumEmails, emails
import re
import json


import pylons.test

__all__ = ['environ', 'url', 'TestController',
           # Email Log
           'getLastEmail', 'getNumEmails', 'emails',
           # libs
           'json', 're'
           ]

# Invoke websetup with the current config file
SetupCommand('setup-app').run([pylons.test.pylonsapp.config['__file__']])


environ = {}


class TestController(TestCase):

    logged_in_as = None
    auth_token   = None

    def __init__(self, *args, **kwargs):
        wsgiapp = pylons.test.pylonsapp
        config = wsgiapp.config
        self.app = TestApp(wsgiapp, extra_environ={'REMOTE_ADDR': '0.0.0.0'})
        url._push_object(URLGenerator(config['routes.map'], environ))
        TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        # log in by default
        self.log_in()

    def tearDown(self):
        # wait for the worker to finish its work before reporting "test passed"
        worker.stop_worker()

    #---------------------------------------------------------------------------
    # Common functions for all test
    #---------------------------------------------------------------------------

    def config_var(self, key, value=None):
        """
        Used to get and set config vars from automated tests
        """
        response = self.app.get(
            url(controller='test', action='config_var'),
            params={
                'key'  : key   ,
                'value': value ,
            },
            status=200
        )
        return json.loads(response.body)[key]

    def log_in(self):
        self.log_in_as('unittest')

    def log_in_as(self, username, password='password'):
        if self.logged_in_as != username:
            self.log_out()
            response = self.app.post(
                url(controller='account', action='signin'),
                extra_environ={'HTTP_X_URL_SCHEME': 'https'},
                params={
                    'username': username ,
                    'password': password ,
                }
            )
            response = self.app.get(url(controller='profile', action='index')) # get an auth token
            self.assertIn('_authentication_token', response.session) # If this failed the login was unsuccessful
            self.auth_token   = response.session['_authentication_token']
            self.logged_in_as = username
            self.logged_in_password = password

    def log_out(self):
        if self.logged_in_as:
            response = self.app.post(
                url(controller='account', action='signout'),
                extra_environ={'HTTP_X_URL_SCHEME': 'https'},
                params={
                    '_authentication_token': self.auth_token
                }
            )
            self.auth_token   = None
            self.logged_in_as = None
        self.app.reset()

    def set_account_type(account_type):
        # AllanC TODO - do somthing with account_type var
        response = self.app.get(url(controller='test', action='set_account_type', id=self.logged_in_as, account_type=account_type))
        self.assertIn('ok', response.body)

    def set_persona(self, username_group):
        response = self.app.post(
            url(controller='account', action='set_persona', id=username_group, format='json'),
            params={
                '_authentication_token': self.auth_token,
            },
            status=200
        )
        response_json = json.loads(response.body)
        self.assertEqual(response_json['status'], 'ok')

    def join(self, username_group):
        response = self.app.post(
            url('group_action', action='join', id=username_group, format='json') ,
            params={
                '_authentication_token': self.auth_token   ,
                #'member'               : self.logged_in_as , #AllanC - why was this here?
            },
            status=200,
        )
        #self.assertIn('request', response) # successful "join request" in response


    def sign_up_as(self, username, password=u'password'):
        """
        A function that can be called from other automated tests to call the signup proccess and generate a new user
        """
        self.log_out()
        num_emails = getNumEmails()
        
        # Request new user email for new user
        response = self.app.post(
            url(controller='register', action='email', format="json"),
            params={
                'username': username,
                'email'   : username+'@moose.com',
            },
        )
        
        # Get email generated by last event
        self.assertEqual(getNumEmails(), num_emails + 1)
        email_response = getLastEmail()
        self.assertGreater(len(email_response.content_text), 0)
        
        # Check for link in email
        link = str(re.search(r'https?://(?:.*?)(/.*?)[\'"\s]', email_response.content_text+' ').group(1))
        self.assertIn('hash', link)
            
        num_emails = getNumEmails()
        response = self.app.post(
            link,
            params={
                'password'        : password,
                'password_confirm': password,
                'dob'             : u'1/1/1980',
                'terms'           : u'checked'
            },
        )
        self.assertEqual(getNumEmails(), num_emails + 1)
        
        self.log_in_as(username, password)
    
    def create_content(self, title=u'Test', content=u'Test', type='article', **kwargs):
        params={
            '_authentication_token': self.auth_token,
            'title'         : title      ,
            'content'       : content    ,
            'type'          : type       ,
            #'submit_publish': u'publish' , # publish needs to be remove from API
        }
        params.update(kwargs)
        
        response = self.app.post(
            url('contents', format='json') ,
            params = params ,
            status = 201 ,
        )
        response_json = json.loads(response.body)
        content_id = int(response_json['data']['id'])
        self.assertGreater(content_id, 0)
        return content_id

    def delete_content(self, id):
        response = self.app.delete(
            url('content', id=id, format="json"),
            params={'_authentication_token': self.auth_token,},
            status=200
        )


    def follow(self, username):
        response = self.app.post(
            url('member_action', action='follow', id=username, format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=200
        )
    
    def unfollow(self, username):
        response = self.app.post(
            url('member_action', action='unfollow', id=username, format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=200
        )

    def follower_trust(self, username):
        response = self.app.post(
            url('member_action', action='follower_trust', id=username, format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=200
        )
        response = self.app.post(
            url('member_action', action='follower_trust', id=username, format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=400
        )
        
    def follower_distrust(self, username):
        response = self.app.post(
            url('member_action', action='follower_distrust', id=username, format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=200
        )
        response = self.app.post(
            url('member_action', action='follower_distrust', id=username, format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=400
        )

    def follower_invite_trusted(self, username):
        response = self.app.post(
            url('member_action', action='follower_invite_trusted', id=username, format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=200
        )

    def send_member_message(self, username, subject, content):
        response = self.app.post(
            url('messages', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'target' : username,
                'subject': subject ,
                'content': content ,
            },
            status=201
        )
        message_id_list = json.loads(response.body)['data']['id']
        # AllanC - the id feild now returns a list of all messages created .. is this needed?
        if len(message_id_list)==1:
            return message_id_list[0]
        return message_id_list

    def boom_content(self, content_id):
        response = self.app.post(
            url('content_action', action='boom', id=content_id, format='json'),
            params={
                '_authentication_token': self.auth_token,
            },
            status=200
        )
        response_json = json.loads(response.body)
        assert response_json['status'] == 'ok'

    def comment(self, content_id, comment='comment'):
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                #'title': "A test comment by the test user",
                'type'     : 'comment'  ,
                'parent_id': content_id ,
                'content'  : comment    ,
            },
            status=201
        )
        return json.loads(response.body)["data"]["id"]

    def accept_assignment(self, id):
        response = self.app.post( # Accept assignment
            url('content_action', action='accept', id=id, format='json') ,
            params = {'_authentication_token': self.auth_token,} ,
            status = 200
        )
        self.assertIn('accepted', response)

    def withdraw_assignment(self, id):
        response = self.app.post(
            url('content_action', action='withdraw', id=id, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        self.assertIn('withdrawn', response)


    def getNumNotifications(self, username=None, password=None):
        if username:
            if self.logged_in_as != username:
                old_user = self.logged_in_as
                old_password = self.logged_in_password
                self.log_in_as(username, password)
        response = self.app.get(
            url('messages', format='json'),
            params={
                'list': 'notification',
            },
            status=200
        )
        response_json = json.loads(response.body)
        if username:
            if self.logged_in_as != old_user:
                self.log_in_as(old_user, old_password)
        return int(response_json['data']['list']['count'])
    
    def getLastNotification(self, username=None, password=None):
        if username:
            if self.logged_in_as != username:
                old_user = self.logged_in_as
                old_password = self.logged_in_password
                self.log_in_as(username, password)
        response = self.app.get(
            url('messages', format='json'),
            params={
                'list': 'notification',
            },
            status=200
        )
        response_json = json.loads(response.body)
        if username:
            if self.logged_in_as != old_user:
                self.log_in_as(old_user, old_password)
        return response_json['data']['list']['items'][0]
    
    def invite_user_to(self, type, id, user):
        # Test that we can access the invite page
        response = self.app.get(
            '/invite',
            params={
                '_authentication_token': self.auth_token,
                'invite': type,
                'id': id,
                'format': 'json',
            },
            status=200
        )
        # Test that searching for user that does not exist returns 0
        response = self.app.get(
            '/invite',
            params={
                '_authentication_token': self.auth_token,
                'invite': type,
                'id': id,
                'format': 'json',
                'search-name': user + 'does_not_exist_ever'
            },
            status=200
        )
        response_json = json.loads(response.body)
        self.assertEqual(response_json['data']['invite_list']['count'], 0)
        # Search for user and check we get less results
        response = self.app.post(
            '/invite',
            params={
                '_authentication_token': self.auth_token,
                'invite': type,
                'id': id,
                'format': 'json',
                'search-name': user
            },
            status=200
        )
        response_json = json.loads(response.body)
        self.assertGreaterEqual(response_json['data']['invite_list']['count'], 1)
        self.assertLess(response_json['data']['invite_list']['count'], 10)
        # Add user to invite list
        response = self.app.post(
            '/invite',
            params={
                '_authentication_token': self.auth_token,
                'invite': type,
                'id': id,
                'format': 'json',
                'search-name': user,
                'add-'+user: user
            },
            status=200
        )
        response_json = json.loads(response.body)
        self.assertIn(user, response_json['data']['invitee_list']['items']['0']['username'])
        # Generate extra invite parameters
        invitees = response_json['data']['invitee_list']['items']
        invitee_list = dict([('inv-'+key, invitees[key]['username']) for key in invitees.keys()])
        params = {
                '_authentication_token': self.auth_token,
                'invite': type,
                'id': id,
                'format': 'json',
                'search-name': user,
                'submit-invite': 'Invite',
            }
        params.update(invitee_list)
        response = self.app.post(
            '/invite',
            params=params,
            status=200
        )
        response_json = json.loads(response.body)
        self.assertEqual(response_json['data']['invitee_list']['count'], 0)
        self.assertEqual(response_json['status'], 'ok')
        
        # Repeat to check error double inviting
        response = self.app.post(
            '/invite',
            params=params,
            status=200
        )
        response_json = json.loads(response.body)
        self.assertEqual(response_json['data']['invitee_list']['count'], 1)
        self.assertEqual(len(response_json['data']['error-list']), 1)
        self.assertEqual(response_json['status'], 'ok')
