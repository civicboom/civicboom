from civicboom.tests import *

import datetime

from pylons import config

import logging
log = logging.getLogger(__name__)


def dob_for_age(age):
    return datetime.datetime.now() - datetime.timedelta(days=365 * age)


class TestAge(TestController):
    def test_age_limit(self):
        assignment_id = self.create_content(title="Assignment for age test", type='assignment')
        
        # Sign up a baby user that is just within the age range
        dob     = dob_for_age(config['setting.age.min_signup']) - datetime.timedelta(days=7) # AllanC - didnt want leap years and stuff to break tests, added 7 days as a buffer
        dob_str = "%s/%s/%s" % (dob.day, dob.month, dob.year)
        self.sign_up_as('test_age_baby', dob=dob_str)
        
        # Baby user trys to accept assignment - should fail because iz a baby
        response = self.app.post( # Accept assignment
            url('content_action', action='accept', id=assignment_id, format='json') ,
            params = {'_authentication_token': self.auth_token,} ,
            status = 403
        )
        self.assertIn('age', response)
        
        # Sign up a big hariy user who can accept accept requests
        dob     = dob_for_age(config['setting.age.accept']) - datetime.timedelta(days=7)
        dob_str = "%s/%s/%s" % (dob.day, dob.month, dob.year)
        
        self.sign_up_as('test_age_adult', dob=dob_str)
        self.accept_assignment(assignment_id)
        
        self.log_in_as('unittest')
        self.delete_content(assignment_id)
