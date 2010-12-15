from civicboom.tests import *

class TestMiscController(TestController):

    def test_about(self):
        response = self.app.get(url(controller='misc', action='about'))

    def test_titlepage(self):
        response = self.app.get(url(controller='misc', action='titlepage'))

    def test_titlepage_cache(self):
        self.log_out()
        response = self.app.get(url(controller='misc', action='titlepage'))
        # FIXME: test that generated-but-static content has cache headers set

    def test_credits(self):
        response = self.app.get(url(controller='misc', action='credits'))

    def test_terms(self):
        response = self.app.get(url(controller='misc', action='terms'))

    def test_press(self):
        response = self.app.get(url(controller='misc', action='press'))

    def test_privacy(self):
        response = self.app.get(url(controller='misc', action='privacy'))

    def test_widget_preview(self):
        response = self.app.get(url(controller='misc', action='widget_preview'))

    def test_upgrade_account(self):
        response = self.app.get(url(controller='misc', action='upgrade_account'))

    def test_close_popup(self):
        response = self.app.get(url(controller='misc', action='close_popup'))
        assert "self.close()" in response

    def test_static(self):
        # test that static content is cachable
        response = self.app.get("/robots.txt")
        # FIXME: test that "Cache-Control: public" is set

    def test_semi_static(self):
        response = self.app.get("/misc/about")
        # FIXME: test that "Cache-Control: public" is NOT set (for logged in user)
        self.log_out()
        response = self.app.get("/misc/about")
        # FIXME: test that "Cache-Control: public" IS set for anonymous

    def test_georss(self):
        response = self.app.get(url(controller='misc', action='georss'))
        response = self.app.get(url(controller='misc', action='georss', feed='/search/content.xml'))
        response = self.app.get(url(controller='misc', action='georss', feed='invalid'))
        response = self.app.get(url(controller='misc', action='georss', location='0,0'))
        response = self.app.get(url(controller='misc', action='georss', location='invalid'))


    def test_mobile_detection(self):
        # test non-mobile
        response = self.app.get(
            url(controller='misc', action='titlepage'),
            extra_environ={'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; fi; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8'}
        )
        # FIXME: test environ['is_mobile']

        # test mobile type 1
        response = self.app.get(
            url(controller='misc', action='titlepage'),
            extra_environ={'HTTP_USER_AGENT': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_1_2 like Mac OS X; fr-fr) AppleWebKit/528.18 (KHTML, like Gecko) Mobile/7D11'}
        )
        # FIXME: test environ['is_mobile']

        # test mobile type 2
        response = self.app.get(
            url(controller='misc', action='titlepage'),
            extra_environ={'HTTP_USER_AGENT': 'w3c asdfasdf'} # tests first 4 characters
        )
        # FIXME: test environ['is_mobile']

        # test http_accept
        response = self.app.get(
            url(controller='misc', action='titlepage'),
            extra_environ={
                'HTTP_USER_AGENT': 'asdfasdf', # http_accept isn't tested without user_agent...
                'HTTP_ACCEPT': 'application/vnd.wap.xhtml+xml'
            }
        )
        # FIXME: test environ['is_mobile']

