
from civicboom.model.meta import Base, location_to_string, JSONType

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText
from sqlalchemy import Integer, DateTime, Boolean
from sqlalchemy import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import DDL

import UserDict
from ConfigParser import SafeConfigParser, NoOptionError


class _ConfigManager(UserDict.DictMixin):
    def __init__(self, base):
        self.base = base

    def __getitem__(self, name):
        if name in self.base:
            return self.base[name]
        try:
            user_defaults = SafeConfigParser()
            user_defaults.read("invoice_defaults.ini")
            return unicode(user_defaults.get("settings", name))
        except NoOptionError:
            raise KeyError(name)

    def __setitem__(self, name, value):
        self.base[name] = value

    def __delitem__(self, name):
        if name in self.base:
            del self.base[name]

    def keys(self):
        return self.base.keys()


class Invoice(Base):
    __tablename__      = "invoice"
    __table_args__     = (
        CheckConstraint('invoice_status = "unbilled"', name='lockdown_billed'),
    )
    id                 = Column(Integer(),     primary_key=True)
    payment_account_id = Column(Integer(),   ForeignKey('payment_account.id'), nullable=False)
    _invoice_status    = Enum("unbilled", "processing", "billed", "disregarded", "paid", name="invoice_status")
    status             = Column(_invoice_status, nullable=False, default="unbilled")
    timestamp          = Column(DateTime(),    nullable=False, default=func.now())
    copied_from_id     = Column(Integer(),   ForeignKey('invoice.id'), nullable=True)
    extra_fields       = Column(JSONType(mutable=True), nullable=False, default={})
    
    _config = None

    @property
    def config(self):
        if not self.extra_fields:
            self.extra_fields = {}
        if not self._config:
            self._config = _ConfigManager(self.extra_fields)
        return self._config
    
class InvoiceLine(Base):
    __tablename__      = "invoice_line"
    __table_args__     = (
        CheckContraint('invoice.invoice_status = "unbilled" on ', name='lockdown_billed'))