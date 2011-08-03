
from civicboom.model.meta import Base, location_to_string, JSONType, Session
from civicboom.model.member import account_types as _payment_account_types

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText
from sqlalchemy import Enum, Integer, Numeric, DateTime, Date, Boolean
from sqlalchemy import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import DDL, CheckConstraint

import UserDict
import copy
from ConfigParser import SafeConfigParser, NoOptionError

from decimal import *


currency_symbols = {
    'GBP':  u"&pound;",
    'USD':  u"$",
    'EUR':  u"&euro;",
}

frequency_multipliers = {
    'month': 1,
    'year' : 12,
}

tax_rates = {
    'GB':    0.2,
    'EU':    0.2,
    'US':    0.2,
}


class _ConfigManager(UserDict.DictMixin):
    def __init__(self, base):
        self.base = base

    def __getitem__(self, name):
        if name in self.base:
            return self.base[name]
        raise KeyError(name)

    def __setitem__(self, name, value):
        self.base[name] = value

    def __delitem__(self, name):
        if name in self.base:
            del self.base[name]

    def keys(self):
        return self.base.keys()
    
class ServicePrice(Base):
    __tablename__      = "payment_service_price"
    service_id         = Column(Integer(),     ForeignKey('payment_service.id'), nullable=False, primary_key=True)
    _frequency         = Enum("once", "month", "year", name="billing_period")
    frequency          = Column(_frequency,    nullable=False, default="month" , primary_key=True)
    currency           = Column(Unicode(),     nullable=False, primary_key=True)
    amount             = Column(Numeric(precision=10, scale=2),     nullable=False)
    
    def __init__(self, service=None, frequency=None, currency=None, amount=None):
        if service:
            self.service = service
        if frequency:
            self.frequency = frequency
        if currency:
            self.currency = currency
        if amount != None:
            self.amount = amount
    
class Service(Base):
    __tablename__      = "payment_service"
    id                 = Column(Integer(),     primary_key=True)
    title              = Column(Unicode(),     nullable=False)
    extra_fields       = Column(JSONType(mutable=True), nullable=False, default={})
    payment_account_type = Column(_payment_account_types, nullable=True, unique=True)
    
    prices = relationship("ServicePrice", backref=backref('service') )
    
    _config = None
    
    def __init__(self, id=None, title=None, extra_fields={}, payment_account_type=None):
        self.id = id
        self.title = title
                
        self.extra_fields = extra_fields
        self.payment_account_type = payment_account_type
    
    @property
    def config(self):
        if not self.extra_fields:
            self.extra_fields = {}
        if not self._config:
            self._config = _ConfigManager(self.extra_fields)
        return self._config
    
    def get_price(self, currency, frequency):
        price = Session.query(ServicePrice).filter(ServicePrice.service_id == self.id).filter(ServicePrice.currency == currency).filter(ServicePrice.frequency == frequency).one()
        if price:
            return price.amount
        else:
            return None
    
class PaymentAccountService(Base):
    __tablename__      = "payment_account_service"
    id                 = Column(Integer(), primary_key=True)
    payment_account_id = Column(Integer(), ForeignKey('payment_account.id')      , nullable=False)
    service_id         = Column(Integer(), ForeignKey('payment_service.id')      , nullable=False)
    start_date         = Column(DateTime(), nullable=False, default=func.now())
    _frequency         = Enum("once", "month", "year", name="billing_period")
    frequency          = Column(_frequency,    nullable=False, default="month")
    quantity           = Column(Integer(), nullable=False, default=1)
    discount           = Column(Numeric(precision=10, scale=2),     nullable=False, default=0)
    note               = Column(Unicode(),     nullable=True)
    
    service = relationship("Service")
    
    @property
    def price(self):
        return self.service.get_price(self.payment_account.currency, self.frequency)
    
    def __init__(self, payment_account=None, service=None, note=None, frequency=None, quantity=None, discount=None ):
        if payment_account:
            self.payment_account = payment_account
        if service:
            self.service = service
        
        if note:
            self.note = note
        
        if service and service.payment_account_type:
            self.frequency = payment_account.frequency
        elif frequency:
            self.frequency = frequency
        
        if quantity:
            self.quantity = quantity
        if discount:
            self.discount = discount

class Invoice(Base):
    __tablename__      = "payment_invoice"
    id                 = Column(Integer(),     primary_key=True)
    payment_account_id = Column(Integer(),   ForeignKey('payment_account.id'), nullable=False)
    _invoice_status    = Enum("unbilled", "processing", "billed", "waiting_payment_processing", "disregarded", "paid", name="invoice_status")
    status             = Column(_invoice_status, nullable=False, default="unbilled")
    timestamp          = Column(DateTime(),    nullable=False, default=func.now())
    due_date           = Column(Date(), nullable=False)
    copied_from_id     = Column(Integer(),   ForeignKey('payment_invoice.id'), nullable=True)
    extra_fields       = Column(JSONType(mutable=True), nullable=False, default={})
    currency           = Column(Unicode(), default="GBP", nullable=False)
    taxable            = Column(Boolean(), nullable=False, default=True)
    _tax_rate_code     = Enum("GB", "EU", "US", name="tax_rate_code")
    tax_rate_code      = Column(_tax_rate_code, nullable=True, default="GB")
    tax_rate           = Column(Numeric(precision=10, scale=4),     nullable=False, default=0)
    
    lines = relationship("InvoiceLine", backref=backref('invoice') )
    
    __to_dict__ = copy.deepcopy(Base.__to_dict__)
    __to_dict__.update({
        'default': {
            'id'                : None ,
            'payment_account_id': None ,
            'status'            : None ,
            'timestamp'         : None ,
            'due_date'          : None ,
            'copied_from_id'    : None ,
            'total_pre_tax'     : None ,
            'total_tax'         : None ,
            'total'             : None ,
            'paid_total'        : None ,
            'total_due'         : None ,
            'currency'          : None ,
        },
    })
    
    __to_dict__.update({
        'full': copy.deepcopy(__to_dict__['default'])
    })
    __to_dict__['full'].update({
            'payment_account'     : lambda invoice: invoice.payment_account.to_dict(),
            'lines'               : lambda invoice: [line.to_dict() for line in invoice.lines],
            'transactions'        : lambda invoice: [trans.to_dict() for trans in invoice.transactions],
            'processing'          : None, 
    })
    
    def __init__(self, payment_account=None):
        if payment_account:
            self.payment_account_id = payment_account.id
            self.currency = payment_account.currency
            self.taxable = payment_account.taxable
            self.tax_rate_code = payment_account.tax_rate_code
            if payment_account.taxable:
                self.tax_rate = tax_rates.get(self.tax_rate_code)
    
    _config = None

    @property
    def total_pre_tax(self):
        return sum ([line.price_final for line in self.lines]).quantize(Decimal('1.00'))

    @property
    def total_tax(self):
        return (self.total_pre_tax * self.tax_rate).quantize(Decimal('1.00'))

    @property
    def total(self):
        return self.total_pre_tax + self.total_tax
    
    @property
    def paid_total(self):
        return sum ([trans.amount for trans in self.transactions if trans.status == "complete"])
    
    @property
    def total_due(self):
        return self.total - self.paid_total
    
    @property
    def processing(self):
        return len([txn for txn in self.transactions if txn.status == 'pending']) != 0

    @property
    def config(self):
        if not self.extra_fields:
            self.extra_fields = {}
        if not self._config:
            self._config = _ConfigManager(self.extra_fields)
        return self._config
    
    
# Allow inserts, allow delete when status != unbilled
# Allow update any field when status = unbilled
# Allow update status field from:
#    processing to unbilled, billed or disregarded
#    billed to disregarded or paid
# Disallow update status field from disregarded or paid
DDL('DROP TRIGGER IF EXISTS update_create_payment_invoice ON payment_invoice').execute_at('before-drop', Invoice.__table__)
DDL("""
CREATE OR REPLACE FUNCTION update_create_payment_invoice() RETURNS TRIGGER AS $$
    DECLARE
        
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            RETURN NULL;
        ELSIF (TG_OP = 'UPDATE') THEN
            IF (OLD.status != 'unbilled') THEN
                IF (OLD.payment_account_id != NEW.payment_account_id) THEN
                    RAISE EXCEPTION 'Cant update %%%% invoice', OLD.status;
                    
                ELSIF (OLD.timestamp != NEW.timestamp) THEN
                    RAISE EXCEPTION 'Cant update %%%% invoice', OLD.status;
                    
                ELSIF (OLD.copied_from_id != NEW.copied_from_id) THEN
                    RAISE EXCEPTION 'Cant update %%%% invoice', OLD.status;
                    
                ELSIF (OLD.extra_fields != NEW.extra_fields) THEN
                    RAISE EXCEPTION 'Cant update %%%% invoice', OLD.status;
                    
                ELSIF (OLD.currency != NEW.currency) THEN
                    RAISE EXCEPTION 'Cant update %%%% invoice', OLD.status;
                    
                ELSIF (OLD.taxable != NEW.taxable) THEN
                    RAISE EXCEPTION 'Cant update %%%% invoice', OLD.status;
                    
                ELSIF (OLD.tax_rate_code != NEW.tax_rate_code) THEN
                    RAISE EXCEPTION 'Cant update %%%% invoice', OLD.status;
                    
                ELSIF (OLD.tax_rate != NEW.tax_rate) THEN
                    RAISE EXCEPTION 'Cant update %%%% invoice', OLD.status;
                    
                END IF;
                
                IF (OLD.status = 'processing' AND (NEW.status NOT IN ('unbilled','billed','disregarded'))) THEN
                    RAISE EXCEPTION 'Cant move from %%%% to %%%%', OLD.status, NEW.status;
                    
                ELSIF (OLD.status = 'billed' AND (NEW.status NOT IN ('disregarded','paid','waiting_payment_processing'))) THEN
                    RAISE EXCEPTION 'Cant move from %%%% to %%%%', OLD.status, NEW.status;
                    
                ELSIF (OLD.status = 'disregarded') THEN
                    RAISE EXCEPTION 'Cant move from %%%% to %%%%', OLD.status, NEW.status;
                    
                ELSIF (OLD.status = 'paid') THEN
                    RAISE EXCEPTION 'Cant move from %%%% to %%%%', OLD.status, NEW.status;
                    
                ELSIF (OLD.status = 'waiting_payment_processing' AND (NEW.status NOT IN ('disregarded','paid','billed'))) THEN
                    RAISE EXCEPTION 'Cant move from %%%% to %%%%', OLD.status, NEW.status;
                    
                END IF;
            END IF;
            RETURN NULL;
        ELSIF (TG_OP = 'DELETE') THEN
            IF (OLD.status != 'unbilled') THEN
                RAISE EXCEPTION 'Cant delete %%%% invoice', OLD.status;
            END IF;
            RETURN NULL;
        END IF;
        RAISE EXCEPTION 'Cant run %%%% on this invoice', TG_OP;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_create_payment_invoice
    AFTER INSERT OR UPDATE OR DELETE ON payment_invoice
    FOR EACH ROW EXECUTE PROCEDURE update_create_payment_invoice();
""").execute_at('after-create', Invoice.__table__)
    
class InvoiceLine(Base):
    __tablename__      = "payment_invoice_line"
    id                 = Column(Integer(),     primary_key=True)
    invoice_id         = Column(Integer(),     ForeignKey('payment_invoice.id'), nullable=False)
    service_id         = Column(Integer(),     ForeignKey('payment_service.id'), nullable=False)
    title              = Column(Unicode(),     nullable=False)
    price              = Column(Numeric(precision=10, scale=2),     nullable=False)
    quantity           = Column(Integer(),     nullable=False, default=1)
    discount           = Column(Numeric(precision=10, scale=2),     nullable=False, default=0)
    start_date         = Column(Date(),        nullable=True)
    note               = Column(Unicode(),     nullable=True)
    extra_fields       = Column(JSONType(mutable=True), nullable=False, default={})
    
    service = relationship("Service")
    
    __to_dict__ = copy.deepcopy(Base.__to_dict__)
    __to_dict__.update({
        'default': {
            'id'                : None ,
            'invoice_id'        : None ,
            'service_id'        : None ,
            'title'             : None ,
            'price'             : None ,
            'quantity'          : None ,
            'discount'          : None , 
            'note'              : None ,
            'price_final'       : None ,
        },
    })
    
    def __init__(self, invoice=None, service=None, payment_account_service=None, frequency=None, start_date=None):
        if invoice:
            self.invoice = invoice
        
        if payment_account_service:
            self.service = payment_account_service.service
            frequency = payment_account_service.frequency
            self.note = payment_account_service.note
            self.discount = payment_account_service.discount
            
        if service:
            self.service = service
            self.title = self.service.title
            self.price = self.service.get_price(invoice.currency, frequency)
            self.extra_fields = self.service.extra_fields

        self.start_date = start_date
    
    _config = None
    
    @property
    def price_final(self):
        return (self.price * (Decimal('1.00')-self.discount) * Decimal(self.quantity)).quantize(Decimal('1.00'))
    
    @property
    def config(self):
        if not self.extra_fields:
            self.extra_fields = {}
        if not self._config:
            self._config = _ConfigManager(self.extra_fields)
        return self._config
    
DDL("CREATE INDEX payment_invoice_line_start_year_idx  ON payment_invoice_line USING btree(extract(year  from start_date));").execute_at('after-create', InvoiceLine.__table__)
DDL("CREATE INDEX payment_invoice_line_start_month_idx ON payment_invoice_line USING btree(extract(month from start_date));").execute_at('after-create', InvoiceLine.__table__)
DDL("CREATE INDEX payment_invoice_line_start_day_idx   ON payment_invoice_line USING btree(extract(day   from start_date));").execute_at('after-create', InvoiceLine.__table__)
    
DDL('DROP TRIGGER IF EXISTS update_create_payment_invoice_line ON payment_invoice_line').execute_at('before-drop', InvoiceLine.__table__)
DDL("""
CREATE OR REPLACE FUNCTION update_create_payment_invoice_line() RETURNS TRIGGER AS $$
    DECLARE
        tmp_invoice_id integer;
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            tmp_invoice_id := NEW.invoice_id;
        ELSIF (TG_OP = 'UPDATE') THEN
            tmp_invoice_id := NEW.invoice_id;
        ELSIF (TG_OP = 'DELETE') THEN
            tmp_invoice_id := OLD.invoice_id;
        END IF;
        
        IF (SELECT status != 'unbilled' FROM payment_invoice WHERE id = tmp_invoice_id) THEN
            RAISE EXCEPTION 'Cant add new billing lines to a billed invoice';
        END IF;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_create_payment_invoice_line
    AFTER INSERT OR UPDATE OR DELETE ON payment_invoice_line
    FOR EACH ROW EXECUTE PROCEDURE update_create_payment_invoice_line();
""").execute_at('after-create', InvoiceLine.__table__)

class BillingAccount(Base):
    __tablename__      = "payment_billing_account"
    id                 = Column(Integer(),     primary_key=True)
    _billing_status    = Enum("active", "deactivated", "error", "flagged", name="billing_account_status")
    status             = Column(_billing_status, nullable=False, default="active")
    provider           = Column(Unicode(),     nullable=False)
    reference          = Column(Unicode(),     nullable=False)
    extra_fields       = Column(JSONType(mutable=True), nullable=False, default={})
    payment_account_id = Column(Integer(),   ForeignKey('payment_account.id'), nullable=False)
    
    __to_dict__ = copy.deepcopy(Base.__to_dict__)
    __to_dict__.update({
        'default': {
            'id'                : None ,
            'status'            : None ,
            'provider'          : None ,
            'payment_account_id': None ,
        },
    })
    
    _config = None
    
    @property
    def config(self):
        if not self.extra_fields:
            self.extra_fields = {}
        if not self._config:
            self._config = _ConfigManager(self.extra_fields)
        return self._config

class BillingTransaction(Base):
    __tablename__ = "payment_billing_transaction"
    id                 = Column(Integer(),     primary_key=True)
    invoice_id         = Column(Integer(),     ForeignKey('payment_invoice.id'), nullable=False)
    _transaction_status= Enum("created", "pending", "complete", "failed", "cancelled", "error", "refunded", name="billing_transaction_status")
    status             = Column(_transaction_status, nullable=False, default="created")
    amount             = Column(Numeric(precision=10, scale=2),     nullable=False)
    billing_account_id = Column(Integer(),     ForeignKey('payment_billing_account.id'), nullable=True)
    provider           = Column(Unicode(),     nullable=True)
    reference          = Column(Unicode(),     nullable=True)
    extra_fields       = Column(JSONType(mutable=True), nullable=False, default={})
    
    billing_account    = relationship("BillingAccount", backref=backref('transactions') )
    invoice            = relationship("Invoice", backref=backref('transactions') )
    
    __to_dict__ = copy.deepcopy(Base.__to_dict__)
    __to_dict__.update({
        'default': {
            'id'                : None ,
            'invoice_id'        : None ,
            'status'            : None ,
            'amount'            : None ,
            'billing_account_id': None ,
            'provider'          : None ,
        },
    })
    
    _config = None
    
    @property
    def config(self):
        if not self.extra_fields:
            self.extra_fields = {}
        if not self._config:
            self._config = _ConfigManager(self.extra_fields)
        return self._config
    