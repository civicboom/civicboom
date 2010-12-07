from civicboom.tests import *

import json
import datetime



class TestAssignAcceptResponseCycleController(TestController):

    #---------------------------------------------------------------------------
    # Open Assignment Cycle
    #---------------------------------------------------------------------------
    def test_open_assignment(self):
        """
        Create
        Respond
        Approve/Dissasociate/Seen
        """
        
        # Create assignment ----------------------------------------------------
        
        response = self.app.post(
            url('contents', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'title'        : u'Unittest Open Assignment',
                'contents'     : u'This tests the Assign/Response cycle. This should be deleted at the end of the tests' ,
                'type'         : u'assignment' ,
                #'due_date'     : datetime.datetime.now() + datetime.timedelta(days=3) ,
                #'event_date'   : datetime.datetime.now() + datetime.timedelta(days=1) ,
                'submit_publish': u'publish' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        self.assignment_id = int(response_json['data']['id'])
        assert self.assignment_id > 0
        
        # Responses ------------------------------------------------------------
        
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
                'submit_publish': u'publish' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        self.assignment_response_id_1 = int(response_json['data']['id'])
        assert self.assignment_response_id_1 > 0
        
        # Response to be 'disasociate'
        response = self.app.post(
            url('contents', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'title'         : u'Response to disasociate',
                'contents'      : u'Test Response' ,
                'type'          : u'article' ,
                'parent_id'     : self.assignment_id ,
                'submit_publish': u'publish' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        self.assignment_response_id_2 = int(response_json['data']['id'])
        assert self.assignment_response_id_2 > 0
        
        # Response to be 'seen'
        response = self.app.post(
            url('contents', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'title'         : u'Response to seen',
                'contents'      : u'Test Response' ,
                'type'          : u'article' ,
                'parent_id'     : self.assignment_id ,
                'submit_publish': u'publish' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        self.assignment_response_id_3 = int(response_json['data']['id'])
        assert self.assignment_response_id_3 > 0
        
        # Check Response -------------------------------------------------------
        
        self.log_in_as('unittest')
        
        response = self.app.get(url('content', id=self.assignment_id, format='json'), status=200)
        response_json = json.loads(response.body)
        assert 'unitfriend'     in response
        assert 'to approve'     in response
        assert 'to disasociate' in response
        assert 'to seen'        in response
        assert len(response_json['data']['responses']) == 3
        
        # Approve and Dissassociate --------------------------------------------
        
        response = self.app.post(
            url('content_action', action='approve'    , id=self.assignment_response_id_1, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        
        response = self.app.post(
            url('content_action', action='disasociate', id=self.assignment_response_id_2, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        
        response = self.app.post(
            url('content_action', action='seen',        id=self.assignment_response_id_3, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        
        
        # Check Approved and Dissassociate -------------------------------------
        
        response = self.app.get(url('content', id=self.assignment_id, format='json'), status=200)
        response_json = json.loads(response.body)
        assert 'unitfriend'         in response
        assert 'to approve'         in response
        assert 'to disasociate' not in response
        assert 'to seen'            in response
        assert len(response_json['data']['responses']) == 2
        
        # Delete Assignment ----------------------------------------------------
        
        response = self.app.delete(
            url('content', id=self.assignment_id, format="json"),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        
        # Check Cascade of Delete was correct ----------------------------------
        
        response = self.app.get(url('content', id=self.assignment_response_id_1, format='json'), status=200)
        assert 'to approve' in response
        response = self.app.get(url('content', id=self.assignment_response_id_2, format='json'), status=200)
        assert 'to disasociate' in response
        response = self.app.get(url('content', id=self.assignment_response_id_3, format='json'), status=200)
        assert 'to seen' in response
        
        # Cleanup --------------------------------------------------------------
        
        self.log_in_as('unitfriend')
        
        # Owner should not be able to delete the content because it is locked
        response = self.app.delete(
            url('content', id=self.assignment_response_id_1, format="json"),
            params={'_authentication_token': self.auth_token,},
            status=403
        )
        
        response = self.app.delete(
            url('content', id=self.assignment_response_id_2, format="json"),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        
        response = self.app.delete(
            url('content', id=self.assignment_response_id_3, format="json"),
            params={'_authentication_token': self.auth_token,},
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
                'submit_publish': u'publish' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        self.assignment_id = int(response_json['data']['id'])
        assert self.assignment_id > 0
        
        # Accept and Withdraw Assignment ---------------------------------------
        
        # Try to accept own assignment (should fail)
        response = self.app.post(
            url('content_action', action='accept', id=self.assignment_id, format='json'),
            params={'_authentication_token': self.auth_token,},
            #status=400
            status=200
            # TODO: This should fail! needs to be added in future!
            #       Users should not be able to accept there own assignments
        )
        
        self.log_in_as('unitfriend')
        
        # record number of currently accepted assignments - to compare at end
        response      = self.app.get(url('member', id='unitfriend', format='json'), status=200)
        response_json = json.loads(response.body)
        num_accepted  = len(response_json['data']['assignments_accepted'])
        
        # Withdraw before accepting (should error)
        response = self.app.post(
            url('content_action', action='withdraw', id=self.assignment_id, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=400
        )
        
        # Accept
        response = self.app.post(
            url('content_action', action='accept', id=self.assignment_id, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        assert 'accepted' in response
        
        # withdraw
        response = self.app.post(
            url('content_action', action='withdraw', id=self.assignment_id, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        assert 'withdrawn' in response
        
        # Accept again (should reject)
        response = self.app.post(
            url('content_action', action='accept', id=self.assignment_id, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=400
        )
        
        # Num accepted ---------------------------------------------------------
        
        # compare number of accepted assignments to num at beggining of test
        # record number of currently accepted assignments - to compare at end
        response = self.app.get(url('member', id='unitfriend', format='json'), status=200)
        response_json = json.loads(response.body)
        assert num_accepted == len(response_json['data']['assignments_accepted'])
        
        # Cleanup --------------------------------------------------------------
        
        self.log_in_as('unittest')
        
        response = self.app.delete(
            url('content', id=self.assignment_id, format="json"),
            params={'_authentication_token': self.auth_token,},
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
    def test_accept_withdraw(self):
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
                'title'        : u'Assignment to test accept delete cascade',
                'contents'     : u'content' ,
                'type'         : u'assignment' ,
                'submit_publish': u'publish' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        self.assignment_id = int(response_json['data']['id'])
        assert self.assignment_id > 0
        
        self.log_in_as('unitfriend')
        
        # Accept ---------------------------------------------------------------
        response = self.app.post(
            url('content_action', action='accept', id=self.assignment_id, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        assert 'accepted' in response

        # Delete assignemnt ----------------------------------------------------
        
        self.log_in_as('unittest')
        
        response = self.app.delete(
            url('content', id=self.assignment_id, format="json"),
            params={'_authentication_token': self.auth_token,},
            status=200
        )

        # Check delete cascade  ------------------------------------------------

        self.log_in_as('unitfriend')

        response = self.app.get(url('member', id='unitfriend', format='json'), status=200)
        response_json = json.loads(response.body)

        #TODO
        # Check delete cascade
        # Check assignment canceled notification was sent