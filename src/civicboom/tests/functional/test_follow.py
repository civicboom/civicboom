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

        def get_following_count():
            response      = self.app.get(url('member_action', action='following', id=self.logged_in_as, format='json'), status=200)
            response_json = json.loads(response.body)
            return response_json['data']['list']['count']
        
        def get_follower_count():
            response      = self.app.get(url('member_action', action='followers', id=self.logged_in_as, format='json'), status=200)
            response_json = json.loads(response.body)
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
            
        
        self.log_in_as('unittest')
        num_unittest_followers = get_follower_count()
        num_unittest_following = get_following_count()
        
        self.sign_up_as('follow_test')
        
        check_follow(following=0, followers=0)
        self.follow('unittest')
        check_follow(following=1, followers=0)
        
        # GregM: Test basic trust distrust routines
        self.log_in_as('unittest')
        # Check not trusted
        self.follower_trust('follow_test')
        # Check trused
        self.follower_distrust('follow_test')
        # Check not trusted
        
        self.log_in_as('unittest')
        check_follow(following=num_unittest_following  , followers=num_unittest_followers+1)
        self.follow('follow_test')
        check_follow(following=num_unittest_following+1, followers=num_unittest_followers+1)
        
        self.log_in_as('follow_test')
        check_follow(following=1, followers=1)
        
        # GregM: Begin testing trusted follow invites etc.
        self.unfollow('unittest')
        check_follow(following=0, followers=1)
        
        self.log_in_as('unittest')
        check_follow(following=num_unittest_following+1, followers=num_unittest_followers  )
        self.follower_invite_trusted('follow_test')
        check_follow(following=num_unittest_following+1, followers=num_unittest_followers  )
        
        self.log_in_as('follow_test')
        # Check invite
        self.follow('unittest')
        check_follow(following=1, followers=1)
        # Check I am trusted follower
        
        self.log_in_as('unittest')
        check_follow(following=num_unittest_following+1, followers=num_unittest_followers+1)
        # Check follow_test is trusted
        
        self.log_in_as('follow_test')
        self.unfollow('unittest')
        # Check I am not trusted follower
        
        self.follow('unittest')
        # Check I am not trusted follower