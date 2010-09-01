from civicboom.tests import *

class TestAdminController(TestController):

    def test_admin(self):
        response = self.app.get(url(controller='admin', action='models')) # "models" is the admin index

    def test_event_log(self):
        response = self.app.get(url(controller='test', action='fill_log'))
        response = self.app.get(url(controller='admin', action='event_log'))
        assert "debug" in response
        # test searching
        response = self.app.get(url(controller='admin', action='event_log', module='civicboom/controllers/test.py'))
        response = self.app.get(url(controller='admin', action='event_log', line_num='20'))
        response = self.app.get(url(controller='admin', action='event_log', username='None'))
        response = self.app.get(url(controller='admin', action='event_log', address='127.0.0.1'))
        response = self.app.get(url(controller='admin', action='event_log', url='http://waffle.com'))

    def test_user_list(self):
        response = self.app.get("/admin/User/models")

    def test_admin_search(self):
        # tests strings
        response = self.app.get("/admin/User/models?User--username=jammy")
        # tests ints
        response = self.app.get("/admin/Group/models?Group--num_members=1")

    def test_user_edit(self):
        response = self.app.get("/admin/User/models/1/edit?")

    def test_license_list(self):
        response = self.app.get("/admin/License/models")

    def test_license_edit(self):
        response = self.app.get("/admin/License/models/1/edit?")

    def test_group_new(self):
        response = self.app.get("/admin/Group/models/new")

