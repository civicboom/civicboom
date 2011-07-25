
from civicboom.model.meta import Base, location_to_string, JSONType, Session
from civicboom.model.member import account_types as _payment_account_types

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText
from sqlalchemy import Enum, Integer, Float, DateTime, Boolean
from sqlalchemy import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import DDL, CheckConstraint

import UserDict
import copy
from ConfigParser import SafeConfigParser, NoOptionError


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
    _period            = Enum("once", "hour", "day", "week", "month", "year", name="billing_period")
    period             = Column(_period,       nullable=False, default="month" , primary_key=True)
    currency           = Column(Unicode(),     nullable=False, primary_key=True)
    amount             = Column(Float(precision=2),     nullable=False)
    
    def __init__(self, service, period, currency, amount):
        self.service = service
        self.period = period
        self.currency = currency
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
    
    def get_price(self, currency, period):
        price = Session.query(ServicePrice).filter(ServicePrice.service_id == self.id).filter(ServicePrice.currency == currency).filter(ServicePrice.period == period).one()
        if price:
            return price.amount
        else:
            return None
    
class MemberService(Base):
    __tablename__ = "payment_member_service"
    member_id     = Column(Integer(), ForeignKey('member.id')      , primary_key=True)
    service_id    = Column(Integer(), ForeignKey('payment_service.id'), primary_key=True)
    

class Invoice(Base):
    __tablename__      = "payment_invoice"
    id                 = Column(Integer(),     primary_key=True)
    payment_account_id = Column(Integer(),   ForeignKey('payment_account.id'), nullable=False)
    _invoice_status    = Enum("unbilled", "processing", "billed", "disregarded", "paid", name="invoice_status")
    status             = Column(_invoice_status, nullable=False, default="unbilled")
    timestamp          = Column(DateTime(),    nullable=False, default=func.now())
    copied_from_id     = Column(Integer(),   ForeignKey('payment_invoice.id'), nullable=True)
    extra_fields       = Column(JSONType(mutable=True), nullable=False, default={})
    currency           = Column(Unicode(), default="GBP", nullable=False)
    
    lines = relationship("InvoiceLine", backref=backref('invoice') )
    
    __to_dict__ = copy.deepcopy(Base.__to_dict__)
    __to_dict__.update({
        'default': {
            'id'                : None ,
            'payment_account_id': None ,
            'status'            : None ,
            'timestamp'         : None ,
            'copied_from_id'    : None ,
            'total'             : None ,
            'paid_total'        : None, 
        },
    })
    
    __to_dict__.update({
        'full': copy.deepcopy(__to_dict__['default'])
    })
    __to_dict__['full'].update({
            'payment_account'     : lambda invoice: invoice.payment_account.to_dict(),
            'lines'               : lambda invoice: [line.to_dict() for line in invoice.lines],
            'transactions'        : lambda invoice: [trans.to_dict() for trans in invoice.transactions],
    })
    
    _config = None

    @property
    def total(self):
        return sum ([line.price for line in self.lines])
    
    @property
    def paid_total(self):
        return sum([trans.amount for trans in self.transactions if trans.status == "complete"])

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
                END IF;
                
                IF (OLD.status = 'processing' AND (NEW.status NOT IN ('unbilled','billed','disregarded'))) THEN
                    RAISE EXCEPTION 'Cant move from %%%% to %%%%', OLD.status, NEW.status;
                ELSIF (OLD.status = 'billed' AND (NEW.status NOT IN ('disregarded','paid'))) THEN
                    RAISE EXCEPTION 'Cant move from %%%% to %%%%', OLD.status, NEW.status;
                ELSIF (OLD.status = 'disregarded') THEN
                    RAISE EXCEPTION 'Cant move from %%%% to %%%%', OLD.status, NEW.status;
                ELSIF (OLD.status = 'paid') THEN
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
    price              = Column(Float(precision=2),     nullable=False)
    quantity           = Column(Integer(),     nullable=False, default=1)
    discount           = Column(Integer(),     nullable=False, default=0)
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
    _transaction_status= Enum("created", "pending", "complete", "error", "refunded", name="billing_transaction_status")
    status             = Column(_transaction_status, nullable=False, default="created")
    amount             = Column(Float(precision=2),     nullable=False)
    billing_account_id = Column(Integer(),     ForeignKey('payment_billing_account.id'), nullable=False)
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
            'provider'          : lambda trans: trans.billing_account.provider,
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
    