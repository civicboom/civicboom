from civicboom.tests import *

class TestSettingsController(TestController):

    def test_need_signin(self):
        self.log_out()
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
                '_authentication_token': self.auth_token
            }
        )

    def test_location(self):
        # test that with no ID, we get our own user page
        response = self.app.get(url(controller='settings', action='location'))
        # FIXME: location page has no text to test for

        # test for error
        response = self.app.post(
            url(controller='settings', action='save_location', id='unittest'),
            params={
                '_authentication_token': self.auth_token
            }
        )

        # test guess-coordinates-by-name
        response = self.app.post(
            url(controller='settings', action='save_location', id='unittest'),
            params={
                '_authentication_token': self.auth_token,
                'location_name': "Canterbury"
            }
        )

        # test specified coordinates
        response = self.app.post(
            url(controller='settings', action='save_location', id='unittest'),
            params={
                '_authentication_token': self.auth_token,
                'location_name': "Canterbury",
                'location': '1.28,51.28'
            }
        )

        # test specified coordinates with json output
        response = self.app.post(
            url(controller='settings', action='save_location', id='unittest', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'location_name': "Canterbury",
                'location': '1.28,51.28'
            }
        )
        # FIXME: test response["status"] == "ok"

        # test bad location
        response = self.app.post(
            url(controller='settings', action='save_location', id='unittest', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'location_name': "Canterbury",
                'location': 'arf arf I am a waffle'
            }
        )
        # FIXME: test response["status"] == "error"

    def test_messages(self):
        # test that with no ID, we get our own user page
        response = self.app.get(url(controller='settings', action='messages'))
        assert "a test message" in response

        response = self.app.post(
            url(controller='settings', action='save_messages', id='unittest'),
            params={
                '_authentication_token': self.auth_token
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
        assert "Hold it!" in response
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
        #    params={'_authentication_token': self.auth_token},
        #    status=403,
        #)
        # FIXME: test
