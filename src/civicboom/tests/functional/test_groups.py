from civicboom.tests import *

class TestGroupsController(TestController):

    def test_group_page(self):
        response = self.app.get(url('group', id='patty', format='json'))

