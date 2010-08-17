from civicboom.tests import *

class TestMessagesController(TestController):
    def setUp(self):
        response = self.app.post(
            url(controller='account', action='signin'),
            extra_environ={'HTTP_X_URL_SCHEME': 'https'},
            params={
                'username': u'unittest',
                'password': u'password'
            }
        )

    def test_index(self):
        response = self.app.get(url(controller='messages', action='index'))
        assert "Re: Re: singing" in response

    def test_read(self):
        response = self.app.get(url(controller='messages', action='read', id=2))
        assert "truncation" in response
