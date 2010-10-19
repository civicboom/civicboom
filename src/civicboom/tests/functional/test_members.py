from civicboom.tests import *

class TestMembersController(TestController):

    def test_member_page(self):
        response = self.app.get(url(controller='members', action='index', format='json'))

    def test_member_name_results(self):
        response = self.app.get(url(controller='members', action='index', format="json", list="all", term="mr"))
        assert "Mr U. Test" in response

    def test_member_username_results(self):
        response = self.app.get(url(controller='members', action='index', format="json", list="all", term="unit"))
        assert "Mr U. Test" in response

    def test_member_no_results(self):
        response = self.app.get(url(controller='members', action='index', format="json", list="all", term="waffleville"))
        assert "Mr" not in response

