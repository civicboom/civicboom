from civicboom.tests import *

class TestUserProfileController(TestController):
    def setUp(self):
        response = self.app.post(
            url(controller='account', action='signin'),
            extra_environ={'HTTP_X_URL_SCHEME': 'https'},
            params={
                'username': u'unittest',
                'password': u'password'
            }
        )

    def test_index_not_logged_in(self):
        response = self.app.get(url(controller='account', action='signout'))
        response = self.app.get(url(controller='profile', action='index'), status=302)
        # FIXME: follow the redirect, then:
        # assert "Sign in" in response

    def test_index(self):
        response = self.app.get(url(controller='profile', action='index'))
        assert "Mr U. Test (unittest)" in response

    def test_view_default(self):
        response = self.app.get(url(controller='profile', action='view'))
        assert "Mr U. Test (unittest)" in response

    def test_view_self(self):
        response = self.app.get(url(controller='profile', action='view', id='unittest'))
        assert "Mr U. Test (unittest)" in response

    def test_view_other(self):
        response = self.app.get(url(controller='profile', action='view', id='unitfriend'))
        assert "(unitfriend)" in response

    def test_bad_profile_view(self):
        # test for a sensible error when accessing a non-existent profile
        response = self.app.get(url(controller='profile', action='view', id='MrNotExists'))
        # FIXME: test

