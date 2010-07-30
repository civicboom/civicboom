from civicboom.tests import *

class TestUserProfileController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='user_profile', action='index'))
        # Test response...
