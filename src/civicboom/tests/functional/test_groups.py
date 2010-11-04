from civicboom.tests import *

class TestGroupsController(TestController):

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


    def test_create_invalid_duplicate_groupname(self):
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

    def test_create_invalid_groupname(self):
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

    def test_create_invalid_groupname2(self):
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
    
    ## delete ################################################################