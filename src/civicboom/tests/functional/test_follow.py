from civicboom.tests import *
from pylons import config


class TestFollowController(TestController):


    #---------------------------------------------------------------------------
    # Test Following
    #---------------------------------------------------------------------------
    def test_follow(self):
        """
        """
        
        self.log_in_as('unittest')
        num_unittest_followers = self.get_follower_count()
        num_unittest_following = self.get_following_count()
        
        self.sign_up_as('follow_test')
        
        self.check_follow(following=0, followers=0)
        self.follow('unittest')
        self.check_follow(following=1, followers=0)
        
        self.log_in_as('unittest')
        self.check_follow(following=num_unittest_following  , followers=num_unittest_followers+1)
        self.follow('follow_test')
        self.check_follow(following=num_unittest_following+1, followers=num_unittest_followers+1)
        
        self.log_in_as('follow_test')
        self.check_follow(following=1, followers=1)
        
        
        