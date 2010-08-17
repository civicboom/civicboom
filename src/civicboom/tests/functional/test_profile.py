from civicboom.tests import *

class TestUserProfileController(TestController):

    def test_index_not_logged_in(self):
        response = self.app.get(url(controller='profile', action='index'))
        # FIXME: test that we get a login page

    def test_view(self):
        response = self.app.get(url(controller='profile', action='view', id='unittest'))
        assert "Mr U. Test (unittest)" in response

    def test_bad_profile_view(self):
        # test for a sensible error when accessing a non-existent profile
        response = self.app.get(url(controller='profile', action='view', id='MrNotExists'))
        # FIXME: test

