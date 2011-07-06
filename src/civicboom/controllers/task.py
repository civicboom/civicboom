"""
Task Controller
Maintinence tasks that can be tiggered via cron jobs

All tasks are locked down to be executed by localhost only
See the companion script "tasks.py" in the project root for details on how to
setup a cron job to run these tasks
"""

from civicboom.lib.base import *

from cbutils.misc import timedelta_str

from sqlalchemy import and_

import datetime

log = logging.getLogger(__name__)

response_completed_ok = "task:ok" #If this is changed please update tasks.py to reflect the same "task ok" string


def normalize_datetime(datetime):
    return datetime.replace(minute=0, second=0, microsecond=0)
    

class TaskController(BaseController):
    
    #---------------------------------------------------------------------------
    # Security: Restict Calls to Localhost
    #---------------------------------------------------------------------------
    
    def __before__(self, action, **params):
        ##  Only accept requests from 127.0.0.1 as we never want these being
        ##  run by anyone other than the server at set times the server cron
        ##  system should have a script that makes URL requests at localhost
        ##  to activate these actions
        ##  Shish - no REMOTE_ADDR = "paster request foo.ini /task/blah" from
        ##  the command line
        if not (
                'REMOTE_ADDR' not in request.environ or
                request.environ['REMOTE_ADDR'] == "127.0.0.1" or
                request.environ['REMOTE_ADDR'] == request.environ.get('SERVER_ADDR', '0.0.0.0')
            ):
            return abort(403)
        # AllanC - these can be activated without a logged in user
        # Shish  - then they get logged as "anonymous"; it's still good to
        #          have the logging go to the central place
        # AllanC - automated tests seems to be failing as c.logged_in_user is not set. should lib/database/userlog.py be modifyed to cope with this? advice on loggin needed. This is strange because c.logged_in_user is ALWAYS inited even if it is None see base.py line 373 _get_member() always returns None
        
        # AllanC - BEHOLD!!! THE HOLY HACK!!! This was a short term fix so that timed tasks had links to live server rather than generating URL's with 'localhost' - issue #614
        #          Shish can you fix this properly. www.civicboom.com should not be hard coded here, it should be in python code, should be in a cfg file somewhere
        request.environ['HTTP_HOST'] = 'www.civicboom.com'
            
        user_log.info("Performing task '%s'" % (action, ))
        BaseController.__before__(self)


    #---------------------------------------------------------------------------
    # Remind Pending users after 1 day
    #---------------------------------------------------------------------------
    @web_params_to_kwargs
    def remind_pending_users(self, remind_after="hours=24", frequency_of_timed_task="hours=1"):
        """
        Users who try to sign up but don't complete the registration within one day get a reminder email
        to be run once every 24 hours
        """
        from civicboom.model.member import User
        from civicboom.lib.accounts import validation_url
        
        frequency_of_timed_task = timedelta_str(frequency_of_timed_task)
        remind_after            = timedelta_str(remind_after           )
        
        reminder_start = normalize_datetime(now()          - remind_after           )
        reminder_end   = normalize_datetime(reminder_start + frequency_of_timed_task)
        
        users_to_remind = Session.query(User).filter(User.status=='pending').filter(and_(User.join_date <= reminder_end, User.join_date >= reminder_start)).all() #.filter(~User.login_details.any()).
        for user in users_to_remind:
            log.info('Reminding pending user %s - %s' % (user.username, user.email_normalized))
            register_url = validation_url(user, controller='register', action='new_user')
            user.send_email(subject=_('_site_name: reminder'), content_html=render('/email/user_pending_reminder.mako', extra_vars={'register_url':register_url}))
        return response_completed_ok


    
    #---------------------------------------------------------------------------
    # Prune Pending users if not completed registration in 7 days
    #---------------------------------------------------------------------------
    @web_params_to_kwargs
    def remove_pending_users(self, delete_older_than="days=7"):
        """
        Users who do not complete the signup process by entering an email
        address that is incorrect or a bots or cant use email should be
        removed if they have still not signed up after 7 Days
        """
        from civicboom.model.member import User
        
        ghost_expire = normalize_datetime(now() - timedelta_str(delete_older_than))
        
        for user in Session.query(User).filter(User.status=='pending').filter(User.join_date <= ghost_expire).all(): # .filter(~User.login_details.any()).
            Session.delete(user)
            log.info('Deleting pending user %s - %s' % (user.username, user.email_normalized))
            # It may be nice to log numbers here to aid future business desctions
        Session.commit()
        # AllanC - the method above could be inefficent. could just do it at the DB side?
        return response_completed_ok



    #---------------------------------------------------------------------------
    # Assignment Reminder Notifications
    #---------------------------------------------------------------------------
    @web_params_to_kwargs
    def assignment_near_expire(self, frequency_of_timed_task="days=1"):
        """
        Users who have accepted assigments but have not posted response
        question should be reminded via a notification that the assingment
        has not long left
        """
        from civicboom.model.content     import AssignmentContent
        from civicboom.lib.communication import messages
        
        def get_assignments_by_date(date_start, date_end):
            return Session.query(AssignmentContent).filter(and_(AssignmentContent.due_date >= date_start, AssignmentContent.due_date <= date_end)).all()
        
        def get_responded(assignment):
            return [response.creator_id for response in assignment.responses]
        
        frequency_of_timed_task = timedelta_str(frequency_of_timed_task)
        
        date_7days_time = normalize_datetime(now() + datetime.timedelta(days=7))
        date_1days_time = normalize_datetime(now() + datetime.timedelta(days=1))
        
        for assignment in get_assignments_by_date(date_start=date_7days_time, date_end=date_7days_time + frequency_of_timed_task): # Get all assignments due in 7 days
            responded_member_ids = get_responded(assignment)                                                              #   Get a list of all the members that have responded to this assignment
            for member in [member for member in assignment.accepted_by if member.id not in responded_member_ids]:         #   For all members accepted this assignment #     Check if they have responded with an article
                member.send_notification( messages.assignment_due_7days(you=member, assignment=assignment) )              #     if not send a reminder notification
        
        for assignment in get_assignments_by_date(date_start=date_1days_time, date_end=date_1days_time + frequency_of_timed_task): #Same as above but on day before
            responded_member_ids = get_responded(assignment)
            for member in [member for member in assignment.accepted_by if member.id not in responded_member_ids]:
                member.send_notification( messages.assignment_due_1day (you=member, assignment=assignment) )
        
        Session.commit()
        return response_completed_ok


    #---------------------------------------------------------------------------
    # Message Clean
    #---------------------------------------------------------------------------

    def message_clean(self):
        """
        The message table could expand out of control and the old messages
        need to be removed automatically from the db
        """
        pass

    #---------------------------------------------------------------------------
    # New Users and Groups Summary
    #---------------------------------------------------------------------------
    @web_params_to_kwargs
    def email_new_user_summary(self, frequency_of_timed_task="days=1"):
        """
        query for all users in last <timedelta> and email 
        """
        frequency_of_timed_task = timedelta_str(frequency_of_timed_task)
        
        from civicboom.model import Member
        members = Session.query(Member) \
                    .with_polymorphic('*') \
                    .filter(Member.join_date>=normalize_datetime(now()) - frequency_of_timed_task) \
                    .all()
        
        if not members:
            log.debug('Report not generated: no new members in %s' % frequency_of_timed_task)
            return response_completed_ok
        
        from civicboom.lib.communication.email_lib import send_email
        send_email(
            config['email.event_alert'],
            subject      ='new user registration summary',
            content_html = render(
                            '/email/admin/summary_new_users.mako',
                            extra_vars = {
                                "members"   : members                 ,
                                "timedelta" : frequency_of_timed_task ,
                            }
                        ),
        )
        
        return response_completed_ok


    def purge_unneeded_warehouse_media(self):
        """
        Compare the warehouse files with the database media list.
        If media records have been removed then we can safly remove them from the warehouse
        """
        #        it also may be worth looking for media records without an associated content record and removeing them as well
        pass


    #---------------------------------------------------------------------------
    # Test Task
    #---------------------------------------------------------------------------

    def test(self):
        return "<task happened>"


    #---------------------------------------------------------------------------
    # One-off things
    #---------------------------------------------------------------------------

    def convert_descriptions(self):
        from civicboom.model.member import Member
        for m in Session.query(Member):
            if not m.description and "description" in m.config:
                m.description = m.config.get("description", "")
                del m.config['description']
            yield str(m.username + "\n")
        Session.commit()
