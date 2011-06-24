from civicboom.tests import *


class TestWorker(TestController):
    
    def test_worker_message(self):
        self.config_var('test_mode', 'False')
        
        # Messages when not in test mode are qued in the worker thread ... this forces the worker thread to be excersised
        
        self.unfollow('unitfriend')
        self.follow('unitfriend')
        
        # AllanC - how do we check the messages actually got there?
        #self.send_member_message('unitfriend', 'test message', 'a message to test to see if messages can be posted to using the worker thread')
        
        self.config_var('test_mode', 'True')
