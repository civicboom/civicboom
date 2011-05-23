from civicboom.tests import *


from civicboom.controllers.task import response_completed_ok

from civicboom.lib.database.get_cached import get_member


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
        pass

    
    #---------------------------------------------------------------------------
    # Remind and remove pending users
    #---------------------------------------------------------------------------
    def test_remind_and_remove_pending(self):
        """
        """
        
        def count_pending_members():
            return Session.query(User).filter(status=='pending').count()
        
        def set_join_date(username, join_date=None, timedelta=None):
            remind_pending_member = get_member(username)
            if not join_date:
                join_date = remind_pending_member.join_date - timedelta
            remind_pending_member.join_date = join_date
            Session.commit()
        
        def remind_pending_users():
            response = self.app.get(url(controller='task', action='remind_pending_users', frequency_of_timed_task="hours=3"))
            self.assertIn(response_completed_ok, response)
        
        def remove_pending_users():
            response = self.app.get(url(controller='task', action='remind_pending_users', delete_older_than      ="days=7" ))
            self.assertIn(response_completed_ok, response)
        
        num_pending = count_pending_members()
        
        # Create new pending user
        response = self.app.post(
            url(controller='register', action='email', format="json"),
            params={
                'username': u'pending_test',
                'email'   : u'pending@moose.com',
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
        remind_pending_users()
        self.assertEqual(num_emails + 1, getNumEmails())
        email_response = getLastEmail()
        self.assertIn  (email_response.subject, 'reminder')
        self.assertTrue(email_response.content_text       )
        num_emails += 1
        
        # Movie join date further skill .. we dont want a repeat reminder
        set_join_date('pending_test', join_date=datetime.datetime.now() - datetime.timedelta(days=5) ) # join date back a day
        
        num_emails = getNumEmails()
        remind_pending_users()
        self.assertEqual(num_emails + 0, getNumEmails()) # No emails should be sent again
        
        self.assertEquals(count_pending_members(), num_pending) # Member should still be pending at the end of this test
        
        
        
        # Remove Pending users -------------------------------------------------
        
        remove_pending_users() # set to 7 days
        self.assertEquals(count_pending_members(), num_pending) # no users should have changed
        self.assertEquals(getNumEmails()         , num_emails ) # no emails should have been sent
        
        set_join_date('pending_test', join_date=datetime.datetime.now() - datetime.timedelta(days=8) )
        
        remove_pending_users() # set to 7 days
        self.assertEquals(count_pending_members(), num_pending - 1) # user removed
        self.assertEquals(getNumEmails()         , num_emails     ) # no email sent
        num_pending += -1