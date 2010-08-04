from civicboom.tests import *

class TestUserProfileController(TestController):

    def test_view(self):
        response = self.app.get(url(controller='user_profile', action='view', id='unittest'))
        assert "Mr U. Test (unittest)" in response

    def test_bad_profile_view(self):
        # test for a sensible error when accessing a non-existent profile
        response = self.app.get(url(controller='user_profile', action='edit', id='MrNotExists'))
        # FIXME: test

    def test_edit(self):
        # not logged in, expect login prompt
        response = self.app.get(url(controller='user_profile', action='edit', id='unittest'))
        # FIXME: test it

        response = self.app.post(
            "/account/signin", #url(controller='account', action='signin'),
            params={
                'username': u'unittest',
                'password': u'password'
            }
        )
        # FIXME: response has no c?
        #assert response.c.logged_in_user

        # test that with no ID, we get our own user page
        response = self.app.get(url(controller='user_profile', action='edit'))
        # FIXME: test it

        response = self.app.get(url(controller='user_profile', action='edit', id='unittest'))
        # FIXME: this fails? :|
        # assert "Display name" in response

        # test that settings get set
        response = self.app.post(
            "/user_profile/save", #url(controller='account', action='signin'),
            params={
                'email': u'waffle@iamtesting.com',
            },
        )
        # FIXME: check for session['flash'] = "Settings changed: email"
        # FIXME: check that we're redirected back to the settings page
        # FIXME: check that the new settings appear on the new page

        # test that we can't edit other people's profiles
        response = self.app.get(url(controller='user_profile', action='edit', id='unitfriend'))
        # FIXME: test
