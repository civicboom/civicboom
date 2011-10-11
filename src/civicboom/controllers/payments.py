from civicboom.lib.base import *
from civicboom.model import User, Group, PaymentAccount
from civicboom.model.payment import country_codes

from civicboom.lib.form_validators.validator_factory import build_schema
from civicboom.lib.form_validators.dict_overlay import validate_dict    

from civicboom.controllers.payment_actions import PaymentActionsController

payment_actions_controller = PaymentActionsController()

import formencode
import civicboom.lib.form_validators
import civicboom.lib.form_validators.base
import civicboom.lib.form_validators.registration

import time, re

log      = logging.getLogger(__name__)

country_ec_vat = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EL', 'ES', 'FI', 'FR', 'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK', 'GB']

# Compiled regex for every EC state's vat registration number format
tax_code_regex = re.compile(
    '^('
    '((EE|EL|DE|PT)([0-9]{9}))|' \
    '((FI|HU|LU|MT|SI)([0-9]{8}))|' \
    '((PL|SK)([0-9]{10}))|' \
    '((IT|LV)([0-9]{11}))|' \
    '((SE)([0-9]{12}))|' \
    '((BE)(0?[0-9]{9}))|' \
    '((CY)([0-9]{8}[A-Z]))|' \
    '((CZ)([0-9]{8,10}))|' \
    '((DK)(([0-9]{2}\ ?){3}[0-9]{2}))|' \
    '((ES)(([0-9A-Z][0-9]{7}[A-Z])|([A-Z][0-9]{7}[0-9A-Z])))|' \
    '((FR)([0-9A-Z]{2}\ ?[0-9]{9}))|' \
    '((GB)(([1-9][0-9]{2}\ ?[0-9]{4}\ ?[0-9]{2})|([1-9][0-9]{2}\ ?[0-9]{4}\ ?[0-9]{2}\ ?[0-9]{3})|((GD|HA)[0-9]{3})))|' \
    '((IE)([0-9][0-9A-Z\+\*][0-9]{5}[A-Z]))|' \
    '((LT)(([0-9]{9}|[0-9]{12})))|' \
    '((NL)([0-9]{9}B[0-9]{2}))|' \
    '((AT)(U[0-9]{8}))|' \
    '((BG)([0-9]{9,10}))|' \
    '((RO)([0-9]{2,10}))' \
    ')$'
)

tax_code_validator = formencode.validators.Regex(tax_code_regex, strip=True, not_empty=False)

class PaymentsController(BaseController):
    """
    @title Payments
    @doc payment
    @desc controller for administering payment accounts
    """
    
#    # Only allow these actions if in development mode
#    def __before__(self, action, **params):
#        if not config['development_mode']==True:
#            return abort(404)
#        BaseController.__before__(self)
    
    @web
    @authorize
    @role_required('admin')
    def index(self, **kwargs):
        """
        GET /groups: All groups the current user is a member of
        @api groups 1.0 (WIP)
        @param * (see common list return controls)
        @return 200 - data.list = array of group objects that logged in user is a member including the additional field 'members "role" in the group'
        """
        # url('payments')
        
        
        
        if not c.logged_in_persona.payment_account:
            if c.format == 'html':
                
                return redirect(url('new_payment'))
            raise action_error(_('There is no payment account associated with this user, please create a new payment account'), code=404)
        
        account = c.logged_in_persona.payment_account
        
        return self.show(account.id)
    
    @web
    @authorize
    @role_required('admin')
    def new(self, **kwargs):
        """
        """
        account = c.logged_in_persona.payment_account
        if account:
            return redirect(url('payment', action='show', id=account.id))
        #url_for('new_payment')
        return action_ok()

    @web
    @auth
    @role_required('admin')
    def create(self, **kwargs):
        """
        """
        
        payment_account = PaymentAccount()
        payment_account.members.append(c.logged_in_persona)
        
        c.template_error = "payments/new"
        self.update(payment_account, **kwargs)
        
        payment_account.frequency = 'month'
        
        Session.commit()
        plans = ['free', 'plus', 'corp']
        plan = [key[5:] for key in kwargs.keys() if key[0:5] == 'plan_' and key[5:] in plans]
        if plan:
            plan = plan[0]
        else:
            plan = 'free'
        # Only regrade if plan != free (regrade errors on same plan)
        if plan != 'free':
            payment_actions_controller.regrade(id=payment_account.id, new_type=plan)
            
        if c.format in ('html', 'redirect'):
            return redirect(url('payment', action='show', id=payment_account.id))
        return action_ok('Account created')

    @web
    @authorize
    @role_required('admin')
    def edit(self, id, **kwargs):
        """
        """
        account = c.logged_in_persona.payment_account
        if not account:
            raise action_error(_('Payment account does not exist'), code=404)
        if c.logged_in_persona not in account.members:
            raise action_error(_('You do not have permission to view this account'), code=404)
        
        account_dict = account.to_dict('full')
        
        data = {'id':account.id}
        data.update(dict([(key, account.config[key]) for key in account.config if key in account._user_edit_config]))
        
        data = {'payment':data}
        
        return action_ok(data=data)

    @web
    @auth
    @role_required('admin')
    def update(self, id, **kwargs):
        """
        """
        if isinstance(id, PaymentAccount):
            account = id
        else:
            account = Session.query(PaymentAccount).filter(PaymentAccount.id==id).first()
        if not account:
            raise action_error(_('Payment account does not exist'), code=404)
        if c.logged_in_persona not in account.members:
            raise action_error(_('You do not have permission to view this account'), code=404)
        
        address_fields = PaymentAccount._address_config_order
        # Build validation schema
        schema = build_schema(
            name_type       = formencode.validators.OneOf(['org','ind'], messages={'missing': 'Please select a type'}, not_empty=True),
            org_name        = formencode.validators.UnicodeString(),
            ind_name        = formencode.validators.UnicodeString(),
        )
        if kwargs.get('name_type') == 'org':
            schema.fields['org_name']  = formencode.validators.UnicodeString(not_empty=True)
        else:
            schema.fields['ind_name']  = formencode.validators.UnicodeString(not_empty=True)
            
        for address_field in address_fields:
            schema.fields[address_field] = formencode.validators.UnicodeString(not_empty=(address_field in PaymentAccount._address_required))
            
        schema.fields['address_country'] = formencode.validators.OneOf(country_codes.keys(), messages={'missing': 'Please select a country'}, not_empty=True)
#        if kwargs.get('address_country') in country_ec_vat:
#            if kwargs.get('vat_no'):
#                kwargs['vat_no'] = kwargs.get('address_country','') + kwargs['vat_no']
#            schema.fields['vat_no'] = tax_code_validator
#        else:
#            schema.fields['vat_no'] = formencode.validators.Empty()
        data = {'payment':kwargs}
        data = validate_dict(data, schema, dict_to_validate_key='payment', template_error=c.template_error if hasattr(c, 'template_error') else 'payments/edit')
        form = data['payment']
             
#        if form.get('vat_no'):
#            form['vat_no'] = form['vat_no'][2:]
        
        for field in account._user_edit_config:
            if form.get(field):
                account.config[field] = form[field]
            elif account.config.get(field):
                del account.config[field]
                
        if account.config.get('address_country') in country_ec_vat:
            if account.config['address_country'] == 'GB':
                account.taxable = True
            elif account.config.get('vat_no'):
                account.taxable = False
            else:
                account.taxable = True
        else:
            account.taxable = False
        
#        if form.get('ind_name'):
#            account.config['ind_name'] = form['ind_name']
#        elif account.config.get('ind_name'):
#            del account.config['ind_name']
#        if form.get('org_name'):
#            account.config['org_name'] = form['org_name']
#        elif account.config.get('org_name'):
#            del account.config['org_name']
#        
#        for field_name in address_fields:
#            if form.get(field_name):
#                account.config[field_name] = form[field_name]
        
        # account.frequency = 'month' This can be changed in the future
        
        #return redirect(url('payment', action='show', id=payment_account.id))
        
        Session.commit()
        
        # url('payment', id=ID)
        if c.format == 'redirect':
            redirect(url('payment', id=account.id))
        
        return action_ok()
    
    @web
    @auth
    @role_required('admin')
    def delete(self, id, **kwargs):
        """
        """
        # url('payment', id=ID)
        return action_ok()
    
    @web
    @authorize
    @role_required('admin')
    def show(self, id, **kwargs):
        """
        """
        if isinstance(id, PaymentAccount):
            account = id
        else:
            account = Session.query(PaymentAccount).get(id)
        
        if not account:
            raise action_error(_('Payment account does not exist'), code=404)
        if not c.logged_in_persona in account.members:
            raise action_error(_('You do not have permission to view this account'), code=404)
        
        data = account.to_dict('full')
        return action_ok(code=200, data=data)
