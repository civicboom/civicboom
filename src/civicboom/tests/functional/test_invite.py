from civicboom.tests import *
#import json


class TestInviteController(TestController):
    
    def test_all(self):
        self.sign_up_as("invite_test_user")
        self.sign_up_as("invite_test_user_tfollower")
        self.part_create_private_group()
        self.part_create_private_assignment()
        self.part_create_private_content()
        
        self.part_invite_fails()
        
        self.part_check_assignment_content_group()
        self.part_invite_assignment()
        self.part_invite_group()
        self.part_invite_trusted_follower()
        
    def part_create_private_group(self):
        self.log_in_as('unittest')
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username'     : 'test_private_group',
                'name'         : 'Test private group for unit tests' ,
                'description'  : 'This group should not be visible once the tests have completed because it will be removed' ,
                'default_role' : 'editor' ,
                'join_mode'    : 'invite' ,
                'member_visibility'         : 'public' , #required to test join request later
                'default_content_visibility': 'private' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        self.group_id = int(response_json['data']['id'])
        
        self.log_in_as("invite_test_user")
        
        response = self.app.post(
            url('group_action', action='join', id='test_private_group', format='json') ,
            params={
                '_authentication_token': self.auth_token   ,
            },
            status=403,
        )
    
    def part_create_private_assignment(self):
        self.log_in_as('unittest')
        self.set_persona('test_private_group')
        self.set_account_type('free') # Because of #513 groups are now created with the account of there parent - we need to reset the account type to free for the next test to fail
        # Should fail to post as this group does not have a 'plus' account - validation will fail on content being default 'private'
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "A test private assignment for test_private_group",
                'type': "assignment",
                'content': "This is my private assignment.",
                'license': 'CC-BY',
                'location': "1.0707 51.2999",
            },
            status=400
        )
        self.set_account_type('plus')
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "A test private assignment for test_private_group",
                'type': "assignment",
                'content': "This is my private assignment.",
                'license': 'CC-BY',
                'location': "1.0707 51.2999",
            },
            status=201
        )
        
        self.my_assignment_id = json.loads(response.body)["data"]["id"]
    
    def part_create_private_content(self):
        self.log_in_as('unittest')
        self.set_persona('test_private_group')
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "A test private article for test_private_group",
                'type': "article",
                'content': "This is my private article.",
                'license': 'CC-BY',
                'location': "1.0707 51.2999",
            },
            status=201
        )
        self.my_article_id = json.loads(response.body)["data"]["id"]
    
    def part_check_assignment_content_group(self):
        self.log_in_as('invite_test_user')
        response = self.app.get(url('content', id=self.my_article_id,   _authentication_token=self.auth_token), status=403)
        response = self.app.get(url('content', id=self.my_assignment_id,_authentication_token=self.auth_token), status=403)
        
    def part_invite_fails(self):
        self.log_in_as('unittest')
        self.set_persona('test_private_group')
        # Test parameters required
        response = self.app.get(
            '/invite',
            params={
                '_authentication_token': self.auth_token,
                'invite': 'assignment',
                'format': 'json',
            },
            status=500
        )
        response = self.app.get(
            '/invite',
            params={
                '_authentication_token': self.auth_token,
                'id': 'unknown',
                'format': 'json',
            },
            status=500
        )
        # Test 404
        response = self.app.get(
            '/invite',
            params={
                '_authentication_token': self.auth_token,
                'invite': 'assignment',
                'id': '99999',
                'format': 'json',
            },
            status=404
        )
        # Test 403 No Permission
        response = self.app.get(
            '/invite',
            params={
                '_authentication_token': self.auth_token,
                'invite': 'group',
                'id': 'unittest',
                'format': 'json',
            },
            status=403
        )
        # Test invite to group unittest (wrong type)
        self.set_persona('unittest')
        response = self.app.get(
            '/invite',
            params={
                '_authentication_token': self.auth_token,
                'invite': 'group',
                'id': 'me',
                'format': 'json',
            },
            status=403
        )
        # Test invite no permission
        response = self.app.get(
            '/invite',
            params={
                '_authentication_token': self.auth_token,
                'invite': 'group',
                'id': 'test_private_group',
                'format': 'json',
            },
            status=403
        )
        response = self.app.get(
            '/invite',
            params={
                '_authentication_token': self.auth_token,
                'invite': 'assignment',
                'id': self.my_assignment_id,
                'format': 'json',
            },
            status=403
        )
        response = self.app.get(
            '/invite',
            params={
                '_authentication_token': self.auth_token,
                'invite': 'trusted_follower',
                'id': 'test_private_group',
                'format': 'json',
            },
            status=403
        )

    
    def part_invite_assignment(self):
        self.log_in_as('invite_test_user')
        self.notifs_invite = self.getNumNotifications()
        response = self.app.get(
            url('content', id=self.my_assignment_id),
            status=403,
        )
        self.log_in_as('unittest')
        self.set_persona('test_private_group')
        self.invite_user_to('assignment', self.my_assignment_id, 'invite_test_user')
        
        self.log_in_as('invite_test_user')
        assert self.getNumNotifications() == self.notifs_invite + 1
        response = self.app.get(
            url('content', id=self.my_assignment_id),
            status=200,
        )
        
    def part_invite_group(self):
        self.log_in_as('invite_test_user')
        self.notifs_invite = self.getNumNotifications()
        response = self.app.get(
            url('content', id=self.my_article_id),
            status=403,
        )
        self.log_in_as('unittest')
        self.set_persona('test_private_group')
        self.invite_user_to('group', 'me', 'invite_test_user')
        
        self.log_in_as('invite_test_user')
        assert self.getNumNotifications() == self.notifs_invite + 1
        
        response = self.app.get(
            url('member', id='test_private_group', format="json"),
            status=200,
        )
        response_json = json.loads(response.body)
        me_in_group = None
        for member in response_json['data']['members']['items']:
            if member['username'] == 'invite_test_user':
                me_in_group = member
        assert me_in_group != None
        assert me_in_group['status'] == 'invite'
        
        self.join('test_private_group')
        
        response = self.app.get(
            url('member', id='test_private_group', format="json"),
            status=200,
        )
        response_json = json.loads(response.body)
        me_in_group = None
        for member in response_json['data']['members']['items']:
            if member['username'] == 'invite_test_user':
                me_in_group = member
        assert me_in_group != None
        assert me_in_group['status'] == 'active'
        
        self.set_persona('test_private_group')
        
        response = self.app.get(url('content', id=self.my_article_id), status=200)
        
    def part_invite_trusted_follower(self):
        self.log_in_as('invite_test_user_tfollower')
        self.notifs_invite = self.getNumNotifications()
        response = self.app.get(
            url('content', id=self.my_article_id),
            status=403,
        )
        self.log_in_as('unittest')
        self.set_persona('test_private_group')
        self.invite_user_to('trusted_follower', 'me', 'invite_test_user_tfollower')
        
        self.log_in_as('invite_test_user_tfollower')
        assert self.getNumNotifications() == self.notifs_invite + 1
        
        response = self.app.get(url('content', id=self.my_article_id), status=403)
        
        response = self.app.get(
            url('member', id='test_private_group', format="json"),
            status=200,
        )
        response_json = json.loads(response.body)
        
        assert 'follow' in response_json['data']['actions'] and 'unfollow' in response_json['data']['actions']
        
        self.follow('test_private_group')
        
        response = self.app.get(
            url('content', id=self.my_article_id),
            status=200,
        )
        #response
