from civicboom.tests import *

class TestAccountController(TestController):

    def setUp(self):
        pass # don't log in


    def test_https_is_required_for_login(self):
        response = self.app.get(
            url(controller='account', action='signin'),
            extra_environ={'HTTP_X_URL_SCHEME': 'http'},
            status=302
        )

        response = self.app.get(
            url(controller='account', action='signin'),
            extra_environ={'HTTP_X_URL_SCHEME': 'https'},
            status=200
        )


    def test_user_can_log_in_with_correct_password(self):
        response = self.app.post(
            url(controller='account', action='signin', format="json"),
            extra_environ={'HTTP_X_URL_SCHEME': 'https'},
            params={
                'username': u'unittest',
                'password': u'password'
            },
            status=200
        )


    def test_user_cannot_log_in_with_incorrect_password(self):
        response = self.app.post(
            url(controller='account', action='signin', format="json"),
            extra_environ={'HTTP_X_URL_SCHEME': 'https'},
            params={
                'username': u'unittest',
                'password': u'asdfasdf'
            },
            status=403
        )


    def test_user_can_log_in_with_any_linked_janrain_account(self):
        pass
