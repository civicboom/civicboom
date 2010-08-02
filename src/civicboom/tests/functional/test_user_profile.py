from civicboom.tests import *

class TestUserProfileController(TestController):

    def test_view(self):
        response = self.app.get(url(controller='user_profile', action='view', id='unittest'))
        assert "Mr U. Test (unittest)" in response

    def test_edit(self):
        response = self.app.get(url(controller='user_profile', action='edit', id='unittest'))
        # FIXME: not logged in, expect login prompt

        response = self.app.post(
            "/account/signin", #url(controller='account', action='signin'),
            params={
                'username': u'unittest',
                'password': u'password'
            },
            extra_environ={
                'REMOTE_ADDR': '127.0.0.1'
            }
        )
        # FIXME: response has no c?
        #assert response.c.logged_in_user

        response = self.app.get(url(controller='user_profile', action='edit'))
        # FIXME: test that with no ID, we get our own user page

        response = self.app.get(url(controller='user_profile', action='edit', id='unittest'))
        assert "Display name" in response

        response = self.app.get(url(controller='user_profile', action='edit', id='unitfriend'))
        # FIXME: test that we can't edit other people's profiles

        response = self.app.get(url(controller='user_profile', action='edit', id='MrNotExists'))
        # FIXME: test for a sensible error when accessing a non-existent profile
