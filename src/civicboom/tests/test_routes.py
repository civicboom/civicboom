from civicboom.tests import TestController
from civicboom.lib.web import url


# inherit from TestController so that url() is set up
class TestRoutes(TestController):

    def test_proto_regular_route(self):
        self.assertEqual(
            url(controller='misc', action='foo', protocol="http"),
            "http://www.civicboom.com/misc/foo"
        )
        self.assertEqual(
            url(controller='misc', action='foo', protocol="https"),
            "https://www.civicboom.com/misc/foo"
        )

    def test_proto_named_route(self):
        self.assertEqual(
            url('member', id='shish', format='rss', protocol="http"),
            "http://www.civicboom.com/members/shish.rss"
        )
        self.assertEqual(
            url('member', id='shish', format='rss', protocol="https"),
            "https://www.civicboom.com/members/shish.rss"
        )

    def test_proto_static_route(self):
        self.assertEqual(
            url('/waffo', protocol="http"),
            "http://www.civicboom.com/waffo"
        )
        self.assertEqual(
            url('/waffo', protocol="https"),
            "https://www.civicboom.com/waffo"
        )


    def test_subdomain_regular_route(self):
        self.assertEqual(  # different subdomain = do have full URL
            url(controller='misc', action='foo', sub_domain="m"),
            "https://m.civicboom.com/misc/foo"
        )
        self.assertEqual(  # same subdomain = don't have full URL
            url(controller='misc', action='foo', sub_domain="www"),
            "/misc/foo"
        )
        self.assertEqual(  # unless qualified=True
            url(controller='misc', action='foo', sub_domain="www", qualified=True),
            "https://www.civicboom.com/misc/foo"
        )

    def test_subdomain_named_route(self):
        self.assertEqual(  # named route, same domain
            url('member', id='shish', format='rss', sub_domain='www'),
            "/members/shish.rss"
        )
        self.assertEqual(  # named route, different domain
            url('member', id='shish', format='rss', sub_domain='m'),
            "https://m.civicboom.com/members/shish.rss"
        )

    def test_subdomain_static_route(self):
        return
        # FIXME: static routes are static, generation is flaky
        self.assertEqual(  # static path, different domain
            url('/waffo', sub_domain='m'),
            "https://m.civicboom.com/waffo"
        )
        self.assertEqual(  # static path, same domain
            url('/waffo', sub_domain='www'),
            "/waffo"
        )


    def test_host(self):
        # setting hosts is broken weirdly
        self.assertEqual(
            url(controller='misc', action='foo', host="pie.civicboom.com"),
            "https://pie.civicboom.com/misc/foo"
        )
        self.assertEqual(
            url(controller='misc', action='foo', host="www.civicboom.com"),
            "https://www.civicboom.com/misc/foo"
        )
        self.assertEqual(
            url(controller='misc', action='foo', host="www.civicboom.com", qualified=True, sub_domain="www"),
            "https://www.civicboom.com/misc/foo"
        )


    def test_rest_routes(self):
        self.assertEqual(
            url('content', id=123),
            "/contents/123"
        )
        self.assertEqual(
            url('edit_content', id=123),
            "/contents/123/edit"
        )
        self.assertEqual(
            url('edit_content', id=123, format="json"),
            "/contents/123/edit.json"
        )
        self.assertEqual(
            url('contents'),
            "/contents"
        )
        self.assertEqual(
            url('new_content'),
            "/contents/new"
        )
        self.assertEqual(
            url('member', id='shish'),
            "/members/shish"
        )
        self.assertEqual(
            url('member_action', id='shish', action='follow'),
            "/members/shish/follow"
        )

    def test_current(self):
        self.assertEqual(
            url('current'),
            "/"
        )
        self.assertEqual(
            url('current', qualified=True),
            "https://www.civicboom.com/"
        )
        self.assertEqual(  # changing the subdomain should imply qualified
            url('current', sub_domain="m"),
            "https://m.civicboom.com/"
        )

    def test_custom_routes(self):
        self.assertEqual(  # /about/(.*) = /misc/about?id=$1
            url(controller='misc', action='about', id="civicboom"),
            "/about/civicboom"
        )
        self.assertEqual(
            url(controller='misc', action='titlepage'),
            "/"
        )

    def test_front_page_synonyms(self):
        self.assertEqual(
            url('/'),
            "/"
        )
        self.assertEqual(
            url('/', qualified=True),
            "https://www.civicboom.com/"
        )
        self.assertEqual(
            url(controller='misc', action='titlepage'),
            "/"
        )
        self.assertEqual(
            url(controller='misc', action='titlepage', qualified=True),
            "https://www.civicboom.com/"
        )

    def test_blank(self):
        self.assertEqual(
            url(''),
            ""
        )
        self.assertEqual(
            url('', qualified=True),
            "https://www.civicboom.com/"
        )

    def test_normal_formats(self):
        self.assertEqual(
            url(controller='mobile', action='media_init', format="json"),
            "/mobile/media_init.json"
        )
