from civicboom.tests import *

class TestSettingsController(TestController):
    def setUp(self):
        response = self.app.post(
            url(controller='account', action='signin'),
            extra_environ={'HTTP_X_URL_SCHEME': 'https'},
            params={
                'username': u'unittest',
                'password': u'password'
            }
        )

    def test_need_signin(self):
        response = self.app.get(url(controller='account', action='signout'))
        response = self.app.get(url(controller='settings', action='general', id='unittest'), status=302)
        # FIXME: follow the redirect, then:
        # assert "Sign in" in response

    def test_general(self):
        # test that with no ID, we get our own user page
        response = self.app.get(url(controller='settings', action='general'))
        assert "Display name" in response

        response = self.app.post(
            url(controller='settings', action='save_general', id='unittest'),
            params={
                '_authentication_token': response.session['_authentication_token']
            }
        )

    def test_csrf(self):
        # test that a setting without CSRF protection is rejected
        response = self.app.post(
            url(controller='settings', action='save_general'),
            params={
                'email': u'waffle@iamtesting.com',
            },
            status = 403
        )
        # FIXME: test with CSRF protection passed
        # FIXME: check for session['flash'] = "Settings changed: email"
        # FIXME: check that we're redirected back to the settings page
        # FIXME: check that the new settings appear on the new page

    def test_edit_other_person_fails(self):
        response = self.app.get(url(controller='settings', action='general'))

        # test that we can't edit other people's profiles
        # FIXME: for now, the 'id' paramater is ignored
        #response = self.app.post(
        #    url(controller='settings', action='save_general', id='unitfriend'),
        #    params={'_authentication_token': response.session['_authentication_token']},
        #    status=403,
        #)
        # FIXME: test
