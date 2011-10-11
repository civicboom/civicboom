from civicboom.tests import *

import warnings


class TestGroupsController(TestController):

    #self.group_id = 0

    ## index -> show #########################################################

    #def test_group(self):
    #    response = self.app.get(url('group', id='patty', format='json'))
    #    self.assertIn('patty', response)

    #def test_group_page_html(self):
    #    response = self.app.get(url('group', id='patty'))
    #    self.assertIn('patty', response)

    ## new -> create #########################################################

    def test_new(self):
        response = self.app.get(url('new_group'))



    def test_create_invalid(self):
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username'     : 'fail_group' ,
                'name'         : 'p' ,
                'default_role' : 'fail_group' ,
                'join_mode'    : 'fail_group' ,
                'member_visibility'         : 'fail_group' ,
                'default_content_visibility': 'fail_group' ,
            },
            status=400
        )
        self.assertIn('invalid'     , response)
        self.assertIn('name'        , response)
        self.assertIn('default_role', response)
        self.assertIn('join_mode'   , response)
        self.assertIn('member_visibility', response)
        self.assertIn('default_content_visibility', response)








    def test_subtests(self):
        self.group_id = self.create_group(
            username          = 'test_group',
            name              = 'Test group for unit tests',
            description       = 'This group should not be visible once the tests have completed because it will be removed',
            join_mode                  = 'invite_and_request',
            default_role               = 'editor',
            member_visibility          = 'public',
            default_content_visibility = 'public',
        )

        self.subtest_create_invalid_groupname()
        self.subtest_edit()
        #self.subtest_update() # AllanC - TODO!!!! URGENT! Fails validation!!!!
        self.subtest_join_request()
        self.subtest_invite_join()
        self.subtest_setrole()
        self.subtest_delete()

        
        

    def subtest_create_invalid_groupname(self):
        # username duplicate
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username' : 'test_group',
            },
            status=400
        )
        self.assertIn('invalid' , response)
        self.assertIn('username', response)
        
        # username too short
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username' : 'a',
            },
            status=400
        )
        self.assertIn('invalid' , response)
        self.assertIn('username', response)

        # username invalid chars
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username' : '..hello..',
            },
            status=400
        )
        self.assertIn('invalid' , response)
        self.assertIn('username', response)




    ## edit -> update ########################################################
    
    def subtest_edit(self):
        
        response = self.app.get(url('edit_group', id=1       ), status=404)
        self.assertNotEqual(self.group_id, 0)
        response = self.app.get(url('settings', id='test_group', format="json"), status=200)
        self.assertIn('Test group for unit tests', response)
        self.log_out()
        response = self.app.get(url('settings', id='test_group'), status=302) # redirect to login page as not logged in
        self.log_in_as('unitfriend')
        response = self.app.get(url('settings', id='test_group'), status=403) # permission denied not a group admin

        self.log_out()


    def subtest_update(self):
        

        self.log_in_as('unittest')
        
        response = self.app.put(
            url('settings', id='test_group', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'name'         : 'Test group for unit tests (ALRIGHT!)' ,
                'default_role' : 'contributor' ,
            },
            #status=200
        )
        #log.debug(response)
        # appears to be a validation error? why? description is missing!! ? WHAT? description is not a required field.. wtf
        self.assertIn('ALRIGHT', response)
        self.assertNotIn('editor', response)
        self.assertIn('contributor', response)
        
    
    ## join request ############################################################
    
    def subtest_join_request(self):
        """
        Go though the process of requesting to join a group and the admin accepting the request
        """
        self.log_in_as('unittest')
        num_notifications = self.getNumNotifications()
        
        self.log_in_as('unitfriend')
        
        # Create a join request (as group is invite and request and unitfriend is not a member)
        self.join('test_group')
        
        self.log_out()
        
        # check member is actually part of group
        #   - member visibility is public so the join request should be visible even when viewed by a logged_out user
        response = self.app.get(url('group', id='test_group', format='json'))
        response_json = json.loads(response.body)
        found = False
        for member in response_json['data']['members']['items']:
            if member['username'] == 'unitfriend' and member['status']=='request':
                found = True
        self.assertTrue(found)
        
        self.log_in_as('unittest')
        self.assertEquals(num_notifications + 1, self.getNumNotifications()) # Check a request notification is generated for group members
        self.assertIn('unitfriend', self.getLastNotification().get('content')) 
        self.set_persona('test_group')
        # AllanC - groups dont recivce notifications at the moment (see issue #464)
        #self.assertIn('unitfriend', self.getLastNotification()) # Check a request notification is generated for group
        
        response = self.app.get(url('group', id='test_group', format='json'))
        self.assertIn('unitfriend', response)
        self.assertIn('request', response) # successful "join request" in member list
        
        # accept join request
        
        # AllanC - notification testing differed till later
        # num_notifications = self.getNumNotification() #issue 464
        response = self.app.post(
            url('group_action', action='set_role', id='test_group', format='json') ,
            params={
                '_authentication_token': self.auth_token ,
                'member': 'unitfriend',
            } ,
            status=200
        )
        # AllanC - issue #464
        #self.assertEqual(num_notifications + 1, self.getNumNotification()) # Check the group got notifyed of the new member
        #self.assertIn('unitfriend', self.getLastNotification())            # Check the notification was about unitfriend
        
        self.log_out()
        
        # check member is now part of group
        response = self.app.get(url('group', id='test_group', format='json'))
        response_json = json.loads(response.body)
        found = False
        for member in response_json['data']['members']['items']:
            if member['username'] == 'unitfriend' and member['status']=='active':
                found = True
        self.assertTrue(found)
        
        self.log_in_as('unittest') # AllanC - would be better to check group got notifcaiton as well .. see issue #464
        self.assertEqual(num_notifications + 2, self.getNumNotifications()) # Check the group got notifyed of the new member, the 2 messages are 'request to join' and 'new member'
        self.assertIn('unitfriend', self.getLastNotification().get('content')) # Check the notification was about unitfriend
    
    
    ## invite ############################################################
    
    def subtest_invite_join(self):
        pass
        # AllanC - TODO
        #warnings.warn("test not implemented")
        # must check notifications as well
    
    
    ## setrole ###############################################################
    
    def subtest_setrole(self):
        
        
        self.log_in_as('unittest')
        self.set_persona('test_group')
        
        # Cannot set own role as unittest is the only admin - error will be thrown
        response = self.app.post(
            url('group_action', action='set_role', id='test_group', format='json') ,
            params={
                '_authentication_token': self.auth_token ,
                'member': 'unittest',
                'role'  : 'editor',
            } ,
            status=400
        )
        self.assertIn('admin', response)
        
        # Upgrade 'unitfriend' to admin
        response = self.app.post(
            url('group_action', action='set_role', id='test_group', format='json') ,
            params={
                '_authentication_token': self.auth_token ,
                'member': 'unitfriend',
                'role'  : 'admin',
            } ,
            status=200
        )
        
        # Now downgrade self to observer
        response = self.app.post(
            url('group_action', action='set_role', id='test_group', format='json') ,
            params={
                '_authentication_token': self.auth_token ,
                'member': 'unittest',
                'role'  : 'observer',
            } ,
            status=200
        )
        
        # Try to upgrade self to editor after becoming an observer
        # NOTE: because the permissions check is done every load of base this permissions should take effect imediately
        # If we eveer just store role in the session then this test will fail because the user has not logged in and out to refresh the role
        response = self.app.post(
            url('group_action', action='set_role', id='test_group', format='json') ,
            params={
                '_authentication_token': self.auth_token ,
                'member': 'unittest',
                'role'  : 'editor',
            } ,
            status=403
        )
        
    
    
    ## delete ################################################################
    
    def subtest_delete(self):
        """
        As 'unitfriend' is now the only admin of the group they will remove it
        """
        
        
        #self.log_in_as('unittest')
        #self.set_persona('test_group')
        
        # Try deleting when logged in as 'unittest' ... should fail as 'unittest' is not an admin anymore
        response = self.app.post(
            url('group', id='test_group', format='json'),
            params={
                '_method': 'delete',
                '_authentication_token': self.auth_token
            },
            status=403
        )
        
        
        # AllanC - it appears that the delete cascades are slightly differnt for groups? .. got a server error 3/8/2011 14:00 - follower map?
        # Setup mutual follow for delete cascade
        #self.log_in_as('unitfriend')
        #self.set_persona('test_group')
        #self.follow('kitten')
        #self.log_in_as('kitten')
        #self.follow('test_group')
        # humm ... this appears to work .. will create a dedicated cascade test to do this
        
        self.log_in_as('unitfriend')
        self.set_persona('test_group')
        
        response = self.app.post(
            url('group', id='test_group', format='json'),
            params={
                '_method': 'delete',
                '_authentication_token': self.auth_token
            },
            status=200
        )
        
        self.log_out()
        
        # The group should not exist
        response = self.app.get(url('group', id='test_group', format='json'), status=404)
