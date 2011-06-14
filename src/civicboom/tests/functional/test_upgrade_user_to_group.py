from civicboom.tests import *

from civicboom.lib.database.get_cached import get_member


class TestUpgradeUserToGroup(TestController):

    def test_upgrade(self):
        """
        Create new user
        Upgrade user to group
        
        Login as converted new user
        check group membership
        """
        # Create new user_to_group user
        self.sign_up_as('user_to_group')
        self.log_out()
        
        # Call admin upgrade call
        response = self.app.post(
            url(controller='test', action='upgrade_user_to_group'),
            params={
                'member_to_upgrade_to_group': u'user_to_group',
                'new_admins_username'       : u'user_of_group',
            },
        )
        
        # Check login record transfered
        self.log_in_as('user_of_group')
        
        # Check member is admin of group
        response      = self.app.get(url(controller='profile', action='index', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEquals(response_json['data']['groups']['count'], 1)
        self.assertEquals(response_json['data']['groups']['items'][0]['username'], 'user_to_group')
        self.assertEquals(response_json['data']['groups']['items'][0]['role']    , 'admin'        )
        
        self.set_persona('user_to_group')
        
        # Delete and cleanup group and member
        response = self.app.delete(
            url('group', id='user_to_group', format='json'),
            params={
                '_authentication_token': self.auth_token
            },
            status=200
        )
        member = get_member('user_of_group')
        member.delete()
