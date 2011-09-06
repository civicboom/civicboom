from civicboom.tests import *

from civicboom.lib.database.get_cached import get_member
from civicboom.model.payment import *
from civicboom.model.meta import Session
from sqlalchemy           import or_, and_, not_, null

import copy, datetime, urlparse

class TestPaymentController(TestController):
    """
    Tests for Payment Controller
    """
    
    payment_account_ids = {}
    
    def test_payment_all_ok(self):
        self.server_datetime('now')
        # Run invoice tasks to get any stray emails out of the way
        self.run_task('run_invoice_tasks')
        # Setup payment account numbers dict
        self.payment_account_ids = {}
        # Setup two accounts, ind and org & test invalid form entries for both!
        self.part_sign_up('test_payment_ind', 'ind')
        self.log_out()
        self.part_sign_up('test_payment_org', 'org')
        
        # Regrade org to free so as to get it out of the way...
        self.part_regrade('test_payment_org', 'free')
        # Check 0 invoices still billed for free acct
        assert len(get_member('test_payment_org').payment_account.invoices.filter(Invoice.status=='billed').all()) == 0
        
        # Shift date to check for two day payment fail
        self.server_datetime(datetime.datetime.now() + datetime.timedelta(days=1))
        # Should not send email as two days max unpaid
        emails = getNumEmails()
        self.run_task('run_invoice_tasks')
        assert emails == getNumEmails()
        self.part_check_member_status('test_payment_ind', 'waiting')
        
        self.server_datetime(datetime.datetime.now() + datetime.timedelta(days=2))
        # Should send email as two days max unpaid
        emails = getNumEmails()
        self.run_task('run_invoice_tasks')
        assert emails + 1 == getNumEmails()
        self.part_check_member_status('test_payment_ind', 'failed')
        
        # Get outstanding invoice balance, ensure > 0 and manually pay 5 towards
        outstanding = self.part_get_invoice('test_payment_ind').total_due
        assert outstanding > 0
        self.part_pay_invoice_manual(self.part_get_invoice('test_payment_ind'), 5)
        
        # Check outstanding invoice balance changed, ensure > 0 and manually pay the rest
        assert self.part_get_invoice('test_payment_ind').total_due == outstanding - 5
        assert self.part_get_invoice('test_payment_ind').total_due > 0
        self.part_pay_invoice_manual(self.part_get_invoice('test_payment_ind'), outstanding - 5)
        
        # Check no outstanding balance on invoice, run invoice tasks to change invoice status
        assert self.part_get_invoice('test_payment_ind').total_due == 0
        self.run_task('run_invoice_tasks')
        
        # Check invoice marked as paid & account is returned to "ok"
        assert self.part_get_invoice('test_payment_ind').status == 'paid'
        self.part_check_member_status('test_payment_ind', 'ok')
        
        # Move to next month & check invoice created email
        emails = getNumEmails()
        invoices = len(get_member('test_payment_ind').payment_account.invoices.all())
        self.server_datetime(datetime.datetime.now() + datetime.timedelta(days=27))
        self.run_task('run_invoice_tasks')
        self.assertEqual(getNumEmails(), emails + 1)
        self.assertEqual(len(get_member('test_payment_ind').payment_account.invoices.all()), invoices + 1)
        self.assertIn('invoiced', getLastEmail().content_text)
        # Move to invoice due date and test for invoice due email
        emails = getNumEmails()
        due_date = get_member('test_payment_ind').payment_account.invoices.filter(Invoice.status=='billed').one().due_date
        self.server_datetime(datetime.datetime.combine(due_date, datetime.time(0,0,0)))
        self.run_task('run_invoice_tasks')
        self.assertEqual(getNumEmails(), emails + 1)
        self.assertIn('overdue', getLastEmail().content_text)
        
        self.server_datetime('now')
        
    def test_payment_ok_paypal(self):
        self.server_datetime('now')
        self.run_task('run_invoice_tasks')
        self.part_sign_up('test_payment_paypal', 'org')
        self.run_task('run_invoice_tasks')
        self.part_check_member_status('test_payment_paypal', 'waiting')
        outstanding = self.part_get_invoice('test_payment_paypal').total_due
        
        # Get the invoice and call payment_begin for paypal
        invoice = self.part_get_invoice('test_payment_paypal')
        response = self.app.get(
            url(controller='payment_actions', id=invoice.payment_account.id, action='payment_begin', invoice_id=invoice.id, service="paypal_express"),
            status=302
        )
        # Check correct response
        assert 'sandbox.paypal.com' in response
        # Grab 302'd url and token query parameter
        redirect_location = response.response.headers['location']
        redirect_token = urlparse.parse_qs(urlparse.urlparse(redirect_location).query)['token'][0]
        # Check we got a "TESTTOKEN" back (actual token would be "TESTTOKEN-0" for e.g.)
        assert 'TESTTOKEN' in redirect_token
        
        # Get the invoice and call payment_return for paypal
        invoice = self.part_get_invoice('test_payment_paypal')
        response = self.app.get(
            url(controller='payment_actions', id=invoice.payment_account.id, action='payment_return', invoice_id=invoice.id, service="paypal_express", token=redirect_token, PayerID='rar'),
            status=302
        )
        
        self.run_task('run_invoice_tasks')
        invoice = self.part_get_invoice('test_payment_paypal')
        print invoice, invoice.status, invoice.transactions[0].status, invoice.paid_total, invoice.total, invoice.total_due
        assert invoice.status == 'paid'
        self.part_check_member_status('test_payment_paypal', 'ok')
        self.server_datetime('now')
        
    def test_payment_ok_paypal_recurring(self):
        self.server_datetime('now')
        self.run_task('run_invoice_tasks')
        self.part_sign_up('test_payment_paypal_rec', 'org')
        self.run_task('run_invoice_tasks')
        self.part_check_member_status('test_payment_paypal_rec', 'waiting')
        outstanding = self.part_get_invoice('test_payment_paypal_rec').total_due
        
        # Get the invoice and call payment_begin for paypal
        invoice = self.part_get_invoice('test_payment_paypal_rec')
        response = self.app.get(
            url(controller='payment_actions', id=invoice.payment_account.id, action='payment_begin', invoice_id=invoice.id, service="paypal_express", recurring="True"),
            status=302
        )
        # Check correct response
        assert 'sandbox.paypal.com' in response
        # Grab 302'd url and token query parameter
        redirect_location = response.response.headers['location']
        redirect_token = urlparse.parse_qs(urlparse.urlparse(redirect_location).query)['token'][0]
        # Check we got a "TESTTOKEN" back (actual token would be "TESTTOKEN-0" for e.g.)
        assert 'TESTTOKEN' in redirect_token
        
        # Get the invoice and call payment_return for paypal
        invoice = self.part_get_invoice('test_payment_paypal_rec')
        response = self.app.get(
            url(controller='payment_actions', id=invoice.payment_account.id, action='payment_return', invoice_id=invoice.id, service="paypal_express", token=redirect_token, PayerID='rar'),
            status=302
        )
        
        # Check recurring billing account has been created
        bacct = self.part_get_billing_account('test_payment_paypal_rec')
        bacct_id = bacct.id
        self.assertNotEqual(bacct, None)
        self.assertIn('paypal_recurring', bacct.provider)
        
        self.run_task('run_invoice_tasks')
        invoice = self.part_get_invoice('test_payment_paypal_rec')
        print invoice, invoice.status, invoice.transactions[0].status, invoice.paid_total, invoice.total, invoice.total_due
        assert invoice.status == 'paid'
        self.part_check_member_status('test_payment_paypal_rec', 'ok')
        self.server_datetime('now')
        
        # Move to next month & generate invoice so we can test (what greg believes to be) paypal recurring behaviour
        self.server_datetime(datetime.datetime.now() + datetime.timedelta(days=27))
        self.run_task('run_invoice_tasks')
        
        invoice = self.part_get_invoice('test_payment_paypal_rec')
        invoice_id = invoice.id
        print invoice.due_date, invoice, invoice.status
        
        self.assertEqual(invoice.status, 'billed')
        
        self.run_task('run_billing_account_tasks')
        
        transaction = Session.query(BillingTransaction).filter(and_(BillingTransaction.invoice_id==None,BillingTransaction.billing_account_id==bacct_id)).one()
        self.assertIn('BP-TESTTOKEN', transaction.reference)
        trans_id = transaction.id
        
        self.run_task('run_match_billing_transactions')
        transaction = Session.query(BillingTransaction).get(trans_id)
        self.assertIsNotNone(transaction)
        
        self.assertEqual(transaction.invoice_id, invoice_id)
        self.assertIsNone(transaction.billing_account_id)
        
        #self.run_task('')
        
        # Cancel billing account
        response = self.app.post(
            url(controller='payment_actions', id=self.payment_account_ids['test_payment_paypal_rec'], action='billing_account_deactivate', format='json'),
            params={
            '_authentication_token': self.auth_token,
            'billing_account_id'          : bacct_id,
            },
            status=200
        )
        self.server_datetime('now')
        
        
        
    def test_payment_cancel_paypal(self):
        self.server_datetime('now')
        self.run_task('run_invoice_tasks')
        self.part_sign_up('test_payment_pp_cancel', 'org')
        self.run_task('run_invoice_tasks')
        self.part_check_member_status('test_payment_pp_cancel', 'waiting')
        outstanding = self.part_get_invoice('test_payment_pp_cancel').total_due
        
        # Get the invoice and call payment_begin for paypal
        invoice = self.part_get_invoice('test_payment_pp_cancel')
        response = self.app.get(
            url(controller='payment_actions', id=invoice.payment_account.id, action='payment_begin', invoice_id=invoice.id, service="paypal_express"),
            status=302
        )
        # Check correct response
        assert 'sandbox.paypal.com' in response
        # Grab 302'd url and token query parameter
        redirect_location = response.response.headers['location']
        redirect_token = urlparse.parse_qs(urlparse.urlparse(redirect_location).query)['token'][0]
        # Check we got a "TESTTOKEN" back (actual token would be "TESTTOKEN-0" for e.g.)
        assert 'TESTTOKEN' in redirect_token
        
        # Get the invoice and call payment_return for paypal
        invoice = self.part_get_invoice('test_payment_pp_cancel')
        response = self.app.get(
            url(controller='payment_actions', id=invoice.payment_account.id, action='payment_cancel', invoice_id=invoice.id, service="paypal_express", token=redirect_token, PayerID='rar'),
            status=302
        )
        
        self.run_task('run_invoice_tasks')
        invoice = self.part_get_invoice('test_payment_pp_cancel')
        print invoice, invoice.status, invoice.transactions[0].status, invoice.paid_total, invoice.total, invoice.total_due
        assert invoice.status == 'billed'
        assert invoice.transactions[0].status == 'cancelled'
        self.part_check_member_status('test_payment_pp_cancel', 'waiting')
        self.server_datetime('now')
        
    def test_all_billing_tasks(self):
        self.server_datetime('now')
        self.run_task('run_billing_tasks')
        
        
    #===========================================================================
    # Subroutines used for the tests above
    #===========================================================================
    def part_get_invoice(self, username, offset=0):
        """
        Get the invoice at offset for username
        """
        return get_member(username).payment_account.invoices[offset]
        
    def part_pay_invoice_manual(self, invoice, amount=None):
        """
        Create a manual transaction against invoice
        """
        txn = BillingTransaction()
        txn.invoice = invoice
        txn.status = 'complete'
        txn.amount = amount or invoice.total_due
        txn.provider = 'manual_test'
        txn.reference = 'test'
        Session.commit()
        pass
    
    def part_check_member_status(self, username, status):
        """
        Check member status against status parameter
        """
        member = get_member(username)
        self.assertEqual(member.payment_account.billing_status, status)
        
        pac_type = 'free' if status == 'failed' else member.payment_account.type
        self.assertEqual(member.account_type, pac_type)
        
    def part_sign_up(self, username, name_type="ind", type="plus"):
        """
        Sign up to the site, create payment account (testing each required field), check account is waiting)
        """
        self.sign_up_as(username)
        # New member should have no payment account
        member = get_member(username)
        assert member.payment_account == None
        
        # Check redirect from index when no payment account
        response = self.app.get(
            '/payments',
            status=302
        )
        
        params = {
            '_authentication_token': self.auth_token,
            'name_type'         : name_type,
            'org_name'          : ("%s's Organisation Name" % username) if name_type == 'org' else '',
            'ind_name'          : ("%s's Individual Name" % username) if name_type == 'ind' else '',
            'address_1'         : 'Address 1',
            'address_2'         : 'Address 2',
            'address_town'      : 'Town',
            'address_county'    : 'County',
            'address_postal'    : 'PO5 7AL',
            'address_country'   : 'GB',
            'plan_%s' % type    : 'blah',
        }
        # Check each required field for invalid
        for field in ['name_type', '%s_name' % name_type, 'address_1', 'address_town', 'address_country', 'address_postal']:
            params_invalid = copy.deepcopy(params)
            params_invalid[field] = ''
            response = self.app.post(
                url('payments', format="json"),
                params=params_invalid,
                status=400
            )
        # Create a payment account
        response = self.app.post(
            url('payments', format='json'),
            params=params,
            status=200
        )
        # Get member from DB
        member = get_member(username)
        # Set payment account number
        self.payment_account_ids[username] = member.payment_account.id
        # Check upgraded to plus account
        assert member.payment_account.type == type
        # Check name set on account, also tests index
        response = self.app.get(
            url('payments', format='json'),
            status=200
        )
        assert (("%s's Individual Name" % username) if name_type == 'ind' else ("%s's Organisation Name" % username)) in response
        
        # Check edit page
        response = self.app.get(
            url('edit_payment', id=self.payment_account_ids[username]),
            status=200
        )
        
        # Change a field
        params['_authentication_token'] = self.auth_token
        params['address_postal']        = 'PO5_7AL_TESTING'
        response = self.app.put(
            url(controller='payments', id=self.payment_account_ids[username], action="update", format='json'),
            params=params,
            status=200
        )
        # Check field changed, also tests show!
        response = self.app.get(
            url('payments', id=self.payment_account_ids[username], format='json'),
            status=200
        )
        assert 'PO5_7AL_TESTING' in response
        # Get member from DB
        member = get_member(username)
        # Check have one invoice
        invoices = member.payment_account.invoices
        assert len(invoices.all()) == 1
        # Check invoice is billed
        assert invoices[0].status == 'billed'
        # Check invoice total due > 0
        assert invoices[0].total_due > 0
        
        # Check invoice show
        response = self.app.get(
            url(controller='payment_actions', id=self.payment_account_ids[username], action='invoice', invoice_id=invoices[0].id),
            status=200
        )
        assert 'Invoice' in response
        
        # Should not send email as redirected to invoice already, plus account waiting sends overdue email :(
        emails = getNumEmails()
        self.run_task('run_invoice_tasks')
        assert emails == getNumEmails()
        
        # Get member from DB
        member = get_member(username)
        # Check account billing_status is currently 'waiting' (as the invoice is already due!)
        assert member.payment_account.billing_status == 'waiting'
        
        self.sign_up_as('%s_add_me'%username)
        
        self.log_in_as(username)
        
        response = self.app.post(
            url(controller='payment_actions', id=self.payment_account_ids[username], action='member_remove', format='json'),
            params={
            '_authentication_token': self.auth_token,
            'username'          : username,
            },
            status=400
        )
        
        members_len = len(get_member(username).payment_account.members)
        
        response = self.app.post(
            url(controller='payment_actions', id=self.payment_account_ids[username], action='member_add', format='json'),
            params={
            '_authentication_token': self.auth_token,
            'username'          : '%s_add_me'%username,
            },
            status=200
        )
        
        assert len(get_member(username).payment_account.members) == members_len + 1
        
        response = self.app.post(
            url(controller='payment_actions', id=self.payment_account_ids[username], action='member_remove', format='json'),
            params={
            '_authentication_token': self.auth_token,
            'username'          : '%s_add_me'%username,
            },
            status=200
        )
        
        assert len(get_member(username).payment_account.members) == members_len
        
    def part_regrade(self, username, type="free"):
        """
        Regrade account to type (default free)
        """
        response = self.app.post(
            url(controller='payment_actions', action='regrade', id=self.payment_account_ids[username], format="json"),
            params=dict(
                new_type=type
            ),
            status=200)
        
        assert get_member(username).payment_account.type == type
    
    def part_get_billing_account(self, username):
        """
        Get the user's first billing account
        """
        return get_member(username).payment_account.billing_accounts[0]
        
        