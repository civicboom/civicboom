from civicboom.tests import *

class TestAccountController(TestController):
    def test_signin(self):
        response = self.app.get(
            "/account/signin", #url(controller='account', action='signin'),
            params={
                'username': u'unittest',
                'password': u'password'
            }
        )
