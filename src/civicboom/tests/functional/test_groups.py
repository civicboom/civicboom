from civicboom.tests import *

import json

group_id = 0

class TestGroupsController(TestController):

    #group_id = 0

    ## index -> show #########################################################

    def test_group_page(self):
        response = self.app.get(url('group', id='patty', format='json'))
        assert 'patty' in response

    def test_group_page_html(self):
        response = self.app.get(url('group', id='patty'))
        assert 'patty' in response

    ## new -> create #########################################################

    def test_new(self):
        response = self.app.get(url('new_group'))
        
    def test_create(self):
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username'     : 'test_group',
                'name'         : 'Test group for unit tests' ,
                'description'  : 'This group should not be visable once the tests have completed because it will be removed' ,
                'default_role' : 'editor' ,
                'join_mode'    : 'invite_and_request' ,
                'member_visability'         : 'private' ,
                'default_content_visability': 'public' ,
            },
            status=201
        )
        print response.body
        c = json.loads(response.body)
        global group_id
        group_id = int(c['data']['id'])
        assert group_id > 0
        

    def test_create_invalid(self):
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username'     : 'fail_group' ,
                'name'         : 'p' ,
                'default_role' : 'fail_group' ,
                'join_mode'    : 'fail_group' ,
                'member_visability'         : 'fail_group' ,
                'default_content_visability': 'fail_group' ,
            },
            status=400
        )
        assert 'invalid'      in response
        assert 'name'         in response
        assert 'default_role' in response
        assert 'join_mode'    in response
        assert 'member_visability' in response
        assert 'default_content_visability' in response



    def test_create_invalid_groupname(self):
        # username duplicate
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username' : 'test_group',
            },
            status=400
        )
        assert 'invalid'  in response
        assert 'username' in response
        
        # username too short
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username' : 'a',
            },
            status=400
        )
        assert 'invalid'  in response
        assert 'username' in response

        # username invalid chars
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username' : '..hello..',
            },
            status=400
        )
        assert 'invalid'  in response
        assert 'username' in response




    ## edit -> update ########################################################
    
    def test_edit(self):
        response = self.app.get(url('edit_group', id=1       ), status=404)
        global group_id
        assert group_id > 0
        response = self.app.get(url('edit_group', id=group_id), status=200)
        assert 'test_group' in response
        self.log_out()
        response = self.app.get(url('edit_group', id=group_id), status=302) # redirect to login page as not logged in
        self.log_in_as(u'unitfriend')
        response = self.app.get(url('edit_group', id=group_id), status=403) # permission denied not a group admin

    def test_update(self):
        global group_id
        response = self.app.put(
            url('group', id=group_id, format='json'),
            params={
                '_authentication_token': self.auth_token,
                'name'         : 'Test group for unit tests (ALRIGHT!)' ,
                'default_role' : 'contributor' ,
            },
            #status=200
        )
        print response
        # appears to be a validation error? why? description is missing!! ? WHAT? description is not a required field.. wtf
        assert 'ALRIGHT' in response
        assert 'editor' not in response
        assert 'contributor' in response
    
    
    ## invite -> join -> join request ########################################
    
    def test_join_invite_request(self):
        self.log_out()
        self.log_in_as('unitfriend')
        
        # Create a join request (as group is invite and request and unitfriend is not a member)
        response = self.app.post(
            url('group_action', action='join', id=group_id, format='json') ,
            params={
                '_authentication_token': self.auth_token ,
                'member': 'unittest',
            },
            status=200,
        )
        assert 'request' in response # successful "join request" in response
        
    
    ## setrole ###############################################################
    
    def test_setrole(self):
        global group_id
        response = self.app.post(
            url('group_action', action='set_role', id=group_id, format='json') ,
            params={
                '_authentication_token': self.auth_token ,
                'member': 'unittest',
                'role'  : 'editor'
            } ,
            status=400
        ) # Cannot remove last admin error to be thrown
        assert 'admin' in response
    
    
    ## delete ################################################################
    
    