from civicboom.tests import TestController
from civicboom.lib.web import url


# inherit from TestController so that url() is set up
class TestRoutes(TestController):
    def test_proto(self):
        self.assertEqual(
            url('content', id=123, protocol="http"),
            "http://www.civicboom.com/contents/123"
        )
        self.assertEqual(
            url('content', id=123, protocol="https"),
            "https://www.civicboom.com/contents/123"
        )

    def test_subdomain(self):
        self.assertEqual(  # different subdomain = do have full URL
            url('content', id=123, sub_domain="m"),
            "https://m.civicboom.com/contents/123"
        )
        self.assertEqual(  # same subdomain = don't have full URL
            url('content', id=123, sub_domain="www"),
            "/contents/123"
        )
        self.assertEqual(  # unless qualified=True
            url('content', id=123, sub_domain="www", qualified=True),
            "https://www.civicboom.com/contents/123"
        )

    def test_host(self):
        # setting hosts is broken weirdly
        self.assertEqual(
            url('content', id=123, host="pie.civicboom.com"),
            "https://pie.civicboom.com/contents/123"
        )
        self.assertEqual(
            url('content', id=123, host="www.civicboom.com"),
            "https://www.civicboom.com/contents/123"
        )
        self.assertEqual(
            url('content', id=123, host="www.civicboom.com", qualified=True, sub_domain="www"),
            "https://www.civicboom.com/contents/123"
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

    def test_custom_routes(self):
        self.assertEqual(
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

