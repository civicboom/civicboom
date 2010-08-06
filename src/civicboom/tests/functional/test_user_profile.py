from civicboom.tests import *

class TestUserProfileController(TestController):

    def test_view(self):
        response = self.app.get(url(controller='user_profile', action='view', id='unittest'))
        assert "Mr U. Test (unittest)" in response

    def test_bad_profile_view(self):
        # test for a sensible error when accessing a non-existent profile
        response = self.app.get(url(controller='user_profile', action='edit', id='MrNotExists'))
        # FIXME: test

