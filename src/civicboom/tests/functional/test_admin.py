from civicboom.tests import *

class TestEventlogController(TestController):

    def test_event_log(self):
        response = self.app.get(url(controller='test', action='fill_log'))
        response = self.app.get(url(controller='admin', action='event_log'))
        #assert "debug" in response /admin/event_log/ is redirected to /admin/event_log, *then* the page is visible

    def test_admin(self):
        response = self.app.get(url(controller='admin'))

    def test_user_list(self):
        response = self.app.get("/admin/User/models")

    def test_user_edit(self):
        response = self.app.get("/admin/User/models/1/edit?")

    def test_license_list(self):
        response = self.app.get("/admin/License/models")

    def test_license_edit(self):
        response = self.app.get("/admin/License/models/1/edit?")

