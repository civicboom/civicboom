from civicboom.tests import *


class TestUserProfileController(TestController):

    def test_index_not_logged_in(self):
        self.log_out()
        response = self.app.get(url(controller='profile', action='index', format="json"), status=403)

    def test_index(self):
        response = self.app.get(url(controller='profile', action='index'))
        self.assertIn("Mr U. Test", response)
