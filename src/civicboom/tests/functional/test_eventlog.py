from civicboom.tests import *

class TestEventlogController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='misc', action='fill_log'))
        response = self.app.get(url(controller='eventlog', action='index'))
        assert "debug" in response
        # Test response...
