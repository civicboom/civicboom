from civicboom.tests import *

#import json
import warnings

#self.group_id = 0

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







    def test_subtests(self):
        self.subtest_create()
        self.subtest_create_invalid()
        self.subtest_create_invalid_groupname()
        self.subtest_edit()
        #self.subtest_update() # AllanC - TODO!!!! URGENT! Fails validation!!!!
        self.subtest_join_request()
        self.subtest_invite_join()
        self.subtest_setrole()
        self.subtest_delete()

    def subtest_create(self):
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username'     : 'test_group',
                'name'         : 'Test group for unit tests' ,
                'description'  : 'This group should not be visible once the tests have completed because it will be removed' ,
                'default_role' : 'editor' ,
                'join_mode'    : 'invite_and_request' ,
                'member_visibility'         : 'public' , #required to test join request later
                'default_content_visibility': 'public' ,
            },
            status=201
        )
        c = json.loads(response.body)
        #
        self.group_id = int(c['data']['id'])
        self.assertNotEqual(self.group_id, 0)
        
        response = self.app.get(url('group', id=self.group_id, format='json'))
        response_json = json.loads(response.body)
        self.assertEqual(response_json['data']['member']['username']                  , 'test_group')
        self.assertEqual(response_json['data']['member']['join_mode']                 , 'invite_and_request')
        self.assertEqual(response_json['data']['member']['default_role']              , 'editor')
        self.assertEqual(response_json['data']['member']['member_visibility']         , 'public')
        self.assertEqual(response_json['data']['member']['default_content_visibility'], 'public' )
        
        

    def subtest_create_invalid(self):
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
        response = self.app.get(url('edit_group', id=self.group_id), status=200)
        self.assertIn('test_group', response)
        self.log_out()
        response = self.app.get(url('edit_group', id=self.group_id), status=302) # redirect to login page as not logged in
        self.log_in_as('unitfriend')
        response = self.app.get(url('edit_group', id=self.group_id), status=403) # permission denied not a group admin

        self.log_out()


    def subtest_update(self):
        

        self.log_in_as('unittest')
        
        response = self.app.put(
            url('group', id=self.group_id, format='json'),
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
        
        
        self.log_in_as('unitfriend')
        
        # Create a join request (as group is invite and request and unitfriend is not a member)
        response = self.app.post(
            url('group_action', action='join', id=self.group_id, format='json') ,
            params={
                '_authentication_token': self.auth_token ,
                'member': 'unittest',
            },
            status=200,
        )
        self.assertIn('request', response) # successful "join request" in response
        
        self.log_out()
        
        # check member is actually part of group
        #   - member visibility is public so the join request should be visible even when viewed by a logged_out user
        response = self.app.get(url('group', id=self.group_id, format='json'))
        response_json = json.loads(response.body)
        found = False
        for member in response_json['data']['members']['items']:
            if member['username'] == 'unitfriend' and member['status']=='request':
                found = True
        self.assertTrue(found)
        
        self.log_in_as('unittest')
        
        response = self.app.get(url('group', id=self.group_id, format='json'))
        self.assertIn('unitfriend', response)
        self.assertIn('request', response) # successful "join request" in member list
        
        # accept join request
        response = self.app.post(
            url('group_action', action='set_role', id=self.group_id, format='json') ,
            params={
                '_authentication_token': self.auth_token ,
                'member': 'unitfriend',
            } ,
            status=200
        )

        self.log_out()
        
        # check member is now part of group
        response = self.app.get(url('group', id=self.group_id, format='json'))
        response_json = json.loads(response.body)
        found = False
        for member in response_json['data']['members']['items']:
            if member['username'] == 'unitfriend' and member['status']=='active':
                found = True
        self.assertTrue(found)
    
    
    ## invite ############################################################
    
    def subtest_invite_join(self):
        # AllanC - TODO
        warnings.warn("test not implemented")
    
    
    ## setrole ###############################################################
    
    def subtest_setrole(self):
        
        
        self.log_in_as('unittest')
        
        # Cannot set own role as unittest is the only admin - error will be thrown
        response = self.app.post(
            url('group_action', action='set_role', id=self.group_id, format='json') ,
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
            url('group_action', action='set_role', id=self.group_id, format='json') ,
            params={
                '_authentication_token': self.auth_token ,
                'member': 'unitfriend',
                'role'  : 'admin',
            } ,
            status=200
        )
        
        # Now downgrade self to observer
        response = self.app.post(
            url('group_action', action='set_role', id=self.group_id, format='json') ,
            params={
                '_authentication_token': self.auth_token ,
                'member': 'unittest',
                'role'  : 'observer',
            } ,
            status=200
        ) 
        
    
    
    ## delete ################################################################
    
    def subtest_delete(self):
        """
        As 'unitfriend' is now the only admin of the group they will remove it
        """
        
        
        self.log_in_as('unittest')
        
        # Try deleting when logged in as 'unittest' ... should fail as 'unittest' is not an admin anymore
        response = self.app.delete(
            url('group', id=self.group_id, format="json"),
            params={
                '_authentication_token': self.auth_token
            },
            status=403
        )
        
        self.log_in_as('unitfriend')
        
        response = self.app.delete(
            url('group', id=self.group_id, format="json"),
            params={
                '_authentication_token': self.auth_token
            },
            status=200
        )
        
        self.log_out()
        
        # The group should not exist
        response = self.app.get(url('group', id=self.group_id, format='json'), status=404)
