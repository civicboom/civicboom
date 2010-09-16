from civicboom.tests import *

class TestUserProfileController(TestController):

    def test_index_not_logged_in(self):
        self.log_out()
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
        response = self.app.get(url(controller='profile', action='view', id='MrNotExists'), status=404)
        # FIXME: test

