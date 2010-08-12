from civicboom.tests import *

class TestSearchController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='search', action='index'))
        assert "Search For:" in response


    ##########################################################################
    # Content search
    ##########################################################################

    def test_content_results(self):
        response = self.app.get(url(controller='search', action='content', query='text'))
        assert "Here is some text" in response
        assert "Friend" in response
        assert "5 responses" in response

    def test_content_no_results(self):
        response = self.app.get(url(controller='search', action='content', query='cake'))
        assert "'cake' did not match any articles" in response

    def test_content_no_query(self):
        response = self.app.get(url(controller='search', action='content'))

    def test_content_rss(self):
        response = self.app.get(url(controller='search', action='content', format='xml'))

    def test_content_location(self):
        response = self.app.get(url(controller='search', action='content', location='1,51'))
        assert "Here is some text" in response


    ##########################################################################
    # Location search
    ##########################################################################

    def test_location_page(self):
        response = self.app.get(url(controller='search', action='location'))

    def test_location_results(self):
        response = self.app.get(url(controller='search', action='location', format="json", query="cant"))
        # FIXME: test install has no geolocation data
        #assert "Canterbury" in response

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

