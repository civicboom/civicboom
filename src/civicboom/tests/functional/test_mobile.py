from civicboom.tests import *

class TestMobileController(TestController):

    #def setUp(self):
    #    response = self.app.get(url(controller='mobile', action='signin'))

    def test_signup(self):
        response = self.app.get(url(controller='mobile', action='signup'))

    def test_latest_version(self):
        response = self.app.get(url(controller='mobile', action='latest_version'))

    def test_accepted_assignments(self):
        response = self.app.get(url(controller='mobile', action='accepted_assignments'))

    def test_messages(self):
        response = self.app.get(url(controller='mobile', action='messages'))

    def test_upload(self):
        #response = self.app.get(url(controller='mobile', action='upload'))
        #response = self.app.get(url(controller='mobile', action='upload_file'))
        pass

    def test_error(self):
        response = self.app.get(url(controller='mobile', action='error'))
