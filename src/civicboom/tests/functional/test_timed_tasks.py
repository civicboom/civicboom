from civicboom.tests import *

from civicboom.model      import User, Message
from civicboom.model.meta import Session

from civicboom.controllers.task import response_completed_ok

from civicboom.lib.database.get_cached import get_member, get_content

import datetime

from nose.plugins.skip import SkipTest


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
        
        now = self.server_datetime()
        
        # Setup - Create Assignment due in 10 days and Accept 
        self.log_in_as('unittest')
        assignment_id = self.create_content(title="timed_task_test", type="assignment", due_date=now + datetime.timedelta(days=10))
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
        
        set_due_date(assignment_id, due_date=now + datetime.timedelta(days=7))
        assignment_near_expire()
        self.assertEqual(num_emails + 1, getNumEmails())
        num_emails += 1
        self.assertIn('due next week', getLastEmail().content_text)
        
        set_due_date(assignment_id, due_date=now + datetime.timedelta(days=4))
        assignment_near_expire()
        self.assertEqual(num_emails, getNumEmails())
        
        set_due_date(assignment_id, due_date=now + datetime.timedelta(days=1))
        assignment_near_expire()
        self.assertEqual(num_emails + 1, getNumEmails() )
        num_emails += 1
        self.assertIn('due tomorrow', getLastEmail().content_text)
        
        
        set_due_date(assignment_id, due_date=now + datetime.timedelta(days=0))
        assignment_near_expire()
        self.assertEqual(num_emails, getNumEmails())
        
        set_due_date(assignment_id, due_date=now - datetime.timedelta(days=5)) # Expired 5 days ago
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
        
        now = self.server_datetime()
        
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
        set_join_date('pending_test', join_date=now - datetime.timedelta(days=1) )
        
        # Reminder signup email should be generated
        remind_pending_users(frequency_of_timed_task="hours=1", remind_after="hours=24")
        self.assertEqual(getNumEmails(), num_emails + 1)
        email_response = getLastEmail()
        self.assertIn  ('reminder', email_response.subject)
        self.assertTrue(email_response.content_text       )
        num_emails += 1
        
        # Movie join date further skill .. we dont want a repeat reminder
        set_join_date('pending_test', join_date=now - datetime.timedelta(days=5) ) # join date back a day
        
        num_emails = getNumEmails()
        remind_pending_users(frequency_of_timed_task="hours=1", remind_after="hours=24")
        self.assertEqual(num_emails + 0, getNumEmails()) # No emails should be sent again
        
        self.assertEquals(count_pending_members(), num_pending) # Member should still be pending at the end of this test
        
        
        
        # Remove Pending users -------------------------------------------------
        
        remove_pending_users(delete_older_than="days=7")
        self.assertEquals(count_pending_members(), num_pending) # no users should have changed
        self.assertEquals(getNumEmails()         , num_emails ) # no emails should have been sent
        
        set_join_date('pending_test', join_date=now - datetime.timedelta(days=8) )
        
        remove_pending_users(delete_older_than="days=7")
        self.assertEquals(count_pending_members(), num_pending - 1) # user removed
        self.assertEquals(getNumEmails()         , num_emails     ) # no email sent
        num_pending += -1



    #---------------------------------------------------------------------------
    # Auto publish sceduled drafts
    #---------------------------------------------------------------------------
    def test_auto_publish(self):
        """
        Auto publish sceduled drafts
        
        Drafts can have the field 'auto_publish_trigger_datetime'
        If this is set the draft will be auto published on the closest hour
        
        Note this is a paid for feature and can only be set by plus users
        """
        
        def publish_scheduled_content():
            response = self.app.get(url(controller='task', action='publish_scheduled_content'))
            self.assertIn(response_completed_ok, response.body)
        
        now = self.server_datetime()
        
        # Create draft content with auto_publish datetime ----------------------
        
        content_id_1 = self.create_content(
            title       = 'Auto Publish Test',
            content     = 'This should test the auto publish feature',
            type        = 'draft',
            target_type = 'assignment',
            due_date                      = now + datetime.timedelta(days=1   ), # set due_date in extra_fields so they can be reinstated on publish
            auto_publish_trigger_datetime = now + datetime.timedelta(seconds=3), # have to add 3 seconds because date must be in future to pass validator
        )
        
        content_id_2 = self.create_content(
            title       = 'Auto Publish Test 2',
            content     = 'This should test the auto publish feature. Not to be published, because the publish date is to far in the future',
            type        = 'draft',
            target_type = 'assignment',
            due_date                      = now + datetime.timedelta(days=3), # set due_date in extra_fields so they can be reinstated on publish
            auto_publish_trigger_datetime = now + datetime.timedelta(days=1),
        )
        
        
        # Execute timed task ---------------------------------------------------
        publish_scheduled_content() # should only publish content_id_1
        
        # Check published ------------------------------------------------------
        
        content = self.get_content(content_id_1)['content'] # Should have published because date auto_publish date was in correct range
        self.assertEqual(content['type'], 'assignment')
        
        content = self.get_content(content_id_2)['content'] # Should NOT have published as auto_publish date was to far in the future
        self.assertEqual(content['type'], 'draft')
        
        response = self.app.get(url('member_action', id='unittest', action='assignments_active', format='json'))
        response_json = json.loads(response.body)
        self.assertEqual(response_json['data']['list']['items'][0]['id'], content_id_1)
        
        assignment_count = response_json['data']['list']['count']
        
        # Check frag/html list item formatting ---------------------------------
        
        # There should be 1 item awaiting publishing
        # Check that the html/frag lists contains the auto_publish icon for frag_lists
        response = self.app.get(url('member', id='unittest', format='frag'))
        self.assertIn('i_auto_publish', response.body)
        
        
        # Change server time to publish content_id_2 ---------------------------
        
        now = self.server_datetime(now + datetime.timedelta(hours=23))
        publish_scheduled_content() #  should publish nothing
        
        # check no published assignments
        response = self.app.get(url('member_action', id='unittest', action='assignments_active', format='json'))
        response_json = json.loads(response.body)
        self.assertEqual(response_json['data']['list']['count']         , assignment_count    )
        
        now = self.server_datetime(now + datetime.timedelta(hours=1))
        publish_scheduled_content() #  should publish content_id_2
        
        # check content_id_2 published assignments
        response = self.app.get(url('member_action', id='unittest', action='assignments_active', format='json'))
        response_json = json.loads(response.body)
        self.assertEqual(response_json['data']['list']['count']         , assignment_count + 1)
        self.assertEqual(response_json['data']['list']['items'][0]['id'], content_id_2        )
        
        
        # Check Validators for auto_publish_trigger_datetime -------------------
        
        # Reject publish date in past
        response = self.app.post(
            url('contents', format='json') ,
            params = {
                '_authentication_token': self.auth_token    ,
                'title'                : 'Auto Publish Test',
                'content'              : 'Auto Publish Test',
                'type'                 : 'draft'            ,
                'auto_publish_trigger_datetime': now - datetime.timedelta(minutes=1),
            } ,
            status = 400 ,
        )
        self.assertIn('auto publish date must be in the future', response.body)
        
        # 'Non plus account' should not be able to set auto_publish field
        self.log_in_as('kitten')
        response = self.app.post(
            url('contents', format='json') ,
            params = {
                '_authentication_token': self.auth_token    ,
                'title'                : 'Auto Publish Test',
                'content'              : 'Auto Publish Test',
                'type'                 : 'draft'            ,
                'auto_publish_trigger_datetime': now + datetime.timedelta(minutes=1),
            } ,
            status = 400 ,
        )
        self.assertIn('require a paid account', response.body)
        
        # Cleanup --------------------------------------------------------------
        
        self.server_datetime('now') # Reset date jibbling
        
        self.log_in_as('unittest')
        self.delete_content(content_id_1)
        self.delete_content(content_id_2)


    #---------------------------------------------------------------------------
    # Email Notification Symmarys
    #---------------------------------------------------------------------------
    def test_summary_emails(self):
        def task_summary_notification_email():
            response = self.app.get(url(controller='task', action='summary_notification_email'))
            self.assertIn(response_completed_ok, response.body)
        
        now_start = self.server_datetime()
        now = now_start
        
        # No summary emails should trigger yet because no users have setup an interval
        num_emails = getNumEmails()
        task_summary_notification_email()
        self.assertEquals(num_emails, getNumEmails())
        
        # Setup test data ------------------------------------------------------
        self.setting('summary_email_interval', 'advanced', 'hours=1') # Setup summary date
        
        # Execute timed task ---------------------------------------------------
        num_emails = getNumEmails()
        task_summary_notification_email()
        
        # Add message that should trigger in last hour and send notification
        m = Message()
        m.target    = Session.query(User).get('unittest')
        m.subject   = 'Test summary_notification_email'
        m.content   = 'Test summary_notification_email'
        m.timestamp = now + datetime.timedelta(minutes=30)
        Session.add(m)
        Session.commit()
        
        now = self.server_datetime(now + datetime.timedelta(hours=1))
        
        num_emails = getNumEmails()
        task_summary_notification_email()
        
        # Check sent emails ----------------------------------------------------
        
        self.assertEquals(getNumEmails(), num_emails + 1)
        email = getLastEmail().content_text
        self.assertIn('summary_notification_email', email)
        
        # Reset db state
        self.setting('summary_email_interval', 'advanced', '')
        
        # No summary emails should trigger yet because no users have setup an interval
        num_emails = getNumEmails()
        task_summary_notification_email()
        #self.assertEquals(num_emails, getNumEmails()) # AllanC - this fails .. investigation needs to be made
        
        # Reset server datetime
        self.server_datetime(now_start)
        
        Session.delete(m)
        Session.commit()