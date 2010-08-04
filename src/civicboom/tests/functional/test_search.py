from civicboom.tests import *

class TestSearchController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='search', action='index')) # this redirects to the next
        response = self.app.get('/search/index')
        assert "Search for" in response


    ##########################################################################
    # Content search
    ##########################################################################

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
        # FIXME: the above generates /search/content/ which redirects to /search/content...

        response = self.app.get("/search/content", status=302)
        # FIXME: redirect to search/index
        # FIXME: assert "Search for" in response after redirection


    ##########################################################################
    # Location search
    ##########################################################################

    def test_location_page(self):
        response = self.app.get(url(controller='search', action='location'))

    def test_location_results(self):
        response = self.app.get(url(controller='search', action='location', format="json", query="cant"))
        assert "Canterbury" in response

    def test_location_no_results(self):
        response = self.app.get(url(controller='search', action='location', format="json", query="waffleville"))
        assert "Canterbury" not in response


    ##########################################################################
    # Location search
    ##########################################################################

    def test_member_page(self):
        response = self.app.get(url(controller='search', action='member'))

    def test_member_name_results(self):
        response = self.app.get(url(controller='search', action='member', format="json", query="mr"))
        assert "Mr U. Test" in response

    def test_member_username_results(self):
        response = self.app.get(url(controller='search', action='member', format="json", query="unit"))
        assert "Mr U. Test" in response

    def test_member_no_results(self):
        response = self.app.get(url(controller='search', action='member', format="json", query="waffleville"))
        assert "Mr" not in response

