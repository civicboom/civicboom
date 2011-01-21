from civicboom.tests import *
#from pylons import config

import json


class TestListsController(TestController):

    #---------------------------------------------------------------------------
    # Assignment Limit
    #---------------------------------------------------------------------------
    def test_lists(self):
        """
        Create a large number of articles and members to test list functionality
        """
        def create_content(title):
            pass
        def create_member(name):
            self.sign_up_as(name)
            self.follow('unittest')
        
        for count in range(30):
            create_member('list_member_%s' % count)
            create_content('list_content_%s' % count)