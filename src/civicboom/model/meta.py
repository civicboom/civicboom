"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
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



#-------------------------------------------------------------------------------
# Object to Dict Conversion
#-------------------------------------------------------------------------------
#
# Enchancements to Base object

def to_dict(self, list_type='default', include_fields=None, exclude_fields=None, **kwargs):
    """
    describe
    """
    from civicboom.lib.misc import obj_to_dict
    
    if list_type=='empty': # Don't copy a base list if empty list is requested
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

    # Exclude fields
    if isinstance(exclude_fields, basestring):
        exclude_fields = [field.strip() for field in exclude_fields.split(',')]
    if isinstance(exclude_fields, list):
        for field in [field for field in exclude_fields if field in fields]:
            del fields[field]

    return obj_to_dict(self,fields)

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

