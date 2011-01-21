from civicboom.tests import *
from pylons import config

import json

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
            assert get_follower_count()  == followers
            assert get_following_count() == following    
        
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
        