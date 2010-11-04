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

import pylons.test

__all__ = ['environ', 'url', 'TestController']

# Invoke websetup with the current config file
SetupCommand('setup-app').run([pylons.test.pylonsapp.config['__file__']])

# Setup base test data
# - AllanC - I dont know if this is the best place for it ... 
from civicboom.tests.init_base_data import init_base_data
init_base_data()

environ = {}

class TestController(TestCase):

    def __init__(self, *args, **kwargs):
        wsgiapp = pylons.test.pylonsapp
        config = wsgiapp.config
        self.app = TestApp(wsgiapp, extra_environ={'REMOTE_ADDR': '0.0.0.0'})
        url._push_object(URLGenerator(config['routes.map'], environ))
        TestCase.__init__(self, *args, **kwargs)

    def log_in(self):
        response = self.app.post(
            url(controller='account', action='signin'),
            extra_environ={'HTTP_X_URL_SCHEME': 'https'},
            params={
                'username': u'unittest',
                'password': u'password'
            }
        )
        response = self.app.get(url(controller='profile', action='index')) # get an auth token
        self.auth_token = response.session['_authentication_token']

    def log_out(self):
        response = self.app.post(
            url(controller='account', action='signout'),
            extra_environ={'HTTP_X_URL_SCHEME': 'https'},
            params={
                '_authentication_token': self.auth_token
            }
        )

    def setUp(self):
        # log in by default
        self.log_in()
