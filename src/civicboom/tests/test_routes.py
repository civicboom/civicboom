from civicboom.tests import TestController
from civicboom.lib.web import url


# inherit from TestController so that url() is set up
class TestRoutes(TestController):
    def test_proto(self):
        self.assertEqual(
            url(protocol="http", controller='contents', action='show', id=123),
            "http://www.civicboom.com/contents/123"
        )
        self.assertEqual(  # same protocol = do have full URL?
            url(protocol="https", controller='contents', action='show', id=123),
            "https://www.civicboom.com/contents/123"
        )

    def test_subdomain(self):
        self.assertEqual(
            url(sub_domain="m", controller='contents', action='show', id=123),
            "https://m.civicboom.com/contents/123"
        )
        self.assertEqual(  # same subdomain = don't have full URL
            url(sub_domain="www", controller='contents', action='show', id=123),
            "/contents/123"
        )
        self.assertEqual(  # unless qualified=True
            url(sub_domain="www", controller='contents', action='show', id=123, qualified=True),
            "https://www.civicboom.com/contents/123"
        )

    def test_host(self):
        self.assertEqual(
            url(host="pie.civicboom.com", controller='contents', action='show', id=123),
            "https://pie.civicboom.com/contents/123"
        )
        self.assertEqual(
            url(host="www.civicboom.com", controller='contents', action='show', id=123, qualified=True),
            "https://www.civicboom.com/contents/123"
        )

    def test_rest_routes(self):
        self.assertEqual(
            url(controller='contents', action='show', id=123),
            "/contents/123"
        )
        self.assertEqual(
            url(controller='contents', action='index'),
            "/contents"
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

    def test_normal_formats(self):
        self.assertEqual(
            url(controller='mobile', action='media_init', format="json"),
            "/mobile/media_init.json"
        )

    def test_rest_formats(self):
        self.assertEqual(
            url(controller='members', action="show", id='shish'),
            "/members/shish"
        )

        self.assertEqual(
            url('member', id='shish'),
            "/members/shish"
        )

        self.assertEqual(
            url('member_action', id='shish', action='follow'),
            "/members/shish/follow.html"
        )

        # with a specified format, it should be .format
        self.assertEquals(
            url('member_action', id='shish', action='follow', format='json'),
            "/members/shish/follow.json"
        )
