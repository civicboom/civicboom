from civicboom.tests import *


class TestFollowController(TestController):
    #---------------------------------------------------------------------------
    # Test Following
    #---------------------------------------------------------------------------
    def test_follow(self):
        """
        """

        def get_following_count(username=None, follow_type=None):
            if not username:
                username = self.logged_in_as
            response      = self.app.get(url('member_action', action='following', id=username, format='json'), status=200)
            response_json = json.loads(response.body)
            if follow_type:
                return len([follow for follow in response_json['data']['list']['items'] if follow['follow_type']==follow_type])
            return response_json['data']['list']['count']
        
        def get_follower_count(username=None, follow_type=None):
            if not username:
                username = self.logged_in_as
            response      = self.app.get(url('member_action', action='followers', id=username, format='json'), status=200)
            response_json = json.loads(response.body)
            if follow_type:
                return len([follow for follow in response_json['data']['list']['items'] if follow['follow_type']==follow_type])
            return response_json['data']['list']['count']
        
        def check_follow(following, followers, check_postgress_triggers=True):
            # Get follow and follower lists and check correct number of items
            self.assertEqual(get_follower_count() , followers)
            self.assertEqual(get_following_count(), following)
            
            response      = self.app.get(url('member', id=self.logged_in_as, format='json'), status=200)
            response_json = json.loads(response.body)
            
            self.assertEqual(response_json['data']['followers']['count'], followers)
            self.assertEqual(response_json['data']['following']['count'], following)
            
            # Check postgresql triggers            
            if check_postgress_triggers:
                self.assertEqual(response_json['data']['followers']['count'], response_json['data']['member']['num_followers'])
                self.assertEqual(response_json['data']['following']['count'], response_json['data']['member']['num_following'])

            
        
        # Followers ------------------------------------------------------------
        
        self.log_in_as('unittest')
        num_unittest_followers = get_follower_count()
        num_unittest_following = get_following_count()
        
        self.sign_up_as('follow_test')
        
        check_follow(following=0, followers=0)
        self.follow('unittest')
        check_follow(following=1, followers=0)
        
        self.log_in_as('unittest')
        check_follow(following=num_unittest_following  , followers=num_unittest_followers+1)
        self.follow('follow_test')
        check_follow(following=num_unittest_following+1, followers=num_unittest_followers+1)
        
        self.log_in_as('follow_test')
        check_follow(following=1, followers=1)
        self.unfollow('unittest')
        check_follow(following=0, followers=1)
        
        self.log_in_as('unittest')
        check_follow(following=num_unittest_following+1, followers=num_unittest_followers  )
        self.unfollow('follow_test')
        
        # both unittest and follow_test should be back to there starting numbers
        
        
        # Trusted Followers ----------------------------------------------------
        
        self.log_in_as('follow_test')
        
        # Normal users cant trust followers - should reject due to permissions
        response = self.app.post(
            url('member_action', action='follower_trust', id='unittest', format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=402
        )
        
        # Upgrade acount type - trusted followers needs paid for account
        self.set_account_type('plus')
        
        self.log_in_as('unittest')
        #self.set_account_type('plus') # unittest is already a plus account at creation
        
        
        # Invite follow_test as a trusted follower
        check_follow(following=num_unittest_following, followers=num_unittest_followers)
        self.follower_invite_trusted('follow_test')
        response = self.app.post( # try action again, should error
            url('member_action', action='follower_invite_trusted', id='follow_test', format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=500
        )
        
        check_follow(following=num_unittest_following, followers=num_unittest_followers + 1, check_postgress_triggers=False) # the trsuted invite will appear in the follower list for the logged_in user
        self.assertEquals(get_follower_count(follow_type='trusted_invite'), 1)
        self.assertEquals(get_follower_count(follow_type='trusted'       ), 0)
        self.log_out()
        self.assertEquals(get_follower_count(username='unittest'), num_unittest_followers) # invite will not appear for a not logged in user
        
        # Check invite and upgrade to trsuted follower
        self.log_in_as('follow_test')
        self.assertEquals(get_following_count(follow_type='trusted_invite'), 1) # Check invite
        self.assertEquals(get_following_count(follow_type='trusted'       ), 0)
        self.follow('unittest')
        self.assertEquals(get_following_count(follow_type='trusted_invite'), 0) # Check upgrade from invite to trusted follow
        self.assertEquals(get_following_count(follow_type='trusted'       ), 1)
        
        # Check follower has been upgraded to trusted
        self.log_in_as('unittest')
        self.assertEquals(get_follower_count(follow_type='trusted_invite'), 0)
        self.assertEquals(get_follower_count(follow_type='trusted'       ), 1)
        
        self.log_in_as('follow_test')
        # Unfollow - Check I am not trusted follower
        self.assertEquals(get_following_count(follow_type='trusted_invite'), 0)
        self.assertEquals(get_following_count(follow_type='trusted'       ), 1)
        self.unfollow('unittest')
        self.assertEquals(get_following_count(follow_type='trusted_invite'), 0)
        self.assertEquals(get_following_count(follow_type='trusted'       ), 0)
        
        # Check I am not trusted follower
        self.assertEquals(get_following_count(follow_type='trusted_invite'), 0)
        self.assertEquals(get_following_count(follow_type='trusted'       ), 0)
        self.follow('unittest')
        self.assertEquals(get_following_count(follow_type='trusted_invite'), 0)
        self.assertEquals(get_following_count(follow_type='trusted'       ), 0)
        
        # Elevate and deelavte trsuted
        self.log_in_as('unittest')
        self.assertEquals(get_following_count(follow_type='trusted_invite'), 0)
        self.assertEquals(get_following_count(follow_type='trusted'       ), 0)
        self.follower_trust('follow_test')    # trust
        response = self.app.post( #trust again - fail
            url('member_action', action='follower_trust', id='follow_test', format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=400
        )
        self.follower_distrust('follow_test') # Should negate previous state
        self.assertEquals(get_following_count(follow_type='trusted_invite'), 0)
        self.assertEquals(get_following_count(follow_type='trusted'       ), 0)

    #---------------------------------------------------------------------------
    # Test Feature - Hidden followers option
    #---------------------------------------------------------------------------
    def test_hidden_followers(self):
        
        def get_follower_count(username=None):
            if not username:
                username = self.logged_in_as
            response      = self.app.get(url('member_action', action='followers', id=username, format='json'), status=200)
            response_json = json.loads(response.body)
            return response_json['data']['list']['count']
        
        # Count current followers (private)
        # Count current followers (public)
        self.log_in_as('unittest')
        followers_private = get_follower_count('unittest')
        self.log_out()
        followers_public  = get_follower_count('unittest')
        
        self.log_in_as('unittest')
        
        # Set hide followers setting
        self.setting('hide_followers', 'advanced', True)
        
        # Count again (private) - should be all there
        self.assertEquals(followers_private, get_follower_count('unittest'))
        
        # Logged in as anyone else should reveal no followers
        self.log_out()
        self.assertEquals(get_follower_count('unittest'), 0)
        self.log_in_as('unitfriend')
        self.assertEquals(get_follower_count('unittest'), 0)
        
        # Set hide followers to false
        self.log_in_as('unittest')
        self.setting('hide_followers', 'advanced', False)