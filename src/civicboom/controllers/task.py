"""
Task Controller
Maintinence tasks that can be tiggered via cron jobs

All tasks are locked down to be executed by localhost only
See the companion script "tasks.py" in the project root for details on how to
setup a cron job to run these tasks
"""

from civicboom.lib.base import *

from cbutils.misc import timedelta_str

from sqlalchemy import and_, or_

from sqlalchemy.orm import aliased

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
        #          Shish can you fix this properly. www.civicboom.com should not be hard coded here, it should not be in python code, should be in a cfg file somewhere
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

    # GregM: Invoice processing
    def run_invoice_tasks(self):
        # Import model objects
        from civicboom.model.payment import Service, ServicePrice, Invoice, InvoiceLine, BillingAccount, BillingTransaction, PaymentAccountService
        from civicboom.model.member import PaymentAccount
        
        # Set variables
        time_now = datetime.datetime.now()
        days_disable = 6
        days_remind = 3
        days_invoice_in = 7
        seven_days = time_now + datetime.timedelta(days=days_invoice_in)
        
        # Create sql where clauses for checking start dates (SQL used as date_part functions are indexed in postgres)
        def filter_start_dates(query, table=''):
            if table:
                table += '.'
            filter = ""
            if frequency == "month":
                # start day:
                filter += "date_part('day', start_date) >= %(day_s)i " % {'day_s':time_now.day}
                # and if end day in same month, else or:
                filter += "and" if seven_days.day > time_now.day else "or"
                # end day:
                filter += " date_part('day', start_date) < %(day_e)i" % {'day_e':seven_days.day}
            elif frequency == "year":
                ## Month 1! & start day:
                filter += "(date_part('month', start_date) = %(month_s)i and date_part('day', start_date) >= %(day_s)i) or " % {'month_s': time_now.month, 'day_s': time_now.day}
                ## Month 2?:
                filter += "(date_part('month', start_date) = %(month_e)i and " % {'month_e': seven_days.month if time_now.month < seven_days.month else time_now.month}
                ##          & end day:
                filter += "date_part('day', start_date) < %(day_e)i)" % {'day_e': seven_days.day}
                
            return query.filter("(%s)" % (filter))
        
        def check_timestamp(timestamp, days):
            return timestamp > (time_now - datetime.timedelta(days=days)) and timestamp < (time_now - datetime.timedelta(days=days-1))
        
        # Calculate the next bill date for a service based on the service's start date (rounding down to nearest day, e.g. start 29/02/2000 -> 28/02/2010)
        def next_start_date(start_date, frequency, offset=0):
            _start_date = start_date
            for i in range(10):
                try:
                    if frequency == "year":
                        _start_date = _start_date.replace(year=time_now.year+offset)
                    elif frequency == "month":
                        _start_date = _start_date.replace(year=time_now.year, month=time_now.month+offset)
                    break
                except ValueError:
                    start_date = _start_date.replace(day=_start_date.day-1)
            if _start_date < time_now.date():
                _start_date = next_start_date(start_date, frequency, 1)
            return _start_date
        
        # For each billing frequency get accounts likely to be due in the next x days
        for frequency in ["month", "year"]:
            # Get accounts due in the next x days and have paid services:
            unbilled_accounts = filter_start_dates(
                    Session.query(PaymentAccount)\
                    .filter(PaymentAccount.frequency == frequency)
                )\
                .join((Service, Service.payment_account_type == PaymentAccount.type))\
                .join((ServicePrice, ServicePrice.service_id == Service.id and ServicePrice.frequency == frequency))\
                .filter(ServicePrice.amount > 0)\
                .all()
            # For each account found determine if invoice already exists & if not produces an invoice
            for account in unbilled_accounts:
                currency = account.currency
                
                # Calculate the start date we are going to try and invoice for
                start_date = next_start_date(account.start_date, frequency)
                
                #Check for invoices with the start date already in the system (not disregarded though!)
                check = account.invoices.filter(Invoice.status != "disregarded")\
                    .join((InvoiceLine, InvoiceLine.invoice_id == Invoice.id))\
                    .filter(InvoiceLine.start_date == start_date)\
                    .join((Service, Service.id == InvoiceLine.service_id))\
                    .filter(Service.payment_account_type == account.type).first()
                if check:
                    continue
                
                # Get the service object applicable for this account
                service = Session.query(Service).filter(Service.payment_account_type == account.type).one()
                
                # Create a new Invoice object & set the due date to the service start date
                invoice = Invoice(account)
                invoice.due_date = start_date
                
                # Check if there is a payment account service set-up for this account (allows discount, etc. to be applied)
                payment_account_service = Session.query(PaymentAccountService).filter(PaymentAccountService.payment_account_id == account.id)\
                    .filter(PaymentAccountService.service_id == service.id).first()
                
                # Create billing line for the account's main service type
                line = InvoiceLine(
                       invoice,
                       payment_account_service  = payment_account_service,
                       service                  = service,
                       frequency                = frequency,
                       start_date               = start_date
                   )
                invoice.lines.append(line)
                
                # Loop through the rest of the services and create billing lines
                # TODO: This needs to take into account service frequency / account frequency, etc.
                for payment_account_service in account.services:
                    if payment_account_service.service.payment_account_type != account.type:
                        line = InvoiceLine(invoice, payment_account_service.service, frequency)
                        invoice.lines.append(line)
                        #lines.append(line)
                
                # Commit the invoice before changing status or the commit will fail db level security check!
                Session.add(invoice)
                Session.commit()
                
                # TODO: Any Invoice changes need to go here!
                
                # Change invoice status to billed, no further changes can be made to invoice and related lines from now onwards!
                invoice.status = "billed"
                Session.commit()
        
        ## Process 2: Check all billed invoices & update accounts accordingly
        billed_invoices = Session.query(Invoice).filter(Invoice.status == "billed").all()
        for invoice in billed_invoices:
            if invoice.paid_total >= invoice.total:
                # This shouldn't really happen, invoices should be marked as paid when payments are successful, but just in case:
                invoice.status = "paid"
                Session.commit()
                if invoice.payment_account.billing_status != "ok":
                    if len([inv for inv in invoices.payment_account.invoices if inv.status == 'billed']) == 0:
                        invoice.payment_account.billing_status = "ok"
                    # Send invoice cleared thanks email
                # TODO: if invoice.paid_total > invoice.total:
                #    refund overpayment
            elif check_timestamp(invoice.timestamp, days_disable):
                if invoice.payment_account.billing_status != "failed":
                    # Send account disabled email
                    invoice.payment_account.billing_status = "failed"
                else:
                    # Send account disabled reminder email
                    pass
            elif check_timestamp(invoice.timestamp, days_remind):
                # Send reminder email
                pass
            else:
                if invoice.due_date > time_now.date():
                    if invoice.payment_account.billing_status != "invoiced":
                        invoice.payment_account.billing_status = "invoiced"
                        # Send invoice created email
                else:
                    if invoice.payment_account.billing_status != "waiting":
                        invoice.payment_account.billing_status = "waiting"
                        # Send invoice due email
        Session.commit()
        return response_completed_ok
    
    # GregM: Invoice processing
    def run_transaction_tasks(self):
        from civicboom.model.payment import Service, ServicePrice, Invoice, InvoiceLine, BillingAccount, BillingTransaction, PaymentAccountService
        from civicboom.controllers.payment_actions import paypal_interface
        from civicboom.model.member import PaymentAccount
        transactions = Session.query(BillingTransaction).filter(BillingTransaction.status=='pending').all()
        
        for txn in transactions:
            if txn.provider == 'paypal_express':
                try:
                    response = paypal_interface.get_transaction_details(
                        transactionid = txn.config['transaction_id'],
                    )
                except:
                    pass
                else:
                    if response.PAYMENTSTATUS in ('Completed',):
                        txn.status = 'complete'
                        if txn.invoice.total_paid >= txn.invoice.total:
                            txn.invoice.status = 'paid'
                    pass
            pass
        
        Session.commit()
        return response_completed_ok
        pass

    #---------------------------------------------------------------------------
    # Publish Sceduled Assignments
    #---------------------------------------------------------------------------
    @web_params_to_kwargs
    def publish_sceduled_content(self, frequency_of_timed_task="hours=1"):
        """
        query for all users in last <timedelta> and email 
        """
        frequency_of_timed_task = timedelta_str(frequency_of_timed_task)
        datetime_now            = normalize_datetime(now())
        
        from civicboom.model.content        import DraftContent
        from civicboom.controllers.contents import ContentsController
        content_publish = ContentsController().update
        
        def get_content_to_publish(date_start, date_end):
            return Session.query(DraftContent).filter(and_(DraftContent.auto_publish_trigger_datetime >= date_start, DraftContent.auto_publish_trigger_datetime <= date_end)).all()
        
        # AllanC - calls will be made to content.py:update this will trigger the normal decorators, we need to ensure that these dont prohibit the update call's we are about to make
        c.authenticated_form = True     # AllanC - Fake the authenticated status so that the auth decorator does not tigger
        c.format             = 'python'
        
        for content in get_content_to_publish(datetime_now, datetime_now + frequency_of_timed_task):
            log.info('Auto publishing content #%s - %s' % (content.id, content.title))
            # By calling the content:update method with no param with the content as a draft, it automatically pubishs the content
            content_publish(content, submit_publish=True)
        
        return response_completed_ok

    #---------------------------------------------------------------------------
    # Warehouse Managment
    #---------------------------------------------------------------------------
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
