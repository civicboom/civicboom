from civicboom.tests import *

#import json
import datetime

import logging
log = logging.getLogger(__name__)


class TestAssignAcceptResponseCycleController(TestController):


    #---------------------------------------------------------------------------
    # Open Assignment Cycle
    #---------------------------------------------------------------------------
    def test_open_assignment(self):
        """
        Create
        Respond
        Approve/Disassociate/Seen
        """
        
        # Create assignment ----------------------------------------------------
        #   unittest creates
        
        response = self.app.post(
            url('contents', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'title'        : u'Unittest Open Assignment',
                'contents'     : u'This tests the Assign/Response cycle. This should be deleted at the end of the tests' ,
                'type'         : u'assignment' ,
                #'due_date'     : datetime.datetime.now() + datetime.timedelta(days=3) ,
                #'event_date'   : datetime.datetime.now() + datetime.timedelta(days=1) ,
                #'submit_publish': u'publish' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        self.assignment_id = int(response_json['data']['id'])
        self.assertNotEqual(self.assignment_id, 0)
        
        # Responses ------------------------------------------------------------
        #  unitfirend to respond 3 times
        
        self.log_in_as('unitfriend')
        
        # Response to be 'approve'
        response = self.app.post(
            url('contents', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'title'         : u'Response to approve',
                'contents'      : u'Test Response' ,
                'type'          : u'article' ,
                'parent_id'     : self.assignment_id ,
                #'submit_publish': u'publish' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        self.assignment_response_id_1 = int(response_json['data']['id'])
        self.assertNotEqual(self.assignment_response_id_1, 0)
        
        # Response to be 'disassociate'
        response = self.app.post(
            url('contents', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'title'         : u'Response to disassociate',
                'contents'      : u'Test Response' ,
                'type'          : u'article' ,
                'parent_id'     : self.assignment_id ,
                #'submit_publish': u'publish' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        self.assignment_response_id_2 = int(response_json['data']['id'])
        self.assertNotEqual(self.assignment_response_id_2, 0)
        
        # Response to be 'seen'
        response = self.app.post(
            url('contents', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'title'         : u'Response to seen',
                'contents'      : u'Test Response' ,
                'type'          : u'article' ,
                'parent_id'     : self.assignment_id ,
                #'submit_publish': u'publish' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        self.assignment_response_id_3 = int(response_json['data']['id'])
        self.assertNotEqual(self.assignment_response_id_3, 0)
        
        # Check Responses are present ------------------------------------------
        
        self.log_in_as('unittest')
        
        response = self.app.get(url('content', id=self.assignment_id, format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertIn('unitfriend'     , response)
        self.assertIn('to approve'     , response)
        self.assertIn('to disassociate', response)
        self.assertIn('to seen'        , response)
        self.assertEqual(len(response_json['data']['responses']['items']), 3)
        
        # Check other users dont have approve/seen/dissacociate actions --------
        
        for user in ['unitfriend', 'kitten']:
            self.log_in_as(user)
            for id in [self.assignment_response_id_1, self.assignment_response_id_2, self.assignment_response_id_3]:
                actions = self.get_actions(id)
                for action in ['approve', 'seen', 'dissasociate']:
                    self.assertNotIn(action, actions)
        
        self.log_in_as('unittest')
        
        # Approve --------------------------------------------------------------
        
        #self.set_account_type('plus') # Double enforce that unittest is a plus user
        
        num_emails = getNumEmails()
        
        self.assertIn('approve', self.get_actions(self.assignment_response_id_1))
        response = self.app.post(
            url('content_action', action='approve'    , id=self.assignment_response_id_1, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        self.assertNotIn('approve', self.get_actions(self.assignment_response_id_1))

        # Check that the emails have been generated and sent to the correct users once approved
        self.assertEqual(getNumEmails(), num_emails + 2)
        emails_to = [email.email_to for email in emails[-2:]]
        self.assertIn('test+unittest@civicboom.com'  , emails_to)
        self.assertIn('test+unitfriend@civicboom.com', emails_to)
        self.assertSubStringIn(['requested for potential','creator has been notified'],[email.content_text for email in emails[-2:]]) # Check the contents of the emails is one accepted, one accepted parent
        
        # Disassociate ---------------------------------------------------------
        
        self.assertIn('dissasociate', self.get_actions(self.assignment_response_id_2))
        response = self.app.post(
            url('content_action', action='disassociate', id=self.assignment_response_id_2, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        self.assertNotIn('dissasociate', self.get_actions(self.assignment_response_id_2))
        
        # Test 2nd time fail - GregM: Should this fail?
#        response = self.app.post(
#            url('content_action', action='disassociate', id=self.assignment_response_id_2, format='json'),
#            params={'_authentication_token': self.auth_token,},
#            status=403
#        )
        
        # Seen -----------------------------------------------------------------
        
        self.assertIn('seen', self.get_actions(self.assignment_response_id_3))
        response = self.app.post(
            url('content_action', action='seen',        id=self.assignment_response_id_3, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        self.assertNotIn('seen', self.get_actions(self.assignment_response_id_3))
        
        # Check Approved and Dissassociate -------------------------------------
        
        response = self.app.get(url('content', id=self.assignment_id, format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertIn('unitfriend'         , response)
        self.assertIn('to approve'         , response)
        self.assertNotIn('to disassociate' , response)
        self.assertIn('to seen'            , response)
        self.assertEqual(len(response_json['data']['responses']['items']), 2)
        
        # Delete Assignment ----------------------------------------------------
        
        self.delete_content(self.assignment_id)
        
        # Check Cascade of Delete was correct ----------------------------------
        
        response = self.app.get(url('content', id=self.assignment_response_id_1, format='json'), status=200)
        self.assertIn('to approve', response)
        response = self.app.get(url('content', id=self.assignment_response_id_2, format='json'), status=200)
        self.assertIn('to disassociate', response)
        response = self.app.get(url('content', id=self.assignment_response_id_3, format='json'), status=200)
        self.assertIn('to seen', response)
        
        # Cleanup --------------------------------------------------------------
        
        self.log_in_as('unitfriend')
        
        # Owner should not be able to delete the content because it is locked
        #self.assertNotIn('delete', self.get_actions(self.assignment_response_id_1)) # AllanC - This SHOULD not be in the actions list :(
        response = self.app.post(
            url('content', id=self.assignment_response_id_1, format="json"),
            params={'_method': 'delete', '_authentication_token': self.auth_token,},
            status=403
        )
        
        self.delete_content(self.assignment_response_id_2)
        #self.assertIn('delete', self.get_actions(self.assignment_response_id_2))
        #response = self.app.post(
        #    url('content', id=self.assignment_response_id_2, format="json"),
        #    params={'_method': 'delete', '_authentication_token': self.auth_token,},
        #    status=200
        #)
        
        response = self.app.post(
            url('content', id=self.assignment_response_id_3, format="json"),
            params={'_method': 'delete', '_authentication_token': self.auth_token,},
            status=403
        )
        
        #TODO: To complete cleanup we need to delete 'assignment_response_id_1' and '3' ... but how?
        #      if no parent_id and locked by 'parent owner' then allow delete?


    #---------------------------------------------------------------------------
    # Accept / Withdraw Cycle
    #---------------------------------------------------------------------------
    def test_accept_withdraw(self):
        """
        Accept then withdraw
        """
        
        # Create assignment ----------------------------------------------------
        
        response = self.app.post(
            url('contents', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'title'        : u'Assignment to test Accept/Withdraw',
                'contents'     : u'content' ,
                'type'         : u'assignment' ,
                #'submit_publish': u'publish' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        self.assignment_id = int(response_json['data']['id'])
        self.assertGreater(self.assignment_id, 0)
        
        # Check content is published and check num_accepted trigger
        response      = self.app.get(url('content', id=self.assignment_id, format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEquals(response_json['data']['content']['num_accepted'], 0)

        
        # Accept and Withdraw Assignment ---------------------------------------
        
        # Try to accept own assignment (should fail)
        response = self.app.post(
            url('content_action', action='accept', id=self.assignment_id, format='json'),
            params={'_authentication_token': self.auth_token,},
            #status=400
            status=200
            # TODO: Should this fail? needs to be added in future?
            #       Should Users should not be able to accept there own assignments?
        )

        # check accepted num
        response      = self.app.get(url('content', id=self.assignment_id, format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEquals(response_json['data']['content']['num_accepted'], 1)

        
        self.log_in_as('unitfriend')
        
        # record number of currently accepted assignments - to compare at end
        response      = self.app.get(url('member', id='unitfriend', format='json'), status=200)
        response_json = json.loads(response.body)
        num_accepted  = len(response_json['data']['assignments_accepted']['items'])
        
        # Withdraw before accepting (should error)
        self.assertNotIn('withdraw', self.get_actions(self.assignment_id)) # Withdraw should not be an action as there isnt an accept record generated yet
        response = self.app.post(
            url('content_action', action='withdraw', id=self.assignment_id, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=400
        )
        
        # Accept
        self.accept_assignment(self.assignment_id)
        
        # check accepted num - only appear in postgress trigger if record exisits
        response      = self.app.get(url('content', id=self.assignment_id, format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEquals(response_json['data']['content']['num_accepted'], 2)
        self.assertIn('unitfriend', [accepted['username'] for accepted in response_json['data']['accepted_status']['items'] if accepted['status']=='accepted'])
        
        # withdraw
        self.withdraw_assignment(self.assignment_id)
        
        # Accept again (should reject)
        self.assertNotIn('accept', self.get_actions(self.assignment_id)) # Withdraw should not be an action as there isnt an accept record generated yet
        response = self.app.post(
            url('content_action', action='accept', id=self.assignment_id, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=400
        )
        
        # Content num accepted ------------------------------------------------

        response      = self.app.get(url('content', id=self.assignment_id, format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEquals(response_json['data']['content']['num_accepted'], 1)
        self.assertIn('unitfriend', [accepted['username'] for accepted in response_json['data']['accepted_status']['items'] if accepted['status']=='withdrawn'])
        
        # Member Num accepted ---------------------------------------------------------
        
        # compare number of accepted assignments to num at beggining of test
        # record number of currently accepted assignments - to compare at end
        response = self.app.get(url('member', id='unitfriend', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEqual(num_accepted, len(response_json['data']['assignments_accepted']['items']))
        
        # Cleanup --------------------------------------------------------------
        
        self.log_in_as('unittest')
        
        response = self.app.post(
            url('content', id=self.assignment_id, format="json"),
            params={'_method': 'delete', '_authentication_token': self.auth_token,},
            status=200
        )
        

    #---------------------------------------------------------------------------
    # Closed Assignment Cycle
    #---------------------------------------------------------------------------
    def test_closed_assignment(self):
        """
        Closed
        Invite
        Response
        Approve/Dissassociate
        """
        pass

    def subtest_create_closed_assignment(self):
        pass
    
    def subtest_invite_members(self):
        pass
    
    
    #---------------------------------------------------------------------------
    # Accepted Assignment Delete Cascade
    #---------------------------------------------------------------------------
    def test_accept_delete(self):
        """
        Create assignment
        Accept assignment
        Delete assignment
        (accepted record should have cascaded delete)
        """
        
        # Create assignment ----------------------------------------------------
        
        response = self.app.post(
            url('contents', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'title'        : u'Assignment to test accept delete (not allowed to say it) c4sc4dE',
                'contents'     : u'content' ,
                'type'         : u'assignment' ,
                #'submit_publish': u'publish' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        assignment_id = int(response_json['data']['id'])
        self.assertGreater(assignment_id, 0)
                
        self.log_in_as('unitfriend')

        # AllanC - I double check the assignment num here because the prostgress trigger was incorrect and returning ALL accepted number for all assignments at one point, so haveing another accept check here was sensibel

        # check accepted num
        response      = self.app.get(url('content', id=assignment_id, format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEquals(response_json['data']['content']['num_accepted'], 0)
        
        # Accept ---------------------------------------------------------------
        self.accept_assignment(assignment_id)

        # check accepted num
        response      = self.app.get(url('content', id=assignment_id, format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEquals(response_json['data']['content']['num_accepted'], 1)
        
        


        # Delete assignemnt ----------------------------------------------------
        
        self.log_in_as('unittest')
        
        # AllanC - this is tested in test_delete_cascade?
        
        #self.delete_content(assignment_id)

        # Check delete cascade  ------------------------------------------------

        #self.log_in_as('unitfriend')

        #response = self.app.get(url('member', id='unitfriend', format='json'), status=200)
        #response_json = json.loads(response.body)

        #TODO
        # Check delete cascade - AllanC: see test_delete_cascades.py
        # Check assignment canceled notification was sent


    #---------------------------------------------------------------------------
    # Dissassociate comments
    #---------------------------------------------------------------------------
    def test_dissasocaite_comments(self):
        self.log_in_as('unittest')
        assignment_id = self.create_content(title='moderator test', content='reply with an offensive comments and I will dissassociate it', type='assignment', responses_require_moderation=True)
        
        self.log_in_as('unitfriend')
        self.assertNotIn('moderator', self.get_actions(assignment_id))
        comment_id_1 = self.comment(assignment_id, 'My god this assignment is barbaric!!! what lies! what slader!')
        
        self.log_in_as('kitten')
        comment_id_2 = self.comment(assignment_id, 'I agree! youre horrible Mr Unittest! I HATE YOU!')
        
        self.log_in_as('unittest')
        comment_id_3 = self.comment(assignment_id, 'We will soon see about that mi-lado! Lets the dissassociation commence!')
        
        assignment = self.get_content(assignment_id)
        self.assertIn('moderator', assignment['actions'])
        comment_ids = [comment['id'] for comment in assignment['comments']['items']]
        self.assertIn(comment_id_1, comment_ids)
        self.assertIn(comment_id_2, comment_ids)
        self.assertIn(comment_id_3, comment_ids)
        
        response = self.app.post(
            url('content_action', action='disassociate', id=comment_id_1, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        assignment = self.get_content(assignment_id)
        comment_ids = [comment['id'] for comment in assignment['comments']['items']]
        self.assertNotIn(comment_id_1, comment_ids)
        self.assertIn   (comment_id_2, comment_ids)
        self.assertIn   (comment_id_3, comment_ids)
        notification = self.getLastNotification('unitfriend')
        self.assertIn   (url('content', id=assignment_id), notification['content'])
        self.assertIn   ('disassociated', notification['subject'])
        
        self.log_in_as('kitten')
        comment_id_4 = self.comment(assignment_id, 'NOOO!!! How dare you! you bastard! He had a valid point! Will anyone help us in our hour of need!')
        
        self.log_in_as('unittest')
        response = self.app.post(
            url('content_action', action='disassociate', id=comment_id_2), # deliberatly dont use a format - test the html_fallback_url
            params={'_authentication_token': self.auth_token,},
            status=302
        )
        assignment = self.get_content(assignment_id)
        comment_ids = [comment['id'] for comment in assignment['comments']['items']]
        self.assertNotIn(comment_id_1, comment_ids)
        self.assertNotIn(comment_id_2, comment_ids)
        self.assertIn   (comment_id_3, comment_ids)
        self.assertIn   (comment_id_4, comment_ids)
        
        self.log_in_as('unittest')
        self.delete_content(assignment_id)
        
        self.delete_content(comment_id_1, force=True)
        self.delete_content(comment_id_2, force=True)
        #self.delete_content(comment_id_3, force=True) # These have already been deleted by the delete casades
        #self.delete_content(comment_id_4, force=True)