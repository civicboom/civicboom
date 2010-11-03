from civicboom.tests import *

class TestMembersController(TestController):

    def test_member_page(self):
        response = self.app.get(url('members', format='json'))

    def test_member_name_results(self):
        response = self.app.get(url('members', format="json", list="all", term="mr"))
        assert "Mr U. Test" in response

    def test_member_username_results(self):
        response = self.app.get(url('members', format="json", list="all", term="unit"))
        assert "Mr U. Test" in response

    def test_member_no_results(self):
        response = self.app.get(url('members', format="json", list="all", term="waffleville"))
        assert "Mr" not in response


    def test_member_show(self):
        response = self.app.get(url('member', id='unittest', format='json'))

    def test_member_show_nonexist(self):
        response = self.app.get(url('member', id='mrdoesnotexist', format='json'), status=404)

