from civicboom.tests import *

class TestMiscController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='misc', action='index'))

    def test_about(self):
        response = self.app.get(url(controller='misc', action='about'))

    def test_titlepage(self):
        response = self.app.get(url(controller='misc', action='titlepage'))

    def test_credits(self):
        response = self.app.get(url(controller='misc', action='credits'))

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


    def test_mobile_detection(self):
        # test non-mobile
        response = self.app.get(
            url(controller='misc', action='index'),
            extra_environ={'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; fi; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8'}
        )
        # FIXME: test environ['is_mobile']

        # test mobile type 1
        response = self.app.get(
            url(controller='misc', action='index'),
            extra_environ={'HTTP_USER_AGENT': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_1_2 like Mac OS X; fr-fr) AppleWebKit/528.18 (KHTML, like Gecko) Mobile/7D11'}
        )
        # FIXME: test environ['is_mobile']

        # test mobile type 2
        response = self.app.get(
            url(controller='misc', action='index'),
            extra_environ={'HTTP_USER_AGENT': 'w3c asdfasdf'} # tests first 4 characters
        )
        # FIXME: test environ['is_mobile']

        # test http_accept
        response = self.app.get(
            url(controller='misc', action='index'),
            extra_environ={
                'HTTP_USER_AGENT': 'asdfasdf', # http_accept isn't tested without user_agent...
                'HTTP_ACCEPT': 'application/vnd.wap.xhtml+xml'
            }
        )
        # FIXME: test environ['is_mobile']

