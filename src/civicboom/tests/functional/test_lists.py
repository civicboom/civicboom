from civicboom.tests import *
from pylons import config

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
            response = self.app.post(
                url('contents', format='json'),
                params={
                    '_authentication_token': self.auth_token,
                    'title'         : title      ,
                    'contents'      : title      ,
                    'type'          : u'article' ,
                    'submit_publish': u'publish' ,
                },
                status=201
            )
            response_json = json.loads(response.body)
            assert int(response_json['data']['id']) > 0
        
        def create_member(name):
            self.sign_up_as(name)
            self.follow('unittest')
        
        # Create LOTS Users with 1 peice of content each
        #  create as many as the normal serach limit and then one more to test pagination
        for count in range( config['search.default.limit'] + 1):
            create_content('unit_content_%s' % count)
        
        for count in range( config['search.default.limit'] + 1):
            create_member('list_member_%s' % count)
            create_content('list_content_%s' % count)
        