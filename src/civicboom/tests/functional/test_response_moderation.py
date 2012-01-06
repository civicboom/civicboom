from civicboom.tests import *

from nose.plugins.skip import SkipTest


class TestResponseModeration(TestController):
    
    def test_response_moderation(self):
        """
        Create a response private request
        Respond multiple times with multiple members
        Check the moderated items
        """
        #raise SkipTest("ResponseModeration not completed")
        
        # Setup ----------------------------------------------------------------
        
        
        
        # Request --------------------------------------------------------------
        
        # Create "moderate_required" request
        self.log_in_as('unittest')
        request_id = self.create_content('response_moderate test request', 'an autoamted test to test the flow of response private, responses should not be visible to anyone', type='assignment', responses_require_moderation=True)
        
        
        # Response -------------------------------------------------------------
        #  multiple times by multiple users
        self.log_in_as('unitfriend')
        response_id_1 = self.create_content('response_moderate test response1', 'response1', parent_id=request_id)
        
        self.log_in_as('kitten')
        response_id_2 = self.create_content('response_moderate test response2', 'response2', parent_id=request_id)
        
        
        # Check response visibility --------------------------------------------
        
        # anon users cant see them
        self.log_out()
        response_list = [content['id'] for content in self.get_content(request_id)['responses']['items']]
        for id in [response_id_1, response_id_2]:
            self.assertNotIn(id, response_list)
        
        # The response has the parent still listed
        self.assertEquals(request_id, self.get_content(response_id_1)['content']['parent_id'])
        
        # Requet creator can see them in response list
        self.log_in_as('unittest')
        response_list = [content['id'] for content in self.get_content(request_id)['responses']['items']]
        for id in [response_id_1, response_id_2]:
            self.assertIn(id, response_list)
        
        
        # Moderate -------------------------------------------------------------
        
        self.log_in_as('unittest')
        
        # approve response 1
        response = self.app.post(
            url('content_action', action='approve', id=response_id_1, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        # seen response 2
        response = self.app.post(
            url('content_action', action='seen', id=response_id_2, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        
        # Check response visibility --------------------------------------------
        
        self.log_out()
        response_list = [content['id'] for content in self.get_content(request_id)['responses']['items']]
        for id in [response_id_1, response_id_2]:
            self.assertIn(id, response_list)
        
        
        # Cleanup --------------------------------------------------------------
        
        self.delete_content(request_id   , force=True)
        self.delete_content(response_id_1, force=True)
        self.delete_content(response_id_2, force=True)


# old view check stuff
        
        # No need for trusted checks because the 
        #self.sign_up_as('unittest_trusted_follower')
        #self.follow('unittest', trusted=True)
        #self.sign_up_as('unitfriend_trusted_follower')
        #self.follow('unitfriend', trusted=True)
        
        #self.view_content(request_id, 'unittest'                 , can_view=True)
        #self.view_content(request_id, 'unittest_trusted_follower', can_view=True)
        #self.view_content(request_id, False                      , can_view=True)
        
        # Check the correct view for each user
        #self.view_content(response_id_1, 'unittest'                   , can_view=True )
        #self.view_content(response_id_1, 'unitfriend'                 , can_view=True )
        #self.view_content(response_id_1, 'unittest_trusted_follower'  , can_view=False)
        #self.view_content(response_id_1, 'unitfriend_trusted_follower', can_view=False)
        #self.view_content(response_id_1, False                        , can_view=False)
        #self.view_content(response_id_2, 'unittest'                   , can_view=True )
        #self.view_content(response_id_2, 'unitfriend'                 , can_view=False)
        
        
        # Check the correct view for each user
        #self.view_content(response_id_1, 'unittest'                   , can_view=True )
        #self.view_content(response_id_1, 'unitfriend'                 , can_view=True )
        #self.view_content(response_id_1, 'unittest_trusted_follower'  , can_view=True )
        #self.view_content(response_id_1, False                        , can_view=True )
        
        #self.assertEquals(self.get_content(response_id_2)['data']['content']['parent_id'], None)
        #self.view_content(response_id_2, 'unittest'                   , can_view=True )
        #self.view_content(response_id_2, 'unitfriend'                 , can_view=True )
        
        #self.delete_member('unittest_trusted_follower')
        #self.delete_member('unitfriend_trusted_follower')