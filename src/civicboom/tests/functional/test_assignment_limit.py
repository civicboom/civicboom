from civicboom.tests import *
from pylons import config

#import json

#import logging
#log      = logging.getLogger(__name__)


class TestAssignmentLimitController(TestController):

    #---------------------------------------------------------------------------
    # Assignment Limit
    #---------------------------------------------------------------------------
    def test_publish_assignment_limit(self):
        """
        Create new user
        Create 5 assignments
        Forwarded to correct page when activated 6th
        """
        
        # Create Fresh User ----------------------------------------------------
        self.sign_up_as('assign_limit')
        
        # Set the number of assignments a normal user is limited too
        created_assignments = []
        for i in range(config['payment.free.assignment_limit']-1):
            created_assignments.append(self.create_assignment('Assignment Limit %d' % i))
            
        # Try to set one over the limit
        response = self.create_assignment('Dont allow this assignment', status=402)
        
        # Upgrade account
        self.set_account_type('plus')
        
        # Set a new assignment
        response = self.create_assignment('Assignment Limit > Paid')
        
        # Double check that all the assimgments appear in this users content list
        response = self.app.get(url('member_action', id='assign_limit', action='content', list='assignments',format='json'))
        response_json = json.loads(response.body)
        title_check = [] + [str(i) for i in range(config['payment.free.assignment_limit']-1)] + ['Paid']
        for assignment in response_json['data']['list']['items']:
            for title in title_check:
                if title in assignment['title']:
                    title_check.remove(title)
        self.assertEqual(len(title_check), 0)



    #---------------------------------------------------------------------------
    # Supporting Methods - Create/Delete Assignments
    #---------------------------------------------------------------------------
    
    def create_assignment(self, title, status=201):
        response = self.app.post(
            url('contents', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'title'        : title,
                'contents'     : u'Testing assignment limit' ,
                'type'         : u'assignment' ,
                #'submit_publish': u'publish' ,
            },
            status=status
        )
        if status==201:
            response_json = json.loads(response.body)
            id = int(response_json['data']['id'])
            self.assertNotEqual(id, 0)
            ##print('created assignment %d' % id)
            return id
        return response
