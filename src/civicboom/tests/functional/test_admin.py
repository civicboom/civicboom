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

    def test_group_edit(self):
        response = self.app.get("/admin/Group/models/8/edit?")

    # FIXME: these error out when the pages are empty ._.?

    #def test_history_list(self):
    #    response = self.app.get("/admin/ContentEditHistory/models")

    #def test_content_status(self):
    #    response = self.app.get("/admin/Content/models?Content--status=pending")

    def test_user_status(self):
        response = self.app.get("/admin/User/models?User--status=pending")
        response = self.app.get("/admin/User/models?User--status=suspended")

    def test_datepicker_and_usercompleter(self):
        response = self.app.get("/admin/ArticleContent/models/2/edit?")
