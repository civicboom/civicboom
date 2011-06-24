
from pylons import config

from sqlalchemy import engine_from_config

import logging
log = logging.getLogger(__name__)

gis_engine = None


def get_engine():
    global gis_engine
    if not gis_engine:
        gis_engine = engine_from_config(config, 'sqlalchemy.gis.')
    return gis_engine


def get_location_by_name(name):  # pragma: no cover
    # NOTE: use of the google geocoding and other APIs require that the results
    # are displayed using google maps, using google maps on a for-profit website
    # requires a commercial license
    if False:  # we don't have a license for this
        import urllib2
        import json
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


def find_locations(q, limit=100):
    query = """
        SELECT
            t.name as name,
            ST_AsText(t.way) AS location,
            t.place as type,
            (
                SELECT c.name AS county
                FROM osm_point c
                WHERE c.place='county'
                -- ORDER BY t.way <-> c.way   -- Postgres 9.1 uses knngist to make this one faster?
                                              -- possibly postgis 2.0 would do this internally anyway?
                ORDER BY ST_Distance(t.way, c.way) -- docs for 9.0 explicitly say "doesn't use indexes"
                LIMIT 1
            ) AS county
        FROM
            osm_point t
        WHERE
            t.name ILIKE %s
            AND t.place is not null
        LIMIT %s
    """
    return get_engine().execute(query, [q+"%", limit]).fetchall()
