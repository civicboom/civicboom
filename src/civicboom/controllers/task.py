"""
Task Controller
Maintinence tasks that can be tiggered via cron jobs

All tasks are locked down to be executed by localhost only
See the companion script "tasks.py" in the project root for details on how to
setup a cron job to run these tasks
"""

from civicboom.lib.base import *

from cbutils.misc import timedelta_from_str, set_now

from sqlalchemy import and_, or_, null

from sqlalchemy.orm import aliased

from civicboom.lib.payment.functions import *

import datetime

import civicboom.lib.payment as payment

log = logging.getLogger(__name__)

from civicboom.lib.communication.email_lib import send_email as send_email

response_completed_ok = "task:ok" #If this is changed please update tasks.py to reflect the same "task ok" string

def send_payment_admin_email(subject, content_text):
    send_email(config['email.payment_alert'],
        subject=subject,
        content_text=content_text,
    )

def normalize_datetime(d, accuracy='hour'):
    """
    Normalizez datetime down to hour or day
    Dates are immutable (thank god)
    """
    if   accuracy=='hour':
        return d.replace(minute=0, second=0, microsecond=0)
    elif accuracy=='day' :
        return d.replace(minute=0, second=0, microsecond=0, hour=0)
    elif accuracy=='week':
        return d.replace(minute=0, second=0, microsecond=0, hour=0) - datetime.timedelta(days=d.weekday())
    return d

def process_db_chunk(query, process_item, limit=None):
    if not limit:
        limit = config['timedtask.batch_chunk_size']
    count = query.count()
    for offset in [i*limit for i in range(0, (count/limit)+1)]:
        results = query.offset(offset).limit(limit).all()
        for result in results:
            process_item(result)
    

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
        
        frequency_of_timed_task = timedelta_from_str(frequency_of_timed_task)
        remind_after            = timedelta_from_str(remind_after           )
        
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
        
        ghost_expire = normalize_datetime(now() - timedelta_from_str(delete_older_than))
        
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
        
        frequency_of_timed_task = timedelta_from_str(frequency_of_timed_task)
        
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
        frequency_of_timed_task = timedelta_from_str(frequency_of_timed_task)
        
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
    
    #---------------------------------------------------------------------------
    # Run the below billing tasks (easier for overnight batches)
    #---------------------------------------------------------------------------
    def run_billing_tasks(self):
        self.run_invoice_tasks()
        self.run_transaction_tasks()
        self.run_billing_account_tasks()
        self.run_match_billing_transactions()
        return response_completed_ok
        
    #---------------------------------------------------------------------------
    # Create invoices (up to 7 days in advance)
    # Sets payment account status in accordance with our payment rules
    #---------------------------------------------------------------------------
    def run_invoice_tasks(self):
        # Import model objects
        from civicboom.model.payment import Service, ServicePrice, Invoice, InvoiceLine, BillingAccount, BillingTransaction, PaymentAccountService
        from civicboom.model.member import PaymentAccount
        
        # Set variables
        time_now = now()
        days_disable = 2
        days_remind = 3
        days_invoice_in = 7
        seven_days = time_now + datetime.timedelta(days=days_invoice_in)
        
        def check_timestamp(timestamp, days):
            if isinstance(timestamp, datetime.date):
                timestamp = datetime.datetime.combine(timestamp, datetime.time(0))
            if timestamp > time_now:
                return False
            return (time_now - timestamp).days >= days
        
        # For each billing frequency get accounts likely to be due in the next x days
        for frequency in ["month", "year"]:
            # Get accounts due in the next x days and have paid services:
            unbilled_accounts = payment.db_methods.filter_start_dates(
                    Session.query(PaymentAccount)\
                    .filter(PaymentAccount.do_not_bill==False)\
                    .filter(PaymentAccount.frequency == frequency),
                    frequency, time_now, seven_days,
                )\
                .join((Service, Service.payment_account_type == PaymentAccount.type))\
                .join((ServicePrice, ServicePrice.service_id == Service.id and ServicePrice.frequency == frequency))\
                .filter(ServicePrice.amount > 0)\
                .all()
            # For each account found determine if invoice already exists & if not produces an invoice
            for account in unbilled_accounts:
                currency = account.currency
                
                # Calculate the start date we are going to try and invoice for
                # If next start date is today we calculate for today!
                start_date = payment.calculate_start_date(account.start_date, frequency, time_now)
                
                #Check for invoices with the start date already in the system (not disregarded though!)
                check = account.invoices.filter(Invoice.status != "disregarded")\
                    .join((InvoiceLine, InvoiceLine.invoice_id == Invoice.id))\
                    .filter(InvoiceLine.start_date == start_date)\
                    .join((Service, Service.id == InvoiceLine.service_id))\
                    .filter(Service.payment_account_type == account.type).first()
                if check:
                    continue
                
                #Generate the invoice (note the invoice will be committed with status == 'unbilled'
                invoice = payment.db_methods.generate_invoice(account, start_date)
                
                # Any Invoice changes need to go here!
                
                # Change invoice status to billed, no further changes can be made to invoice and related lines from now onwards!
                invoice.status = "billed"
                Session.commit()
        
        payment_account_status = [
            "ok",
            "invoiced",
            "waiting",
            "failed",
        ]
            
        def send_email_admins(account, **kwargs):
            for user in account.get_admins():
                send_email(user, **kwargs)
        
        ## Process 2 new: Check all payment accounts with outstanding invoices
        billed_accounts = Session.query(PaymentAccount)\
            .join((Invoice, Invoice.payment_account_id == PaymentAccount.id))\
            .filter(Invoice.status == "billed").all()
        for account in billed_accounts:
            max_acct_status = -1
            count_unpaid = 0
            # Check all billed invoices
            for invoice in account.invoices.filter(Invoice.status == "billed").all():
                if invoice.paid_total >= invoice.total:
                    invoice.status = "paid"
                    max_acct_status = max((max_acct_status, payment_account_status.index("ok" )))
                elif check_timestamp(invoice.due_date, days_disable):
                    max_acct_status = max((max_acct_status, payment_account_status.index("failed" )))
                else:
                    if check_timestamp(invoice.timestamp, days_remind):
                        pass
                    if invoice.due_date > time_now.date():
                        max_acct_status = max((max_acct_status, payment_account_status.index("invoiced" )))
                    else:
                        max_acct_status = max((max_acct_status, payment_account_status.index("waiting" )))
            # Update account
            if max_acct_status > -1:
                new_status      = payment_account_status[max_acct_status]
                new_status_n    = max_acct_status
                old_status      = invoice.payment_account.billing_status
                old_status_n    = payment_account_status.index(old_status)
                
                if new_status_n != old_status_n:
                    invoice.payment_account.billing_status = new_status
                    Session.commit()
                    if new_status == "failed":
                        send_email_admins(account, subject=_('_site_name: Service disabled'), content_html=render('/email/payment/account_failed.mako', extra_vars={}))
                        send_payment_admin_email('Account disabled %s' % invoice.payment_account.name, 'Account #%s (%s) has been disabled for non payment!' % (invoice.payment_account.id, invoice.payment_account.name))
                        #account.send_email_admins(subject=_('_site_name: Service disabled'), content_html=render('/email/payment/account_failed.mako', extra_vars={}))
                        pass #Send account disabled email
                    elif new_status == "waiting":
                        send_payment_admin_email('Account set WAITING %s' % invoice.payment_account.name, 'Account #%s (%s) has an invoice with due date today (will be disabled soon!)!' % (invoice.payment_account.id, invoice.payment_account.name))
                        send_email_admins(account, subject=_('_site_name: Invoice nearly overdue'), content_html=render('/email/payment/account_waiting.mako', extra_vars={}))
                        #account.send_email_admins(subject=_('_site_name: Invoice nearly overdue'), content_html=render('/email/payment/account_waiting.mako', extra_vars={}))
                        pass #Send account due email
                    elif new_status == "invoiced":
                        send_payment_admin_email('Account set INVOICED %s' % invoice.payment_account.name, 'Account #%s (%s) has been invoiced!' % (invoice.payment_account.id, invoice.payment_account.name))
                        send_email_admins(account, subject=_('_site_name: Account invoiced'), content_html=render('/email/payment/account_invoiced.mako', extra_vars={}))
                        #account.send_email_admins(subject=_('_site_name: Account invoiced'), content_html=render('/email/payment/account_invoiced.mako', extra_vars={}))
                        pass #Send account invoiced email
                    elif new_status == "ok":
                        send_payment_admin_email('Account set OK %s' % invoice.payment_account.name, 'Account #%s (%s) has paid their invoice(s)!' % (invoice.payment_account.id, invoice.payment_account.name))
                        pass #Send account all ok, thank you, email

        Session.commit()
        return response_completed_ok
    #---------------------------------------------------------------------------
    # Update the status of any pending transactions
    #---------------------------------------------------------------------------
    def run_transaction_tasks(self):
        from civicboom.model.payment import Service, ServicePrice, Invoice, InvoiceLine, BillingAccount, BillingTransaction, PaymentAccountService
        from civicboom.model.member import PaymentAccount
        transactions = Session.query(BillingTransaction)\
            .filter(BillingTransaction.status=='pending')\
            .filter(BillingTransaction.status_updated < (now() - datetime.timedelta(hours=3)))\
            .all()
        
        for txn in transactions:
            if txn.provider in payment.check_transactions:
                try:
                    response = payment.check_transactions[txn.provider](
                        reference = txn.config['transaction_id']
                    )
                except:
                    pass
                else:
                    txn.status = response['status']
                    if txn.status == 'complete':
                        if txn.invoice.total_paid >= txn.invoice.total:
                            txn.invoice.status = 'paid'
                    txn.status_updated = now()
        
        Session.commit()
        return response_completed_ok
    #---------------------------------------------------------------------------
    # Update status of active and pending billing accounts & create any transactions
    #  This is mostly for PayPal as they bill separately to our invoices
    #---------------------------------------------------------------------------
    def run_billing_account_tasks(self):
        from civicboom.model.payment import Service, ServicePrice, Invoice, InvoiceLine, BillingAccount, BillingTransaction, PaymentAccountService
        from civicboom.model.member import PaymentAccount
        
        billing_accounts = Session.query(BillingAccount)\
            .filter(or_(BillingAccount.status=='pending', BillingAccount.status=='active'))\
            .filter(BillingAccount.status_updated < (now() - datetime.timedelta(hours=3)))\
            .all()
        
        for billing_account in billing_accounts:
            if billing_account.provider in payment.check_recurrings:
                response = payment.check_recurrings[billing_account.provider](billing_account.reference)
                if response['status'] != 'error':
                    billing_account.status = response['status']
                    if 'create_transaction_if' in response:
                        cti = response['create_transaction_if']
                        if not Session.query(BillingTransaction).filter(and_(BillingTransaction.provider==cti['provider'], BillingTransaction.timestamp==cti['timestamp'])).first():
                            txn = BillingTransaction()
                            txn.timestamp       = cti['timestamp']
                            txn.status          = cti['status']
                            txn.amount          = cti['amount']
                            txn.billing_account = billing_account
                            txn.provider        = cti['provider']
                            txn.reference       = cti['reference']
            billing_account.status_updated = now()
            
        Session.commit()
        return response_completed_ok
    #---------------------------------------------------------------------------
    # Match any automated billing transactions to billed invoices
    #  (e.g. paypal recurring payments, which annoyingly happen separately to
    #   invoicing)
    #---------------------------------------------------------------------------
    def run_match_billing_transactions(self):
        from civicboom.model.payment import Service, ServicePrice, Invoice, InvoiceLine, BillingAccount, BillingTransaction, PaymentAccountService
        unmatched_txns = Session.query(BillingTransaction).filter(and_(BillingTransaction.invoice_id==None, BillingTransaction.billing_account_id!=None)).all()
        for txn in unmatched_txns:
            within = datetime.timedelta(days=3)
            txn_date = txn.timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
            # Check for Invoices produced within 4 days of this transactions (28th->1st max 2.x days, 30th->1st max 2.x days, this should cover most eventualities)
            pending_invoices = txn.billing_account.payment_account.invoices.filter(
                and_(
                    Invoice.status=='billed',
                    Invoice.due_date > (txn_date-within),
                    Invoice.due_date < (txn_date+within)
                )
            ).filter(
                Invoice.total_due > 0
            ).all()
            if pending_invoices:
                txn.invoice = pending_invoices[0]
                txn.billing_account = None
            else:
                send_payment_admin_email('Unmatched Transaction %s' % txn.id, "We've searched as hard as we can, but the Civicboom hamsters and I can't find the invoice to match transaction %s to. Maybe your human eyes are better after all!" % txn.id)
        Session.commit()
        return response_completed_ok
    
    
    #---------------------------------------------------------------------------
    # Publish Sceduled Assignments
    #---------------------------------------------------------------------------
    @web_params_to_kwargs
    def publish_scheduled_content(self, frequency_of_timed_task="hours=1"):
        """
        query for all users in last <timedelta> and email 
        """
        frequency_of_timed_task = timedelta_from_str(frequency_of_timed_task)
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
    # Summary notification emails
    #---------------------------------------------------------------------------
    @web_params_to_kwargs
    def summary_notification_email(self, frequency_of_timed_task="hours=1"):
        """
        users that have flag themselfs as requesting summary emails can have 24 hours of notifications summerised
        
        TODO: In future this could take into account utc offset
        TODO: don't change the frequencey from 1 hour as this break interval_anchor
        """
        from civicboom.model import User, Message
        from sqlalchemy      import null
        
        frequency_of_timed_task = timedelta_from_str(frequency_of_timed_task)
        datetime_now            = normalize_datetime(now())
        
        def summary_notification_email_user(user):
            """
            All users passed to this methdod have been selected using a query to ensure they have the field 'summary_email_interval'
            """
            # Normalize the interval and ancor to the previous hour to assess if we are on a interval boundary
            if user.summary_email_start:
                interval_ancor = datetime_now - normalize_datetime(user.summary_email_start, accuracy='hour') # todo ... this really should be linked the frequncy of timed task
            else:
                interval_ancor = datetime_now - normalize_datetime(datetime_now            , accuracy='week')
            interval_ancor = interval_ancor.total_seconds()
            interval       = user.summary_email_interval.total_seconds()
            
            # If on interval boundary
            if (interval_ancor % interval) == 0:
                # Select all messages from since the previous interval
                messages = Session.query(Message).filter(or_(Message.target_id==user.id,Message.source_id==user.id)).filter(Message.timestamp >= (datetime_now-user.summary_email_interval)).order_by(Message.timestamp).all()
                # No need to send email summary if no messages have been generated in the last interval
                if messages:
                    content_html = render('/email/notifications/summary.mako', extra_vars={'messages':messages, 'user':user})
                    user.send_email(
                        subject      = _('_site_name: Summary'),
                        content_html = content_html,
                    )
                    
                    # Test output - used to debug email layout
                    #import os
                    #file = open(os.path.expanduser("~/Temp/out.html"), 'w')
                    #file.write(content_html)
                    #file.close()
        
        process_db_chunk(
            Session.query(User).filter(User.summary_email_interval!=null()), #and_(User.summary_email_start, 
            summary_notification_email_user
        )
        
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
