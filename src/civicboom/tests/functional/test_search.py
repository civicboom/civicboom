from civicboom.tests import *


class TestSearchController(TestController):

    ##########################################################################
    # Location search
    ##########################################################################

    def test_location_page(self):
        response = self.app.get(url(controller='search', action='location'))

    def test_location_results(self):
        response = self.app.get(url(controller='search', action='location', format="json", term="cant"))
        # FIXME: test install has no geolocation data
        #self.assertIn("Canterbury", response)

    def test_location_no_results(self):
        response = self.app.get(url(controller='search', action='location', format="json", term="waffleville"))
        self.assertNotIn("Canterbury", response)
