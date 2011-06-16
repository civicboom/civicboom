from civicboom.tests import *

from civicboom.model      import User
from civicboom.model.meta import Session

from civicboom.controllers.task import response_completed_ok

from civicboom.lib.database.get_cached import get_member, get_content

import datetime


class TestTimedTasksController(TestController):

    #---------------------------------------------------------------------------
    # Assignment Expire and alert notifications
    #---------------------------------------------------------------------------
    def test_assignment_expire(self):
        """
        Create assignment
        Fake date and time
        trigger timed tasks
        check correct notifications are generated
        """
        
        def set_due_date(assignment_id, due_date=None, timedelta=None):
            assignment = get_content(assignment_id)
            if not due_date:
                due_date = assignment.due_date - timedelta
            assignment.due_date = due_date
            Session.commit()
        
        def assignment_near_expire():
            response = self.app.get(url(controller='task', action='assignment_near_expire'))
            self.assertIn(response_completed_ok, response)
        
        # Setup - Create Assignment due in 10 days and Accept 
        self.log_in_as('unittest')
        assignment_id = self.create_content(title="timed_task_test", type="assignment", due_date=datetime.datetime.now() + datetime.timedelta(days=10))
        self.log_in_as('unitfriend')
        self.accept_assignment(assignment_id)
        self.log_out
        
        # NOTE: Assumption is made that email notifications for unittest are enabled for the assignment due notifications
        #       TODO - can these be set in the tests so we can guarentee the state
        
        
        num_emails = getNumEmails()
        
        # No emails should be sent as the assignment is due in 10 days
        assignment_near_expire()
        self.assertEqual(num_emails, getNumEmails())
        
        #from civicboom.lib.communication.email_log import getEmailSubjects
        #for s in getEmailSubjects():
        #    print s
        
        set_due_date(assignment_id, due_date=datetime.datetime.now() + datetime.timedelta(days=7))
        assignment_near_expire()
        self.assertEqual(num_emails + 1, getNumEmails())
        num_emails += 1
        self.assertIn('due next week', getLastEmail().content_text)
        
        set_due_date(assignment_id, due_date=datetime.datetime.now() + datetime.timedelta(days=4))
        assignment_near_expire()
        self.assertEqual(num_emails, getNumEmails())
        
        set_due_date(assignment_id, due_date=datetime.datetime.now() + datetime.timedelta(days=1))
        assignment_near_expire()
        self.assertEqual(num_emails + 1, getNumEmails() )
        num_emails += 1
        self.assertIn('due tomorrow', getLastEmail().content_text)
        
        
        set_due_date(assignment_id, due_date=datetime.datetime.now() + datetime.timedelta(days=0))
        assignment_near_expire()
        self.assertEqual(num_emails, getNumEmails())
        
        set_due_date(assignment_id, due_date=datetime.datetime.now() - datetime.timedelta(days=5)) # Expired 5 days ago
        assignment_near_expire()
        self.assertEqual(num_emails, getNumEmails())
        
        self.log_in_as('unittest')
        self.delete_content(assignment_id)

    
    #---------------------------------------------------------------------------
    # Remind and remove pending users
    #---------------------------------------------------------------------------
    def test_remind_and_remove_pending(self):
        """
        """
        
        def count_pending_members():
            return Session.query(User).filter(User.status=='pending').count()
        
        def set_join_date(username, join_date=None, timedelta=None):
            remind_pending_member = get_member(username)
            if not join_date:
                join_date = remind_pending_member.join_date - timedelta
            remind_pending_member.join_date = join_date
            Session.commit()
        
        def remind_pending_users(**kwargs):
            response = self.app.get(url(controller='task', action='remind_pending_users', **kwargs))
            self.assertIn(response_completed_ok, response)
        
        def remove_pending_users(**kwargs):
            response = self.app.get(url(controller='task', action='remove_pending_users', **kwargs))
            self.assertIn(response_completed_ok, response)
        
        num_pending = count_pending_members()
        
        # Create new pending user
        response = self.app.post(
            url(controller='register', action='email', format="json"),
            params={
                'username': u'pending_test',
                'email'   : u'test+pending@civicboom.com',
            },
        )
        self.assertEquals(count_pending_members(), num_pending + 1)
        num_pending += 1
        
        
        
        # Remind Pending users -------------------------------------------------
        
        # Run the task NOW - there should be no email generated because the user has not been pending long enough
        num_emails = getNumEmails()
        remind_pending_users()
        self.assertEqual(num_emails, getNumEmails())
        
        # Move join date to 1 day ago
        set_join_date('pending_test', join_date=datetime.datetime.now() - datetime.timedelta(days=1) )
        
        # Reminder signup email should be generated
        remind_pending_users(frequency_of_timed_task="hours=1", remind_after="hours=24")
        self.assertEqual(getNumEmails(), num_emails + 1)
        email_response = getLastEmail()
        self.assertIn  ('reminder', email_response.subject)
        self.assertTrue(email_response.content_text       )
        num_emails += 1
        
        # Movie join date further skill .. we dont want a repeat reminder
        set_join_date('pending_test', join_date=datetime.datetime.now() - datetime.timedelta(days=5) ) # join date back a day
        
        num_emails = getNumEmails()
        remind_pending_users(frequency_of_timed_task="hours=1", remind_after="hours=24")
        self.assertEqual(num_emails + 0, getNumEmails()) # No emails should be sent again
        
        self.assertEquals(count_pending_members(), num_pending) # Member should still be pending at the end of this test
        
        
        
        # Remove Pending users -------------------------------------------------
        
        remove_pending_users(delete_older_than="days=7")
        self.assertEquals(count_pending_members(), num_pending) # no users should have changed
        self.assertEquals(getNumEmails()         , num_emails ) # no emails should have been sent
        
        set_join_date('pending_test', join_date=datetime.datetime.now() - datetime.timedelta(days=8) )
        
        remove_pending_users(delete_older_than="days=7")
        self.assertEquals(count_pending_members(), num_pending - 1) # user removed
        self.assertEquals(getNumEmails()         , num_emails     ) # no email sent
        num_pending += -1
