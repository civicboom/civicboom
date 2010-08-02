from civicboom.tests import *

class TestSearchController(TestController):

    def test_content_results(self):
        response = self.app.get(url(controller='search', action='content', id='text'))
        assert "Here is some text" in response
        assert "Mr U. Test" in response
        assert "2 responses" in response

    def test_content_no_results(self):
        response = self.app.get(url(controller='search', action='content', id='cake'))
        assert "'cake' did not match any articles" in response

    def test_content_no_query(self):
        response = self.app.get(url(controller='search', action='content'), status=302) # redirect to search/index
        #assert "Search for" in response
