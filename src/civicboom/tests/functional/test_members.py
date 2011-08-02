from civicboom.tests import *


class TestMembersController(TestController):

    def test_member_page(self):
        response = self.app.get(url('members', format='json'))

    def test_member_list(self):
        # by name
        response = self.app.get(url('members', format="json", list="all", term="mr"))
        self.assertIn("Mr U. Test", response)

        # by username
        # fff, this is pushed onto the second page of results...
        #response = self.app.get(url('members', format="json", list="all", term="unit"))
        #self.assertIn("Mr U. Test", response)

        # invalid
        response = self.app.get(url('members', format="json", list="all", term="waffleville"))
        self.assertNotIn("Mr", response)

    def test_member_show(self):
        response = self.app.get(url('member', id='unittest', format='json'))

        # case shouldn't matter
        response = self.app.get(url('member', id='UnitTest', format='json'))

        # non-existent members should 404
        response = self.app.get(url('member', id='mrdoesnotexist', format='json'), status=404)

        # show content from members
        response = self.app.get(url('member_action', id='unittest', action='content'           , format='json'                 ))
        response = self.app.get(url('member_action', id='unittest', action='content'           , format='json', list='articles'))
        response = self.app.get(url('member_action', id='unittest', action='boomed'            , format='json'                 ))
        response = self.app.get(url('member_action', id='unittest', action='content_and_boomed', format='json'                 ))

        # badly named content lists should give "bad paramaters" error
        response = self.app.get(url('member_action', id='unittest', action='content', list='cake', format='json'), status=400)

    def test_member_follow(self):
        # no following self
        response = self.app.post(
            url('member_action', id='unittest', action='follow', format='json'),
            params={'_authentication_token': self.auth_token},
            status=400
        )

        # can follow someone else; refollow is error?
        response = self.app.post(
            url('member_action', id='puppy', action='follow', format='json'),
            params={'_authentication_token': self.auth_token},
        )
        response = self.app.post(
            url('member_action', id='puppy', action='follow', format='json'),
            params={'_authentication_token': self.auth_token},
            status=400
        )

        # can unfollow a followed person; re-unfollow is error?
        response = self.app.post(
            url('member_action', id='puppy', action='unfollow', format='json'),
            params={'_authentication_token': self.auth_token},
        )
        response = self.app.post(
            url('member_action', id='puppy', action='unfollow', format='json'),
            params={'_authentication_token': self.auth_token},
            status=400
        )
