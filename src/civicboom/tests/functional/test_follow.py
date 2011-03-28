from civicboom.tests import *
from pylons import config

#import json


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
            response      = self.app.get(url('member_action', action='following', id=username, limit=0, format='json'), status=200)
            response_json = json.loads(response.body)
            if   type == 'trusted':
                return len(folow for folow in response_json['data']['list']['items'] if follow['follow_type']=='trusted'       )
            elif type == 'trusted_invite':
                return len(folow for folow in response_json['data']['list']['items'] if follow['follow_type']=='trusted_invite')
            return response_json['data']['list']['count']
        
        def get_follower_count(username=None, follow_type=None):
            if not username:
                username = self.logged_in_as
            response      = self.app.get(url('member_action', action='followers', id=username, limit=0, format='json'), status=200)
            response_json = json.loads(response.body)
            if   type == 'trusted':
                return len(folow for folow in response_json['data']['list']['items'] if follow['follow_type']=='trusted'       )
            elif type == 'trusted_invite':
                return len(folow for folow in response_json['data']['list']['items'] if follow['follow_type']=='trusted_invite')
            return response_json['data']['list']['count']
        
        def check_follow(following, followers, username='follow_test'):
            # Get follow and follower lists and check correct number of items
            self.assertEqual(get_follower_count() , followers)
            self.assertEqual(get_following_count(), following)
            
            # Check postgresql triggers
            response      = self.app.get(url('member', id=self.logged_in_as, format='json'), status=200)
            response_json = json.loads(response.body)
            
            self.assertEqual(response_json['data']['followers']['count'], response_json['data']['member']['num_followers'])
            self.assertEqual(response_json['data']['followers']['count'], followers)
            
            self.assertEqual(response_json['data']['following']['count'], response_json['data']['member']['num_following'])
            self.assertEqual(response_json['data']['following']['count'], following)
            
        
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
        
        self.log_in_as('unittest')        
        
        # Invite follow_test as a trusted follower
        check_follow(following=num_unittest_following, followers=num_unittest_followers)
        self.follower_invite_trusted('follow_test') 
        #check_follow(following=num_unittest_following, followers=num_unittest_followers + 1)
        self.assertEquals(get_follower_count(follow_type='trusted_invite'), 1)
        self.assertEquals(get_follower_count(follow_type='trusted'       ), 0)
        self.log_out()
        self.assertEquals(get_follower_count(username='unittest'), num_unittest_followers)
        
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
        self.follower_distrust('follow_test') # Should negate previous state
        self.assertEquals(get_following_count(follow_type='trusted_invite'), 0)
        self.assertEquals(get_following_count(follow_type='trusted'       ), 0)
        

