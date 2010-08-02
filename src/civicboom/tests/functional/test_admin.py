from civicboom.tests import *

class TestEventlogController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='test', action='fill_log'))
        response = self.app.get(url(controller='admin', action='event_log'))
        #assert "debug" in response /admin/event_log/ is redirected to /admin/event_log, *then* the page is visible
