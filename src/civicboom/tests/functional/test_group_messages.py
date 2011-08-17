from civicboom.tests import *


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
        group_id = response_json['data']['id']
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
        self.assertEquals(self.getNumNotifications(), unitfriend_num_notifications + 1) # the join notification when they first joined (anoying I know)
        unitfriend_num_notifications += 1
        
        
        # check "new user joined" notifcation
        self.log_in_as('unittest')
        self.assertEquals(self.getNumNotifications(), unittest_num_notifications + 1)
        unittest_num_notifications += 1
        self.assertIn('test_group_messages2', self.getLastNotification()['content']) # Ensure that the group unitfriend joined is reflected in the content
        
        # message get sent to sub group and should propergate up the chain
        #self.log_in_as('unittest')
        #self.set_persona('unittest')
        #self.send_member_message('test_group_messages3', 'test message', 'a message to test to see if messages can be posted to infinately looping chains of groups')
        
        # the follow message should propergate to unittests notifications
        self.follow('test_group_messages3')
        self.follow('test_group_messages1')
        self.assertEquals(self.getNumNotifications(), unittest_num_notifications   + 2)
        unittest_num_notifications += 2
        
        # unitfriend should have 2 notifications - the follow of test_3
        self.log_in_as('unitfriend')
        self.assertEquals(self.getNumNotifications(), unitfriend_num_notifications + 1)
        unitfriend_num_notifications += 1
        
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
        
        # 'unitfriend' is now going to respond
        # This will:
        #  - Accept the assignment 'accepted' notification
        #    - Will auto follow 'test_group_messages3' - 'new follower' notification
        #  - Create a new response notification 'response' notification
        num_notifications = self.getNumNotificationsInDB()
        
        response_id = self.create_content(title=u'Email test response', content=u'Email test response', type='article', parent_id=assignment_id)
        
        # 'unitfriend' will have followers that will be alerted to the new content
        # these need to be considered when checking the number of notifications generated
        # NOTE: if unitfriend has any GROUPS as followers this automated test WILL break - as we dont know how many notifications will be generated
        num_unitfriend_followers = self.get_member('unitfriend')['member']['num_followers']
        
        notification_subjects = [message.subject for message in self.getNotificationsFromDB( (3*3) + num_unitfriend_followers )]
        self.assertSubStringIn('follow', notification_subjects)
        self.assertSubStringIn('accept', notification_subjects)
        self.assertSubStringIn('respon', notification_subjects)
        self.assertEquals(self.getNumNotificationsInDB(), num_notifications + (3*3) + num_unitfriend_followers ) # 3 notifications should be generated (accepted, new follow, new response) for 3 users test_group_3 + unittest (as member of test_group_1) + unitfriend (is member of test_group_2) 
        
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
        self.assertIn('test+unittest@civicboom.com'  , email_addresss)
        self.assertIn('test+unitfriend@civicboom.com', email_addresss)
        
        
        
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


    def test_message_followers(self):
        """
        Have a member with followers to test message propergation
        The end user should not be messaged twice
        """
        # Setup
        # 'unitfriend' should have 2 followers: 'unittest' and 'message_test'(that unittest is a member of)
        self.log_in_as('unittest')
        self.assertIn('unitfriend', [following['username'] for following in self.get_member()['following']['items']]) # Check unittest is a follower of unitfriend
        self.create_group('message_test')
        self.set_persona('message_test')
        self.follow('unitfriend')
        
        self.log_in_as('unitfriend')
        num_notifications = self.getNumNotificationsInDB()
        num_emails        =      getNumEmails()
        num_unitfriend_followers = self.get_member('unitfriend')['member']['num_followers'] # NOTE: all followers MUST be users appart from one group (added above) or this test will fail
        
        self.boom_content(1) # Boom API doc guaranteed to be content 1
        
        self.assertEquals(self.getNumNotificationsInDB(), num_notifications + num_unitfriend_followers    )
        self.assertEquals(     getNumEmails()           , num_emails        + num_unitfriend_followers - 1)
        
        self.log_in_as('unittest')
        self.set_persona('message_test')
        self.delete_group('message_test')
