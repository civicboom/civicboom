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
#    PaymentAccount.billing_status change -> update PaymentAccount.members.account_type
#    PaymentAccount.members change -> update PaymentAccount.members/memb_appended/memb_removed
#    Member.payment_account_id set None -> update Memb.account_type to 'free'
#===============================================================================

def working_account_type(account_type, billing_status):
    if billing_status == 'failed':
        return 'free'
    return account_type

class PaymentAccountTypeChangeListener(AttributeExtension):
    def set(self, state, value, oldvalue, initiator):
        me = state.obj()
        me_type = working_account_type(value, me.billing_status)
        for member in me.members:
            member.account_type = me_type
        return value
    
class PaymentAccountStatusChangeListener(AttributeExtension):
    def set(self, state, value, oldvalue, initiator):
        me = state.obj()
        me_type = working_account_type(me.type, value)
        for member in me.members:
            member.account_type = me_type
        return value
    
class PaymentAccountMembersChangeListener(AttributeExtension):
    def set(self, state, value, oldvalue, initiator):
        me = state.obj()
        me_type = working_account_type(me.type, me.billing_status)
        for member in me.members:
            member.account_type = me_type
        return value
    
    def append(self, state, value, initiator):
        me = state.obj()
        value.account_type = working_account_type(me.type, me.billing_status)
        return value
    
    def remove(self, state, value, initiator):
        value.account_type = 'free'
        
class MemberPaymentAccountIdChangeListener(AttributeExtension):
    def set(self, state, value, oldvalue, initiator):
        if value == None:
            state.obj().account_type = 'free'
        return value


# AllanC - Testing various SQLAlchemy Events
#          I left it hear because it's a useful tool, getting alerts to every field change

#from civicboom.lib.cache import cache_manager, caching_query
#Session = scoped_session(sessionmaker(  query_cls=caching_query.query_callable(cache_manager) )) # Cache addition
"""
# Cache Additions
#   We need to be able to recive notifications on any data object changes so that we can invalidate the cache
#   Add receive_change_event to base
#
# Reference:
#  - http://www.sqlalchemy.org/trac/browser/examples/custom_attributes/listen_for_events.py?rev=7667%3A6bf675d91a56

from sqlalchemy.orm.interfaces import AttributeExtension,InstrumentationManager

class InstallListeners(InstrumentationManager):
    def post_configure_attribute(self, class_, key, inst):
        # Add an event listener to an InstrumentedAttribute.
        inst.impl.extensions.insert(0, AttributeListener(key))
        
class AttributeListener(AttributeExtension):
    # Generic event listener.  
    # Propigates attribute change events to a "receive_change_event()" method on the target instance.
    
    def __init__(self, key):
        self.key = key
    
    def append(self, state, value, initiator):
        self._report(state, value, None, "appended")
        return value

    def remove(self, state, value, initiator):
        self._report(state, value, None, "removed")

    def set(self, state, value, oldvalue, initiator):
        self._report(state, value, oldvalue, "set")
        return value
    
    def _report(self, state, value, oldvalue, verb):
        state.obj().receive_change_event(verb, self.key, value, oldvalue)


class Base(object):
    __sa_instrumentation_manager__ = InstallListeners
    
    def receive_change_event(self, verb, key, value, oldvalue):
        try:
            s = "Value '%s' %s on attribute '%s', " % (value, verb, key)
            if oldvalue:
                s += "which replaced the value '%s', " % oldvalue
            s += "on object %s" % self
            print s
        except:
            pass
        
Base = declarative_base(cls=Base)
"""


# Listener for Member object events - this triggers invalidate cache
# This is subject to change in sqlalchemy 0.7
# Reference - http://www.sqlalchemy.org/docs/06/orm/interfaces.html#mapper-events
from sqlalchemy.orm.interfaces import MapperExtension
from sqlalchemy.orm.session import object_session
#from sqlalchemy.orm.util import has_identity
class CacheChangeListener(MapperExtension):
    def after_insert(self, mapper, connection, instance):
        self.after_update(mapper, connection, instance)
    def after_update(self, mapper, connection, instance):
        if object_session(instance).is_modified(instance, include_collections=False): # and has_identity(instance)
            instance.invalidate_cache()
            #print "instance %s after_update" % instance
    def before_delete(self, mapper, connection, instance):
        instance.invalidate_cache(remove=True)
        #print "instance %s before_delete" % instance



# types

from sqlalchemy import PickleType, UnicodeText
import simplejson as json

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
def to_dict(self, list_type='default', include_fields=None, exclude_fields=None, **kwargs):
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

    # Delete exlucded fields from return
    if isinstance(exclude_fields, basestring):
        exclude_fields = exclude_fields.split(',')
    if isinstance(exclude_fields, list):
        for field in [field for field in exclude_fields if field in fields]:
            del fields[field]


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
