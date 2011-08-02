 # vim: set fileencoding=utf8:

"""Setup the civicboom application"""
from civicboom.config.environment import load_environment

from civicboom.model.meta import Base, Session
from civicboom.model import License, Tag
from civicboom.model.payment import Service, ServicePrice

from decimal import *

import pylons.test

import logging
log = logging.getLogger(__name__)


def setup_app(command, conf, variables):
    """Place any commands to setup civicboom here"""
    if not pylons.test.pylonsapp:  # pragma: no cover -- "if not testing" will not be true for testing...
        load_environment(conf.global_conf, conf.local_conf)

    ###################################################################
    sess = Session()
    conn = sess.connection()

    log.info("Creating tables")   # {{{

    Base.metadata.drop_all(checkfirst=True, bind=Session.bind)
    Base.metadata.create_all(bind=Session.bind)

    # }}}
    log.info("Creating triggers")   # {{{

    conn.execute("""
CREATE OR REPLACE FUNCTION strip_tags(TEXT) RETURNS TEXT AS $$
    SELECT regexp_replace(regexp_replace($1, E'(?x)<[^>]*?(\s alt \s* = \s* ([\\'"]) ([^>]*?) \\2) [^>]*? >', E'\\3'), E'(?x)(< [^>]*? >)', '', 'g')
$$ LANGUAGE SQL;
""")

    conn.execute("""
CREATE OR REPLACE FUNCTION update_boom_count() RETURNS TRIGGER AS $$
    DECLARE
        tmp_content_id integer;
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            tmp_content_id := NEW.content_id;
        ELSIF (TG_OP = 'UPDATE') THEN
            RAISE EXCEPTION 'Can only add or remove booms, not alter';
        ELSIF (TG_OP = 'DELETE') THEN
            tmp_content_id := OLD.content_id;
        END IF;

        UPDATE content_user_visible SET boom_count = (
            SELECT count(*)
            FROM map_booms
            WHERE content_id=tmp_content_id
        ) WHERE id=tmp_content_id;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_boom_count
    AFTER INSERT OR UPDATE OR DELETE ON map_booms
    FOR EACH ROW EXECUTE PROCEDURE update_boom_count();
    """)
    conn.execute("""
CREATE OR REPLACE FUNCTION pnormaldist(qn DOUBLE PRECISION) RETURNS NUMERIC AS $$
    DECLARE
        b NUMERIC[] := '{}';
        w1 NUMERIC;
        w3 NUMERIC;
    BEGIN
        b[0] := 1.570796288;
        b[1] := 0.03706987906;
        b[2] := -0.8364353589e-3;
        b[3] := -0.2250947176e-3;
        b[4] := 0.6841218299e-5;
        b[5] := 0.5824238515e-5;
        b[6] := -0.104527497e-5;
        b[7] := 0.8360937017e-7;
        b[8] := -0.3231081277e-8;
        b[9] := 0.3657763036e-10;
        b[10] := 0.6936233982e-12;

        IF qn < 0.0 OR 1.0 < qn OR qn = 0.5 THEN
            RETURN 0.0;
        END IF;

        w3 := -log(4.0 * qn * (1.0 - qn));
        w1 := b[0];
        FOR i IN 1..10 LOOP
            w1 := w1 + b[i] * power(w3,i);
        END LOOP;

        IF qn > 0.5 THEN
            RETURN sqrt(w1*w3);
        END IF;
        RETURN -sqrt(w1*w3);
    END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ci_lower_bound(positive BIGINT, total BIGINT, power NUMERIC) RETURNS NUMERIC AS $$
    DECLARE
        z NUMERIC;
        phat NUMERIC;
    BEGIN
        IF total = 0 THEN
            RETURN 0.0;
        END IF;

        z = pnormaldist(1-power/2);
        phat = 1.0*positive/total;
        RETURN (phat + z*z/(2*total) - z * sqrt((phat*(1-phat)+z*z/(4*total))/total))/(1+z*z/total);
    END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_rating() RETURNS TRIGGER AS $$
    DECLARE
        tmp_content_id integer;
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            tmp_content_id := NEW.content_id;
        ELSIF (TG_OP = 'UPDATE') THEN
            RAISE EXCEPTION 'Can only add or remove ratings, not alter';
            IF (NEW.member_id != OLD.member_id OR NEW.content_id != OLD.content_id) THEN
                RAISE EXCEPTION 'Can only alter rating numbers, not relations';
            END IF;
            tmp_content_id := NEW.content_id;
        ELSIF (TG_OP = 'DELETE') THEN
            tmp_content_id := OLD.content_id;
        END IF;

        UPDATE content_article SET rating = (
            -- sum(rating)     = total score achieved
            -- count(rating)*5 = total score possible
            -- 0.1 = we want 95%% certainty of what minimum score is deserved
            SELECT ci_lower_bound(sum(rating), count(rating)*5, 0.1)
            FROM map_ratings
            WHERE content_id=tmp_content_id
        ) WHERE id=tmp_content_id;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_rating
    AFTER INSERT OR UPDATE OR DELETE ON map_ratings
    FOR EACH ROW EXECUTE PROCEDURE update_rating();
    """)
    #}}}
    ###################################################################
    log.info("Populating tables with base data")  # {{{

    unspecified = License(u"Unspecified", u"Unspecified", u"", u"")
    cc_by       = License(u"CC-BY",       u"Creative Commons Attribution", u"Alteration allowed with credit to the source", u"http://www.creativecommons.org")
    cc_by_nd    = License(u"CC-BY-ND",    u"Creative Commons Attribution No-Derivs", u"Reprinting allowed with credit to the source", u"http://www.creativecommons.org")
    cc_by_sa    = License(u"CC-BY-SA",    u"Creative Commons Attribution Share-Alike", u"Alteration allowed with credit to the source, and derivatives must also be CC-BY-SA", u"http://www.creativecommons.org")
    cc_by_nc    = License(u"CC-BY-NC",    u"Creative Commons Attribution Non-Commercial", u"Non-commercial derivatives allowed with credit to the source", u"http://www.creativecommons.org")
    cc_by_nc_nd = License(u"CC-BY-NC-ND", u"Creative Commons Attribution Non-Commercial No-Derivs", u"Non-commercial reprinting allowed with credit to the source", u"http://www.creativecommons.org")
    cc_by_nc_sa = License(u"CC-BY-NC-SA", u"Creative Commons Attribution Non-Commercial Share-Alike", u"Non-commercial alteration allowed with credit to the source, and derivatives must also be CC-BY-NC-SA", u"http://www.creativecommons.org")
    cc_pd       = License(u"CC-PD",       u"Creative Commons Public Domain", u"Public domain", u"http://www.creativecommons.org")
    Session.add_all([
        unspecified,
        cc_by, cc_by_nc, cc_by_nc_nd, cc_by_nc_sa,
        cc_by_nd, cc_by_sa, cc_pd
        ])
    Session.commit()

    category      = Tag(u"Category")
    arts          = Tag(u"Arts",          category)
    business      = Tag(u"Business",      category)
    community     = Tag(u"Community",     category)
    education     = Tag(u"Education",     category)
    entertainment = Tag(u"Entertainment", category)
    environment   = Tag(u"Environment",   category)
    health        = Tag(u"Health",        category)
    politics      = Tag(u"Politics",      category)
    sci_tech      = Tag(u"Science and Technology", category)
    society       = Tag(u"Society",       category)
    sports        = Tag(u"Sports",        category)
    travel        = Tag(u"Travel",        category)
    uncategorised = Tag(u"Uncategorised", category)
    Session.add_all([
        arts, business, community, education,
        entertainment, environment, health,
        politics, sci_tech, society, sports,
        travel, uncategorised
        ])
    Session.commit()
    # }}}
    ###################################################################
    ## Setup default payment_services
    log.info("Populating default payment services")
    
    free = Service(payment_account_type="free", title="Free"        )
    plus = Service(payment_account_type="plus", title="Pro Lite"    )
    corp = Service(payment_account_type="corp", title="Pro Premium" )
    
    free_price_GBP_monthly = ServicePrice(free, "month", "GBP", Decimal(  '0')                   )
    plus_price_GBP_monthly = ServicePrice(plus, "month", "GBP", Decimal( '10') / Decimal('1.20') ) 
    corp_price_GBP_monthly = ServicePrice(corp, "month", "GBP", Decimal('200') / Decimal('1.20') )
    
    Session.add_all([
        free, plus, corp,
        free_price_GBP_monthly, plus_price_GBP_monthly, corp_price_GBP_monthly
    ])
    Session.commit()
    
    
    ###################################################################

    if pylons.test.pylonsapp:  # only populate when in test mode?
        from civicboom.tests.init_base_data import init_base_data
        init_base_data()

    log.info("Successfully set up tables")

    log.info("Setup complete")
