"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

__all__ = ['Session', 'LogSession', 'LegacySession', 'engine', 'metadata', 'Base']

# SQLAlchemy database engine. Updated by model.init_model()
engine = None
log_engine = None
legacy_engine = None

# SQLAlchemy session manager. Updated by model.init_model()
Session = scoped_session(sessionmaker())
LogSession = scoped_session(sessionmaker())
LegacySession = scoped_session(sessionmaker())

# Global metadata. If you have multiple databases with overlapping table
# names, you'll need a metadata for each database
metadata = MetaData()

# Shish - 0.9.7 had this included, 1.0 doesn't?
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
