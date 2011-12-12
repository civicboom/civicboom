from civicboom.tests import *

from nose.plugins.skip import SkipTest


class TestResponseModeration(TestController):
    
    def test_response_moderation(self):
        """
        Create a response private request
        Respond multiple times with multiple members
        Check the correct members can view the responsonses at the correct times
        """
        raise SkipTest("ResponseModeration not completed")
        
        # Setup ----------------------------------------------------------------
        self.sign_up_as('unittest_trusted_follower')
        self.follow('unittest', trusted=True)
        
        self.sign_up_as('unitfriend_trusted_follower')
        self.follow('unitfriend', trusted=True)
        
        
        # Request --------------------------------------------------------------
        
        # Create "Response Private" request
        self.log_in_as('unittest')
        request_id = self.create_content('response_private test', 'an autoamted test to test the flow of response private, responses should not be visible to anyone', type='assignment', response_private=True)
        
        self.view_content(request_id, 'unittest'                 , can_view=True)
        self.view_content(request_id, 'unittest_trusted_follower', can_view=True)
        self.view_content(request_id, False                      , can_view=True)
        
        
        # Response -------------------------------------------------------------
        #  multiple times by multiple users
        self.log_in_as('unitfriend')
        response_id_1 = self.create_content('response_private test response1', 'response1')
        
        self.log_in_as('kitten')
        response_id_2 = self.create_content('response_private test response2', 'response2')
       
        self.log_in_as('unittest')
       
        # Check the correct view for each user
        self.view_content(response_id_1, 'unittest'                   , can_view=True )
        self.view_content(response_id_1, 'unitfriend'                 , can_view=True )
        self.view_content(response_id_1, 'unittest_trusted_follower'  , can_view=False)
        self.view_content(response_id_1, 'unitfriend_trusted_follower', can_view=False)
        self.view_content(response_id_1, False                        , can_view=False)
        
        self.view_content(response_id_2, 'unittest'                   , can_view=True )
        self.view_content(response_id_2, 'unitfriend'                 , can_view=False)
        
        
        # Moderate -------------------------------------------------------------
        
        # approve response 1
        response = self.app.post(
            url('content_action', action='approve', id=response_id_1, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        # Moderate and disasociate response 2
        response = self.app.post(
            url('content_action', action='disassociate', id=response_id_2, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        
        # Check the correct view for each user
        self.view_content(response_id_1, 'unittest'                   , can_view=True )
        self.view_content(response_id_1, 'unitfriend'                 , can_view=True )
        self.view_content(response_id_1, 'unittest_trusted_follower'  , can_view=True )
        self.view_content(response_id_1, False                        , can_view=True )
        
        self.assertEquals(self.get_content(response_id_2)['data']['content']['parent_id'], None)
        self.view_content(response_id_2, 'unittest'                   , can_view=True )
        self.view_content(response_id_2, 'unitfriend'                 , can_view=True )
        
        
        # Cleanup --------------------------------------------------------------
        
        self.delete_member('unittest_trusted_follower')
        self.delete_member('unitfriend_trusted_follower')
        self.delete_content(request_id   , force=True)
        self.delete_content(response_id_1, force=True)
        self.delete_content(response_id_2, force=True)
