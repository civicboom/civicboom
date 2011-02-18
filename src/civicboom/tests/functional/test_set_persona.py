from civicboom.tests import *

class TestSetPersonaController(TestController):
    
    def test_set_persona(self):
        self.log_in_as('unittest')
        
        # Create Group
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username'     : 'set_persona_test',
                'name'         : 'Set Persona Test Group' ,
                'description'  : 'This group should not be visible once the tests have completed because it will be removed' ,
                'default_role' : 'editor' ,
                'join_mode'    : 'invite_and_request' ,
                'member_visibility'         : 'public' , #required to test join request later
                'default_content_visibility': 'public' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        assert response_json['data']['id'] > 0


        # Set Persona to new group
        response = self.app.post(
            url(controller='account', action='set_persona', id='set_persona_test',format='json'),
            params={
                '_authentication_token': self.auth_token,
            },
            status=200
        )
        response_json = json.loads(response.body)

        # Set Persona to group that does not exisit
        response = self.app.post(
            url(controller='account', action='set_persona', id='set_persona_test_not_exists',format='json'),
            params={
                '_authentication_token': self.auth_token,
            },
            status=403
        )
        response_json = json.loads(response.body)

        # Set Persona to user
        response = self.app.post(
            url(controller='account', action='set_persona', id='unitfriend',format='json'),
            params={
                '_authentication_token': self.auth_token,
            },
            status=403
        )
        response_json = json.loads(response.body)

        # Log in as unitfriend
        self.log_in_as('unitfriend')
        
        # Create Group as unitfriend
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username'     : 'set_persona_test2',
                'name'         : 'Set Persona Test Group2' ,
                'description'  : 'This group should not be visible once the tests have completed because it will be removed' ,
                'default_role' : 'editor' ,
                'join_mode'    : 'invite_and_request' ,
                'member_visibility'         : 'public' , #required to test join request later
                'default_content_visibility': 'public' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        assert response_json['data']['id'] > 0

        # Invite - unittest
        response = self.app.post(
            url('group_action', action='invite', id='set_persona_test2', format='json') ,
            params={
                '_authentication_token': self.auth_token,
                'member': 'unittest'
            },
            status=200
        )
        response_json = json.loads(response.body)

        self.log_in_as('unittest')

        # Set Persona to unitfriends group (this should error as user is not an active menber)
        response = self.app.post(
            url(controller='account', action='set_persona', id='set_persona_test2',format='json'),
            params={
                '_authentication_token': self.auth_token,
            },
            status=403
        )
        response_json = json.loads(response.body)


        self.log_in_as('unitfriend')

        # Uninvite - unittest
        response = self.app.post(
            url('group_action', action='remove_member', id='set_persona_test2', format='json') ,
            params={
                '_authentication_token': self.auth_token,
                'member': 'unittest'
            },
            status=200
        )
        response_json = json.loads(response.body)
        

        self.log_in_as('unittest')

        # Set Persona to unitfriends group (this should error as user is not a menber)
        response = self.app.post(
            url(controller='account', action='set_persona', id='set_persona_test2',format='json'),
            params={
                '_authentication_token': self.auth_token,
            },
            status=403
        )
        response_json = json.loads(response.body)
        
        
        #Delete Groups

        response = self.app.delete(
            url('group', id='set_persona_test', format="json"),
            params={
                '_authentication_token': self.auth_token
            },
            status=200
        )

        self.log_in_as('unitfriend')        
        response = self.app.delete(
            url('group', id='set_persona_test2', format="json"),
            params={
                '_authentication_token': self.auth_token
            },
            status=200
        )

