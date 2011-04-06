from civicboom.tests import *

import warnings

class TestGroupsController(TestController):

    def test_message(self):
        
        # Create group and sub group -------------------------------------------
        
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username'     : 'test_group_messages',
                'name'         : 'test_group_messages' ,
                'description'  : 'This group should not be visible once the tests have completed because it will be removed' ,
                'default_role'              : 'admin'  ,
                'join_mode'                 : 'public' ,
                'member_visibility'         : 'public' ,
                'default_content_visibility': 'public' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        group_id = int(response_json['data']['id'])
        self.assertNotEqual(group_id, 0)
        
        self.set_persona('test_group_messages')
        
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username'     : 'test_group_messages2',
                'name'         : 'test_group_messages2' ,
                'description'  : 'This group should not be visible once the tests have completed because it will be removed' ,
                'default_role'              : 'admin'  ,
                'join_mode'                 : 'public' ,
                'member_visibility'         : 'public' ,
                'default_content_visibility': 'public' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        group_id = int(response_json['data']['id'])
        self.assertNotEqual(group_id, 0)
        
        # unitfiend to join sub group ------------------------------------------
        self.log_in_as('unitfriend')
        #self.join('test_group_messages2') # TODO .. BROKEN!!!
        
        # get numbers of messages before for each user
        
        # message get sent to sub group
        
        
        # chec number of messages to check all members and sub members recive it
        
        
        
        # Delete the groups ----------------------------------------------------
        
        self.log_in_as('unittest')
        self.set_persona('test_group_messages')
        
        response = self.app.delete(
            url('group', id='test_group_messages2', format='json'),
            params={
                '_authentication_token': self.auth_token
            },
            status=403
        )
        
        self.set_persona('test_group_messages')
        
        response = self.app.delete(
            url('group', id='test_group_messages', format='json'),
            params={
                '_authentication_token': self.auth_token
            },
            status=200
        )
        

        
        

