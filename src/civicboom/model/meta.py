"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.interfaces import AttributeExtension
import copy

__all__ = ['Session', 'engine', 'metadata', 'Base']

# SQLAlchemy database engine. Updated by model.init_model()
engine = None

# SQLAlchemy session manager. Updated by model.init_model()
Session = scoped_session(sessionmaker())

# Global metadata. If you have multiple databases with overlapping table
# names, you'll need a metadata for each database
metadata = MetaData()

# Shish - 0.9.7 had this included, 1.0 doesn't?
# Allan - dont think it is needed in this project? - http://www.sqlalchemy.org/docs/reference/ext/declarative.html#accessing-the-metadata
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
            
#===============================================================================
# Events for:
#    PaymentAccount.type change -> update PaymentAccount.members.account_type
#    PaymentAccount.members change -> update PaymentAccount.members/memb_appended/memb_removed
#    Member.payment_account_id set None -> update Memb.account_type to 'free'
#===============================================================================
class PaymentAccountTypeChangeListener(AttributeExtension):
    def set(self, state, value, oldvalue, initiator):
        for member in state.obj().members:
            member.account_type = value
        return value
class PaymentAccountMembersChangeListener(AttributeExtension):
    def set(self, state, value, oldvalue, initiator):
        for member in state.obj().members:
            member.account_type = value
        return value
    def append(self, state, value, initiator):
        value.account_type = state.obj().type
        return value
    def remove(self, state, value, initiator):
        value.account_type = 'free'
class MemberPaymentAccountIdChangeListener(AttributeExtension):
    def set(self, state, value, oldvalue, initiator):
        if value == None:
            state.obj().account_type = 'free'
        return value

# types

from sqlalchemy import PickleType, UnicodeText
import json

from cbutils.cbtv import log as t_log


class JSONType(PickleType):
    """
    fff. json dumps to str by default, and unicodetext complains
    """
    impl = UnicodeText

    def __init__(self, mutable=False):
        PickleType.__init__(self, pickler=json, mutable=mutable)


#-------------------------------------------------------------------------------
# Object to Dict Conversion
#-------------------------------------------------------------------------------
#
# Enchancements to Base object

def location_to_string(location):
    if location:
        return '%s %s' % (location.coords(Session)[0], location.coords(Session)[1])
    return None


@t_log("to_dict")
def to_dict(self, list_type='default', include_fields=None, **kwargs):
    """
    describe
    """
    from cbutils.misc import obj_to_dict
    
    if list_type == 'empty': # Don't copy a base list if empty list is requested
        fields = {}
    else:
        if list_type not in self.__to_dict__:
            from civicboom.lib.web import action_error
            raise action_error(message="unsupported list type", code=400)
        fields = copy.deepcopy(self.__to_dict__[list_type])
    
    # Include fields from ['full+actions'] is specifyed in include_fields (can be list of strings or single string separated by ',' )
    master_list_name = 'full' # Constant - should be defined elsewhere?
    if isinstance(include_fields, basestring):
        include_fields = include_fields.split(',')
    if isinstance(include_fields, list):
        for field in [field for field in include_fields if field in self.__to_dict__[master_list_name]]:
            fields[field] = self.__to_dict__[master_list_name][field]

    return obj_to_dict(self, fields)

#def to_dict_update(self, name, field_list, clone_name=None):
#    __to_dict__ =  self.__to_dict__
#    if clone_name:
#        __to_dict__[name] = __to_dict__[clone_name].copy()
#    if name not in __to_dict__:
#        __to_dict__[name] = {}
#    __to_dict__[name].update(field_list)
    
Base.__to_dict__    =  {}
Base.to_dict        = to_dict
#Base.to_dict_update = to_dict_update
