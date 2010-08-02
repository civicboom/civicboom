from civicboom.tests import *

class TestContentController(TestController):

    def test_view(self):
        response = self.app.get(url(controller='content', action='view', id=1))
