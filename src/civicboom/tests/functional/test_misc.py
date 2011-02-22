from civicboom.tests import *

class TestMiscController(TestController):

    # about is mapped to /about/*, and loads the template from /web/about/$id.mako

    def test_about(self):
        response = self.app.get(url(controller='misc', action='about', id='civicboom'))
        response = self.app.get(url(controller='misc', action='about', id='civicboom', format="rss"), status=404)
        response = self.app.get(url(controller='misc', action='about', id='waffles'), status=404)

    def test_help(self):
        response = self.app.get(url(controller='misc', action='help', id='profile'))
        response = self.app.get(url(controller='misc', action='help', id='profile', format="rss"), status=404)
        response = self.app.get(url(controller='misc', action='help', id='waffles'), status=404)


    # actual misc actions

    def test_titlepage(self):
        response = self.app.get(url(controller='misc', action='titlepage'))

    def test_titlepage_cache(self):
        self.log_out()
        response = self.app.get(url(controller='misc', action='titlepage'))
        # FIXME: test that generated-but-static content has cache headers set

    def test_upgrade_account(self):
        response = self.app.get(url(controller='misc', action='upgrade_account'))

    def test_georss(self):
        response = self.app.get(url(controller='misc', action='georss'))
        response = self.app.get(url(controller='misc', action='georss', feed='/search/content.xml'))
        response = self.app.get(url(controller='misc', action='georss', feed='invalid'))
        response = self.app.get(url(controller='misc', action='georss', location='0,0'))
        response = self.app.get(url(controller='misc', action='georss', location='invalid'))

    def test_echo(self):
        # FIXME: tests for GET and POST variables
        response = self.app.get(url(controller='misc', action='echo'))

    def test_stats(self):
        # FIXME: check JSON output
        response = self.app.get(url(controller='misc', action='stats'))

    def test_get_widget(self):
        # FIXME: check for things in response
        response = self.app.get(url(controller='misc', action='get_widget'))

    def test_upgrade_plans(self):
        # FIXME: check for things in response
        response = self.app.get(url(controller='misc', action='upgrade_plans'))

    def test_feedback(self):
        # FIXME: check POST
        response = self.app.get(url(controller='misc', action='feedback'))


    # other misc bits that aren't part of the misc controller, but are just misc

    def test_static(self):
        # test that static content is cachable
        response = self.app.get("/robots.txt")
        # FIXME: test that "Cache-Control: public" is set

    def test_semi_static(self):
        response = self.app.get("/misc/titlepage")
        # FIXME: test that "Cache-Control: public" is NOT set (for logged in user)
        self.log_out()
        response = self.app.get("/misc/titlepage")
        # FIXME: test that "Cache-Control: public" IS set for anonymous


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

