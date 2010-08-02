from civicboom.tests import *

class TestUserProfileController(TestController):

    def test_view(self):
        response = self.app.get(url(controller='user_profile', action='view', id='unittest'))
        assert "Mr U. Test (unittest)" in response

    def test_edit(self):
        response = self.app.get(url(controller='user_profile', action='edit', id='unittest'), status=401) # not logged in
