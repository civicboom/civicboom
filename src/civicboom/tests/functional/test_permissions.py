from civicboom.tests import *

from nose.plugins.skip import SkipTest


class TestPermissionsController(TestController):
    
    def test_action_permissions(self):
        raise SkipTest("Not implemented")
        """
        test actions
         - follow
         - unfollow
         - accept
         - withdraw
        """
    
    
    def test_persona_permissions(self):
        """
        Test content persona publishing permission rules
        other tests handle the rules for the 'individual user' publishing
        this test specifically tests the permissions for an active group persona
        """
        # SETUP ----------------------------------------------------------------
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username'     : 'publish_permission_test',
                'name'         : 'Publish content permission test group' ,
                'description'  : 'This group should not be visible once the tests have completed because it will be removed' ,
                'default_role'              : 'observer'    ,
                'join_mode'                 : 'public'      ,
                'member_visibility'         : 'public'      ,
                'default_content_visibility': 'public'      ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        self.assertNotEqual(response_json['data']['id'], 0)
        
        self.set_persona('publish_permission_test')
        
        # Create draft as group persona
        draft_id = self.create_content(
            title   = 'permission draft 1',
            content = 'a test draft'      ,
            type    = 'draft'             ,
        )
        
        self.log_in_as('unitfriend')
        
        # TODO: comment on private draft should be rejected as member does not have permission to see parent conent
        ## hummm self.comment(draft_id, 'permission comment')
        
        # User should NOT see draft as it's private
        response      = self.app.get(url('member', id='publish_permission_test', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertNotIn("permission draft 1", response)
        
        self.join(       'publish_permission_test')
        
        
        # OBSERVER -------------------------------------------------------------
        
        self.set_persona('publish_permission_test')
        
        # User should see draft as it's private
        #response      = self.app.get(url('member', id='publish_permission_test', format='json'), status=200)
        #response_json = json.loads(response.body)
        #self.assertIn("permission draft 1", response)
        
        # Create draft as group persona - should be rejected because role is observer
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title'  : "permission draft 2",
                'content': "a test draft",
            },
            status=403
        )
        
        # comment on draft
        self.comment(draft_id, 'permission comment')
        
        
        # CONTRIBUTOR ----------------------------------------------------------
        
        # set unitfriend role 'contributor'
        self.log_in_as('unittest')
        self.set_persona('publish_permission_test')
        response = self.app.post(
            url('group_action', action='set_role', id='publish_permission_test', format='json') ,
            params={
                '_authentication_token': self.auth_token ,
                'member': 'unitfriend'  ,
                'role'  : 'contributor' ,
            } ,
            status=200
        )
        
        # Test 'contributor'
        self.log_in_as('unitfriend')
        self.set_persona('publish_permission_test')
        
        # Create draft as group persona - should be rejected because role is observer
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title'  : "permission draft 2",
                'content': "a test draft"      ,
                'type'   : "draft"             ,
            },
            status=201
        )
        draft_id = json.loads(response.body)["data"]["id"]
        self.assertGreater(draft_id, 0)
        
        # Upgrade draft to article - rejected
        response = self.app.post(
            url('content', id=draft_id, format="json"),
            params={
                '_authentication_token': self.auth_token,
                '_method'       : 'PUT'               ,
                'title'         : "permission article",
                'content'       : "a test update"     ,
                'type'          : "article"           ,
                #'submit_publish': u'publish'          ,
            },
            status=403
        )
        
        # Create article as group persona - should be rejected because role is contributor
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title'         : "permission article",
                'content'       : "a test "           ,
                'type'          : "article"           ,
                #'submit_publish': u'publish'          ,
            },
            status=403
        )
        
        # EDITOR ---------------------------------------------------------------
        
        # set unitfriend role 'editor'
        self.log_in_as('unittest')
        self.set_persona('publish_permission_test')
        response = self.app.post(
            url('group_action', action='set_role', id='publish_permission_test', format='json') ,
            params={
                '_authentication_token': self.auth_token ,
                'member': 'unitfriend'  ,
                'role'  : 'editor' ,
            } ,
            status=200
        )
        
        # Test 'editor'
        self.log_in_as('unitfriend')
        self.set_persona('publish_permission_test')
        
        # Comments on the draft
        self.comment(draft_id, 'permission comment')
        
        # Create article as group persona - should be accepted because role is editor
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title'         : "permission article",
                'content'       : "a test "           ,
                'type'          : "article"           ,
                #'submit_publish': u'publish'          ,
            },
            status=201
        )
        
        # Should NOT be able to view settings
        response = self.app.get(url('settings', format="json"), status=403)
        
        
        # ADMIN ----------------------------------------------------------------
        
        # set unitfriend role 'admin'
        self.log_in_as('unittest')
        self.set_persona('publish_permission_test')
        response = self.app.post(
            url('group_action', action='set_role', id='publish_permission_test', format='json') ,
            params={
                '_authentication_token': self.auth_token ,
                'member': 'unitfriend'  ,
                'role'  : 'admin' ,
            } ,
            status=200
        )
        
        # Test 'admin'
        self.log_in_as('unitfriend')
        self.set_persona('publish_permission_test')
        
        # Should be able to view settings
        response = self.app.get(url('settings', format="json"), status=200)
        
        
        # CLEANUP --------------------------------------------------------------
        
        self.log_in_as('unittest')
        self.set_persona('publish_permission_test')
        
        response = self.app.post(
            url('group', id='publish_permission_test', format="json"),
            params={
                '_method': 'delete',
                '_authentication_token': self.auth_token
            },
            status=200
        )


    #---------------------------------------------------------------------------
    # Priavte Content Viewing
    #---------------------------------------------------------------------------

    def test_private_content_viewing_permissions(self):
        # Tests GregM - moved from test_contents by AllanC
        
        # Create accounts & setup to test private content ----------------------
        self.sign_up_as("private_content_trusted")
        self.sign_up_as("private_content_untrusted")
        self.sign_up_as("private_content_nonfollower")
        self.log_in_as("private_content_trusted")
        self.follow("unittest")
        self.log_in_as("private_content_untrusted")
        self.follow("unittest")
        
        self.log_in_as("unittest")
        # GregM: Trust one follower
        self.follower_trust("private_content_trusted")
        
        # Create private content -----------------------------------------------
        #self.log_in_as("unittest")
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "A test private article by the test user",
                'type': "article",
                'content': "This is my private article.",
                'license': 'CC-BY',
                'location': "1.0707 51.2999",
                'private': True,
            },
            status=201
        )
        self.my_private_article_id = json.loads(response.body)["data"]["id"]
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "A test private assignment by the test user",
                'type': "article",
                'content': "This is my private assignment.",
                'license': 'CC-BY',
                'location': "1.0707 51.2999",
                'private': True,
            },
            status=201
        )
        self.my_private_assignment_id = json.loads(response.body)["data"]["id"]
        
        # view_private_content_not_trusted -------------------------------------
        self.log_in_as("private_content_untrusted")
        response = self.app.get(url('content', id=self.my_private_article_id), status=403)
        response = self.app.get(url('content', id=self.my_private_assignment_id), status=403)
        self.log_in_as("private_content_nonfollower")
        response = self.app.get(url('content', id=self.my_private_article_id), status=403)
        response = self.app.get(url('content', id=self.my_private_assignment_id), status=403)
        
        # view_private_content_trusted -----------------------------------------
        self.log_in_as("private_content_trusted")
        response = self.app.get(url('content', id=self.my_private_article_id), status=200)
        response = self.app.get(url('content', id=self.my_private_assignment_id), status=200)
        
        # distrust_check -------------------------------------------------------
        self.log_in_as("unittest")
        self.follower_distrust("private_content_trusted")
        self.log_in_as("private_content_trusted")
        response = self.app.get(url('content', id=self.my_private_article_id), status=403)
        response = self.app.get(url('content', id=self.my_private_assignment_id), status=403)
        self.log_in_as("unittest")
        self.follower_trust("private_content_trusted")
        response = self.app.get(url('content', id=self.my_private_article_id), status=200)
        response = self.app.get(url('content', id=self.my_private_assignment_id), status=200)


    #---------------------------------------------------------------------------
    # Plus Services Permissions
    #---------------------------------------------------------------------------
    
    def test_approve_disasociate_permissions(self):
        raise SkipTest("Not implemented")
