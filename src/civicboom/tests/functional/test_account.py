from civicboom.tests import *

class TestAccountController(TestController):
    def test_https_required(self):
        response = self.app.get(
            url(controller='account', action='signin'),
            extra_environ={'HTTP_X_URL_SCHEME': 'http'},
            status=302
        )
        response = self.app.get(
            url(controller='account', action='signin'),
            extra_environ={'HTTP_X_URL_SCHEME': 'https'},
            status=200
        )

    def test_good_signin(self):
        response = self.app.get(url(controller='account', action='signin'), status=302)
        # FIXME: fill in the form rather than handcrafting a POST?
        response = self.app.post(
            url(controller='account', action='signin'),
            extra_environ={'HTTP_X_URL_SCHEME': 'https'},
            params={
                'username': u'unittest',
                'password': u'password'
            }
        )

    def test_bad_signin(self):
        response = self.app.get(url(controller='account', action='signin'), status=302)
        # FIXME: fill in the form rather than handcrafting a POST?
        response = self.app.post(
            url(controller='account', action='signin'),
            extra_environ={'HTTP_X_URL_SCHEME': 'https'},
            params={
                'username': u'unittest',
                'password': u'asdfasdf'
            }
        )
        # FIXME: test this
