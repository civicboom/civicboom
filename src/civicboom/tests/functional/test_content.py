from civicboom.tests import *

class TestContentController(TestController):

    def test_view(self):
        response = self.app.get(url(controller='content', action='view', id=1))

    def test_view_article(self):
        # 2 just happens to be the ID of an Article, so we can test the view counter
        response = self.app.get(url(controller='content', action='view', id=2))

    def test_view_non_exist(self):
        response = self.app.get(url(controller='content', action='view', id=0))
