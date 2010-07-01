 # vim: set fileencoding=utf8:

"""Setup the civicboom application"""
import logging

from civicboom.config.environment import load_environment
from civicboom.model import meta

from civicboom.model.meta import Base, Session
from civicboom.model import License, Tag
from civicboom.model import User, ArticleContent, Media
import datetime

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup civicboom here"""
    load_environment(conf.global_conf, conf.local_conf)

    ###################################################################
    log.info("Creating tables")

    Base.metadata.drop_all(checkfirst=True, bind=Session.bind)
    Base.metadata.create_all(bind=Session.bind)

    ###################################################################
    log.info("Populating tables with base data")

    cc_by       = License(u"CC-BY",       u"Creative Commons Attribution", u"", u"http://www.creativecommons.org")
    cc_by_nc    = License(u"CC-BY-NC",    u"Creative Commons Attribution Non-Commercial", u"", u"http://www.creativecommons.org")
    cc_by_nc_nd = License(u"CC-BY-NC-ND", u"Creative Commons Attribution Non-Commercial No-Derivs", u"", u"http://www.creativecommons.org")
    cc_by_nc_sa = License(u"CC-BY-NC-SA", u"Creative Commons Attribution Non-Commercial Share-Alike", u"", u"http://www.creativecommons.org")
    cc_by_nd    = License(u"CC-BY-ND",    u"Creative Commons Attribution No-Derivs", u"", u"http://www.creativecommons.org")
    cc_by_sa    = License(u"CC-BY-SA",    u"Creative Commons Attribution Share-Alike", u"", u"http://www.creativecommons.org")
    cc_pd       = License(u"CC-PD",       u"Creative Commons Public Domain", u"", u"http://www.creativecommons.org")
    Session.add_all([
        cc_by, cc_by_nc, cc_by_nc_nd, cc_by_nc_sa,
        cc_by_nd, cc_by_sa, cc_pd
        ])
    Session.commit()

    arts          = Tag(u"Arts",          u"Category")
    business      = Tag(u"Business",      u"Category")
    community     = Tag(u"Community",     u"Category")
    education     = Tag(u"Education",     u"Category")
    entertainment = Tag(u"Entertainment", u"Category")
    environment   = Tag(u"Environment",   u"Category")
    health        = Tag(u"Health",        u"Category")
    politics      = Tag(u"Politics",      u"Category")
    sci_tech      = Tag(u"Science and Technology", u"Category")
    society       = Tag(u"Society",       u"Category")
    sports        = Tag(u"Sports",        u"Category")
    travel        = Tag(u"Travel",        u"Category")
    uncategorised = Tag(u"Uncategorised", u"Category")
    Session.add_all([
        arts, business, community, education,
        entertainment, environment, health,
        politics, sci_tech, society, sports,
        travel, uncategorised
        ])
    Session.commit()

    open_source   = Tag(u"Open Source", parent=sci_tech)
    the_moon_sci  = Tag(u"The Moon", parent=sci_tech)
    the_moon_loc  = Tag(u"The Moon", u"Location", parent=travel)
    Session.add_all([
        open_source, the_moon_loc, the_moon_sci
        ])
    Session.commit()

    ###################################################################
    log.info("Populating tables with test data")

    u = User()
    u.username      = u"unittest"
    u.name          = u"Mr U. Test"
    u.join_date     = datetime.datetime.now()
    u.home_location = u"The Moon"
    u.description   = u"A user for automated tests to log in as"
    u.status        = "active"

    c = ArticleContent()
    c.title      = u"A test article"
    c.content    = u"""
    Here is some text.
    ここにいくつかのテキストです。
    وهنا بعض النص.
    这里是一些文字。
    הנה כמה טקסט.
    εδώ είναι ένα κείμενο.
    यहाँ कुछ पाठ है.
    здесь некий текст.
    여기에 일부 텍스트입니다.
    דאָ איז עטלעכע טעקסט.
    """
    c.creator    = u
    c.status     = "show"
    c.license_id = cc_by.id
    # c.tags       = [open_source, the_moon_loc]

    m = Media()
    m.content     = c
    m.name        = u"hello.jpg"
    m.type        = "image"
    m.subtype     = "jpeg"
    m.hash        = "00000000000000000000000000000000"
    m.caption     = u"A photo of people saying hello"
    m.credit      = u"Shish"
    m.ip          = "0.0.0.0"

    Session.add_all([u, c, m])
    Session.commit()

    ###################################################################
    log.info("Successfully set up tables")

    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)
