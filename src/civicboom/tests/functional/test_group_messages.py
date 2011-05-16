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
        self.assertIn('test_group_messages2', self.getLastNotification()['content']) # Ensure that the group unitfriend joined is reflected in the content
        
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
        
        
        # Check email propergates to all members via approve cycle--------------
        #   this could be simplifyed by just sending a test email, but going though the cycle is only 6 lines so I kept the cycle in
        
        # Create assignment as test_group_3
        assignment_id = self.create_content(title=u'Email test', content=u'Email test', type='assignment')
        # Respond
        self.log_in_as('unitfriend')
        #self.set_persona('test_group_messages2')
        response_id = self.create_content(title=u'Email test response', content=u'Email test response', type='article', parent_id=assignment_id)
        # Approve
        self.log_in_as('unittest')
        self.set_persona('test_group_messages1')
        self.set_persona('test_group_messages2')
        self.set_persona('test_group_messages3')
        num_emails = getNumEmails()
        #AllanC - not needed as unittest's account should be linked to the groups they have created #self.set_account_type('plus') # test_group_messages3 needs to be upgraded to plus account
        response = self.app.post(
            url('content_action', action='approve'    , id=response_id, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        # The above could be replaced with a call to get_group('test_group_mssages3').send_email('test') # but hey .. the above works
        
        # Check that the emails have been generated and sent to the correct users once approved
        self.assertEqual(getNumEmails(), num_emails + 2) # 2 emals are generated, aprove_organisation and apprve_user, HOWEVER! as the aprover is a group it is sent to the two members unittest and unit friend, so 3 emails are actually sent
        emails_sent_when_approved = [
            emails[len(emails)-1],
            emails[len(emails)-2],
        ]
        email_addresss = []
        for emails_to in [email.email_to for email in emails_sent_when_approved]:
            if isinstance(emails_to, list):
                email_addresss += emails_to
            else:
                email_addresss.append(emails_to)
        self.assertEquals(len(email_addresss), 3)
        self.assertIn('unittest@test.com'  , email_addresss)
        self.assertIn('unitfriend@test.com', email_addresss)
        
        
        
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