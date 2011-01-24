from civicboom.tests import *

#import json


class TestTimedTasksController(TestController):

    #---------------------------------------------------------------------------
    # Assignment Expire and alert notifications
    #---------------------------------------------------------------------------
    def test_assignment_expire(self):
        """
        Create assignment
        Fake date and time
        trigger timed tasks
        check correct notifications are generated
        """
        pass