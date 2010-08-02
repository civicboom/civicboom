
from pylons import config
from pylons import request, response, session, tmpl_context as c, url

from sqlalchemy import engine_from_config
from sqlalchemy.sql import text

import logging

gis_engine = None

def get_engine():
    global gis_engine
    if not gis_engine:
        gis_engine = engine_from_config(config, 'sqlalchemy.gis.')
    return gis_engine

