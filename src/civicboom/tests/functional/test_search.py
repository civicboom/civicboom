from civicboom.tests import *

class TestSearchController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='search', action='index'))
        assert "Search For:" in response


    ##########################################################################
    # Location search
    ##########################################################################

    def test_location_page(self):
        response = self.app.get(url(controller='search', action='location'))

    def test_location_results(self):
        response = self.app.get(url(controller='search', action='location', format="json", term="cant"))
        # FIXME: test install has no geolocation data
        #assert "Canterbury" in response

    def test_location_no_results(self):
        response = self.app.get(url(controller='search', action='location', format="json", term="waffleville"))
        assert "Canterbury" not in response
