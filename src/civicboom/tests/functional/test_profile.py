from civicboom.tests import *

from nose.plugins.skip import SkipTest

class TestUserProfileController(TestController):

    def test_index_not_logged_in(self):
        self.log_out()
        response = self.app.get(url(controller='profile', action='index', format="json"), status=403)

    def test_index(self):
        response = self.app.get(url(controller='profile', action='index'))
        self.assertIn("Mr U. Test", response)

    def test_messages(self):
        response = self.app.get(url(controller='profile', action='index', format='json'))
        response_json = json.loads(response.body)
        for field in ['num_unread_messages', 'num_unread_notifications', 'last_message_timestamp', 'last_notification_timestamp']:
            self.assertIn(field, response_json['data'])
    
    def test_personas(self):
        response = self.app.get(url(controller='profile', action='index', format='json'))
        response_json = json.loads(response.body)
        self.assertIn('count', response_json['data']['groups'])
