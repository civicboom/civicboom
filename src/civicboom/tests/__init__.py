"""Pylons application test package

This package assumes the Pylons environment is already loaded, such as
when this script is imported from the `nosetests --with-pylons=test.ini`
command.

This module initializes the application via ``websetup`` (`paster
setup-app`) and provides the base testing objects.
"""
from unittest import TestCase

from paste.deploy import loadapp
from paste.script.appinstall import SetupCommand
from pylons import url
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
           'getLastEmail', 'getNumEmails', 'emails']

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
            assert '_authentication_token' in response.session # If this failed the login was unsuccessful
            self.auth_token   = response.session['_authentication_token']
            self.logged_in_as = username

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

    def sign_up_as(self, username, password=u'password'):
        """
        A function that can be called from other automated tests to call the signup proccess and generate a new user
        """
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
        assert getNumEmails() == num_emails + 1
        email_response = getLastEmail()
        assert email_response.content_text
        
        # Check for link in email
        link = str(re.search(r'https?://(?:.*?)(/.*?)[\'"\s]', email_response.content_text+' ').group(1))
        assert 'hash' in link
            
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
        assert getNumEmails() == num_emails + 1
        
        self.log_in_as(username, password)
    
    def get_following_count(self):
        response      = self.app.get(url('member_action', action='following', id=self.logged_in_as, format='json'), status=200)
        response_json = json.loads(response.body)
        return len(response_json['data']['list'])
    
    def get_follower_count(self):
        response      = self.app.get(url('member_action', action='followers', id=self.logged_in_as, format='json'), status=200)
        response_json = json.loads(response.body)
        return len(response_json['data']['list'])
    
    def check_follow(self, following, followers, username='follow_test'):
        assert self.get_follower_count()  == followers
        assert self.get_following_count() == following
    
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
