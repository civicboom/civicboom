from civicboom.tests import *


class TestAccountController(TestController):

    def setUp(self):
        pass # don't log in


    def test_https_is_required_for_login(self):
        # FIXME: force-https disabled because the mobile app needs
        # a valid certificate, which we don't have for dev.
        #response = self.app.get(
        #    url(controller='account', action='signin'),
        #    extra_environ={'HTTP_X_URL_SCHEME': 'http'},
        #    status=302
        #)

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
                'username': 'unittest',
                'password': 'password'
            },
            status=200
        )


    def test_user_cannot_log_in_with_incorrect_password(self):
        response = self.app.post(
            url(controller='account', action='signin', format="json"),
            extra_environ={'HTTP_X_URL_SCHEME': 'https'},
            params={
                'username': 'unittest',
                'password': 'asdfasdf'
            },
            status=403
        )


    def test_bad_password_causes_reprompt(self):
        response = self.app.post(
            url(controller='account', action='signin', format="html"),
            extra_environ={'HTTP_X_URL_SCHEME': 'https'},
            params={
                'username': 'unittest',
                'password': 'asdfasdf'
            },
            status=302
        )
        self.assertNotIn("Civicboom Internal Error", response)
        response = response.follow()
        # FIXME: this doesn't work; on error, login redirects to referrer,
        # if we re-prompt we lose the referrer... what *should* we do?
        #self.assertIn("Sign in", response)


    def test_user_can_log_in_with_any_linked_janrain_account(self):
        pass
