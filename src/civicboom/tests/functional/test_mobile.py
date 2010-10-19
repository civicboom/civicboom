from civicboom.tests import *

class TestMobileController(TestController):

    def test_latest_version(self):
        response = self.app.get(url(controller='mobile', action='latest_version'))

    def test_media(self):
        #response = self.app.get(url(controller='mobile', action='upload'))
        #response = self.app.get(url(controller='mobile', action='upload_file'))
        pass

    def test_error(self):
        response = self.app.get(url(controller='mobile', action='error', format="json"))
