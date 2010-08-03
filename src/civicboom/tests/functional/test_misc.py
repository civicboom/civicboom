from civicboom.tests import *

class TestMiscController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='misc', action='index'))

    def test_about(self):
        response = self.app.get(url(controller='misc', action='about'))

    def test_titlepage(self):
        response = self.app.get(url(controller='misc', action='titlepage'))
