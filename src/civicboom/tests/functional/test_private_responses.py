from civicboom.tests import *


class TestPrivateResponse(TestController):
    
    def test_private_response_list(self):
        """
        Create a private request
        
        User A Create a private assignment
        User B responds
        User A should see the response in list in the request return
        
        User C is a trusted follower of user B
        User C INCORRECTLY gets a notification about the response even though the content is not visible. issue #609
        """
        
        # Create private assignment
        assignment_id = self.create_content(
            title   = 'private_response_assignment' ,
            content = 'private_response_assignment' ,
            type    = 'assignment' ,
            private = True ,
        )
        
        # Trust unitfriend
        self.follower_trust('unitfriend')
        
        # Unitfriend should be a trusted follower of unittest
        self.log_in_as('unitfriend')
        
        # Check to see if the assigment can be seen by unitfriend
        unittest_assignment_titles = [assignment['title'] for assignment in self.get_member('unittest')['assignments_active']['items']]
        self.assertIn('private_response_assignment', unittest_assignment_titles)
        
        # Post a respsponse
        response_id = self.create_content(
            title   = 'private_response_test' ,
            content = 'private_response_test' ,
            type    = 'assignment' ,
        )
        
        # Check response in list
        for username in ['unittest', 'unitfriend']:
            self.log_in_as(username)
            assignment_reponse_titles = [response['title'] for response in self.get_content(assignment_id)['responses']['items']]
            self.assertIn('private_response_test', assignment_reponse_titles)
        
        # Reset
        self.log_in_as('unittest')
        self.delete_content(assignment_id)
        self.follower_distrust('unitfriend')
        self.log_in_as('unitfriend')
        self.delete_content(response_id)