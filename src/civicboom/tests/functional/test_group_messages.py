from civicboom.tests import *

import warnings

class TestGroupsController(TestController):

    def create_group(self, group_name):
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username'     : group_name ,
                'name'         : group_name ,
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
    
    def delete_group(self, group_name):
        response = self.app.delete(
            url('group', id=group_name, format='json'),
            params={
                '_authentication_token': self.auth_token
            },
            status=200
        )


    def test_message(self):

        # Create group chain ---------------------------------------------------
        
        self.create_group('test_group_messages1')
        self.set_persona( 'test_group_messages1')
        self.create_group('test_group_messages2')
        self.set_persona( 'test_group_messages2')
        self.create_group('test_group_messages3')
        self.set_persona( 'test_group_messages3')
        
        # remeber num notifications --------------------------------------------
        self.log_in_as('unittest')
        self.set_persona('unittest')
        unittest_num_notifications   = self.getNumNotifications()
        
        self.log_in_as('unitfriend')
        unitfriend_num_notifications = self.getNumNotifications()
        
        # unitfiend to join sub group ------------------------------------------
        # unitfirend should not receve messages intended for test_1 as they are a member half way down the chain
        self.log_in_as('unitfriend')
        self.join('test_group_messages2')
        
        
        # check "new user joined" notifcation
        self.log_in_as('unittest')
        self.assertEquals(self.getNumNotifications(), unittest_num_notifications + 1)
        
        
        # message get sent to sub group and should propergate up the chain
        #self.log_in_as('unittest')
        #self.set_persona('unittest')
        #self.send_member_message('test_group_messages3', 'test message', 'a message to test to see if messages can be posted to infinately looping chains of groups')
        
        # the follow message should propergate to unittests notifications
        self.follow('test_group_messages3')
        self.follow('test_group_messages1')
        self.assertEquals(self.getNumNotifications(), unittest_num_notifications   + 3)
        
        # unitfriend should have 2 notifications - 1, the join notification when they first joined (anoying I know) 2. the follow of test_3
        self.log_in_as('unitfriend')
        self.assertEquals(self.getNumNotifications(), unitfriend_num_notifications + 2)
        
        # chec number of messages to check all members and sub members recive it
        
        
        # Create group infinate loop -------------------------------------------
        self.log_in_as('unittest')
        self.set_persona('unittest')
        self.set_persona('test_group_messages1')
        self.set_persona('test_group_messages2')
        self.set_persona('test_group_messages3')
        self.join(       'test_group_messages1')
        
        self.send_member_message('test_group_messages3', 'test message', 'a message to test to see if messages can be posted to infinately looping chains of groups')
        
        
        # Delete the groups ----------------------------------------------------
        
        self.log_in_as('unittest')
        self.set_persona( 'unittest')
        self.set_persona( 'test_group_messages1')
        self.set_persona( 'test_group_messages2')
        self.set_persona( 'test_group_messages3')
        self.delete_group('test_group_messages3')
        
        self.set_persona( 'unittest')
        self.set_persona( 'test_group_messages1')
        self.set_persona( 'test_group_messages2')
        self.delete_group('test_group_messages2')
        
        self.set_persona( 'unittest')
        self.set_persona( 'test_group_messages1')
        self.delete_group('test_group_messages1')