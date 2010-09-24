"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

__all__ = ['Session', 'LegacySession', 'engine', 'metadata', 'Base']

# SQLAlchemy database engine. Updated by model.init_model()
engine = None
legacy_engine = None

# SQLAlchemy session manager. Updated by model.init_model()
Session = scoped_session(sessionmaker())
LegacySession = scoped_session(sessionmaker())

# Global metadata. If you have multiple databases with overlapping table
# names, you'll need a metadata for each database
metadata = MetaData()

# Shish - 0.9.7 had this included, 1.0 doesn't?
# Allan - dont think it is needed in this project? - http://www.sqlalchemy.org/docs/reference/ext/declarative.html#accessing-the-metadata
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

def to_dict(self, method=None, default_method='default'):
    """
    describe
    """
    from civicboom.lib.misc import obj_to_dict
    if method not in self.__to_dict__:
        method = default_method
    return obj_to_dict(self,self.__to_dict__[method])

Base.__to_dict__ =  {}
Base.to_dict = to_dict
