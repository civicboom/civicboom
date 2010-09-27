
from pylons import config
from pylons import request, response, session, tmpl_context as c, url

from sqlalchemy import engine_from_config
from sqlalchemy.sql import text

import logging

gis_engine = None

# NOTE: use of the google geocoding and other APIs require that the results
# are displayed using google maps, using google maps on a for-profit website
# requires a commercial license
we_have_a_gmaps_license = False

def get_engine():
    global gis_engine
    if not gis_engine:
        gis_engine = engine_from_config(config, 'sqlalchemy.gis.')
    return gis_engine

def get_location_by_name(name):
    if we_have_a_gmaps_license:
        import urllib2, json
        log.debug("Looking up location for %s" % addr)
        data = urllib2.urlopen("http://maps.google.com/maps/api/geocode/json?sensor=false&address=%s" % addr).read()
        j = json.loads(data)
        if j["status"] == "OK":
            loc = j["results"][0]["geometry"]["location"]
            return (loc["lng"], loc["lat"])
        elif j["status"] == "ZERO_RESULTS":
            return None
        else:
            log.error("Error geocoding %s: %s" % (addr, j["status"]))
            return None

    return None
