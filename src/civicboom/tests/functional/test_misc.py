from civicboom.tests import *

class TestMiscController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='misc', action='index'))

    def test_about(self):
        response = self.app.get(url(controller='misc', action='about'))

    def test_titlepage(self):
        response = self.app.get(url(controller='misc', action='titlepage'))

    def test_static(self):
        # test that static content is cachable
        response = self.app.get("/robots.txt")
        # FIXME: test that "Cache-Control: public" is set

    def test_georss(self):
        response = self.app.get(url(controller='misc', action='georss'))
        response = self.app.get(url(controller='misc', action='georss', feed='/search/content.xml'))
        response = self.app.get(url(controller='misc', action='georss', feed='invalid'))
        response = self.app.get(url(controller='misc', action='georss', location='0,0'))
        response = self.app.get(url(controller='misc', action='georss', location='invalid'))
