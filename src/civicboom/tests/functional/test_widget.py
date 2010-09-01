from civicboom.tests import *

class TestWidgetController(TestController):

    def test_signin(self):
        response = self.app.get(url(controller='widget', action='signin'))

    def test_main(self):
        response = self.app.get(url(controller='widget', action='main'))

    def test_assignment(self):
        response = self.app.get(url(controller='widget', action='assignment'))

    def test_about(self):
        response = self.app.get(url(controller='widget', action='about'))

    def test_get_widget(self):
        response = self.app.get(url(controller='widget', action='get_widget'))

    def test_get_mobile(self):
        response = self.app.get(url(controller='widget', action='get_mobile'))
