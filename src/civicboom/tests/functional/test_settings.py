from civicboom.tests import *

class TestSettingsController(TestController):
    def test_general(self):
        # not logged in, expect login prompt
        response = self.app.get(url(controller='settings', action='save_general', id='unittest'))
        # FIXME: test it

        return # FIXME: POST requires HTTPS, which we don't have...

        response = self.app.post(
            url(controller='account', action='signin'),
            params={
                'username': u'unittest',
                'password': u'password'
            }
        )
        # FIXME: response has no c?
        #assert response.c.logged_in_user

        # test that with no ID, we get our own user page
        response = self.app.get(url(controller='settings', action='save_general'))
        # FIXME: test it

        response = self.app.get(url(controller='settings', action='save_general', id='unittest'))
        # FIXME: this fails? :|
        # assert "Display name" in response

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

        # test that we can't edit other people's profiles
        response = self.app.get(url(controller='settings', action='save_general', id='unitfriend'))
        # FIXME: test
