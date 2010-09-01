from civicboom.tests import *

class TestWidgetController(TestController):

    def test_signin(self):
        response = self.app.get(url(controller='widget', action='signin', widget_username="unittest"))

    def test_main(self):
        response = self.app.get(url(controller='widget', action='main', widget_username="unittest"))

    def test_assignment(self):
        response = self.app.get(url(controller='widget', action='assignment', id=8, widget_username="unittest"))

    def test_about(self):
        response = self.app.get(url(controller='widget', action='about', widget_username="unittest"))

    def test_get_widget(self):
        response = self.app.get(url(controller='widget', action='get_widget', widget_username="unittest"))

    def test_get_mobile(self):
        response = self.app.get(url(controller='widget', action='get_mobile', widget_username="unittest"))
