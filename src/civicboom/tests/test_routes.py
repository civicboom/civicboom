from civicboom.tests import *

# inherit from TestController so that url() is set up
class TestRoutes(TestController):
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
            url('member_action', id='shish', action='follow'),
            "/members/shish/follow.html"
        )

        # with a specified format, it should be .format
        self.assertEquals(
            url('member_action', id='shish', action='follow', format='json'),
            "/members/shish/follow.json"
        )
