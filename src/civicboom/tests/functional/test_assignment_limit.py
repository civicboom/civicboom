from civicboom.tests import *
from pylons import config

import json

#import logging
#log      = logging.getLogger(__name__)


class TestAssignmentLimitController(TestController):

    #---------------------------------------------------------------------------
    # Assignment Limit
    #---------------------------------------------------------------------------
    def test_open_assignment(self):
        """
        Create new user
        Create 5 assignments
        Forwarded to correct page when activated 6th
        """
        
        # Create Fresh User ----------------------------------------------------
        self.sign_up_as('assign_limit')
        
        created_assignments = []
        for i in range(config['payment.free.assignment_limit']):
            created_assignments.append(self.create_assignment('Assignment Limit %d' % i))
        response = self.create_assignment('Dont allow this assignment', status=403)



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
                'submit_publish': u'publish' ,
            },
            status=status
        )
        if status==201:
            response_json = json.loads(response.body)
            id = int(response_json['data']['id'])
            assert id > 0
            print('created assignment %d' % id)
            return id
        return response

    def delete_assignment(self, id):
        response = self.app.delete(
            url('content', id=id, format="json"),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
