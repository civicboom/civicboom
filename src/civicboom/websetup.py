"""Setup the civicboom application"""
import logging

from civicboom.config.environment import load_environment
from civicboom.model import meta

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup civicboom here"""
    load_environment(conf.global_conf, conf.local_conf)

    from civicboom.model.meta import Base, Session
    log.info("Creating tables")
    Base.metadata.drop_all(checkfirst=True, bind=Session.bind)
    Base.metadata.create_all(bind=Session.bind)
    log.info("Successfully setup")

    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)
