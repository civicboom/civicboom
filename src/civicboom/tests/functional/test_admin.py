from civicboom.tests import *

class TestAdminController(TestController):

    def test_admin(self):
        response = self.app.get(url(controller='admin', action='models')) # "models" is the admin index

    def test_event_log(self):
        response = self.app.get(url(controller='test', action='fill_log'))
        response = self.app.get(url(controller='admin', action='event_log'))
        assert "debug" in response
        response = self.app.get("/admin/event_log?module=civicboom/controllers/test.py") # test searching

    def test_user_list(self):
        response = self.app.get("/admin/User/models")

    def test_user_edit(self):
        response = self.app.get("/admin/User/models/1/edit?")

    def test_license_list(self):
        response = self.app.get("/admin/License/models")

    def test_license_edit(self):
        response = self.app.get("/admin/License/models/1/edit?")

