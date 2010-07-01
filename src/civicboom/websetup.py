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

    cc_by       = License("CC-BY",       "Creative Commons Attribution", "", "http://www.creativecommons.org")
    cc_by_nc    = License("CC-BY-NC",    "Creative Commons Attribution Non-Commercial", "", "http://www.creativecommons.org")
    cc_by_nc_nd = License("CC-BY-NC-ND", "Creative Commons Attribution Non-Commercial No-Derivs", "", "http://www.creativecommons.org")
    cc_by_nc_sa = License("CC-BY-NC-SA", "Creative Commons Attribution Non-Commercial Share-Alike", "", "http://www.creativecommons.org")
    cc_by_nd    = License("CC-BY-ND",    "Creative Commons Attribution No-Derivs", "", "http://www.creativecommons.org")
    cc_by_sa    = License("CC-BY-SA",    "Creative Commons Attribution Share-Alike", "", "http://www.creativecommons.org")
    cc_pd       = License("CC-PD",       "Creative Commons Public Domain", "", "http://www.creativecommons.org")
    Session.add_all([
        cc_by, cc_by_nc, cc_by_nc_nd, cc_by_nc_sa,
        cc_by_nd, cc_by_sa, cc_pd
        ])
    Session.commit()

    arts          = Tag("Arts", "Category")
    business      = Tag("Business", "Category")
    community     = Tag("Community", "Category")
    education     = Tag("Education", "Category")
    entertainment = Tag("Entertainment", "Category")
    environment   = Tag("Environment", "Category")
    health        = Tag("Health", "Category")
    politics      = Tag("Politics", "Category")
    sci_tech      = Tag("Science and Technology", "Category")
    society       = Tag("Society", "Category")
    sports        = Tag("Sports", "Category")
    travel        = Tag("Travel", "Category")
    uncategorised = Tag("Uncategorised", "Category")
    Session.add_all([
        arts, business, community, education,
        entertainment, environment, health,
        politics, sci_tech, society, sports,
        travel, uncategorised
        ])
    Session.commit()

    open_source   = Tag("Open Source", parent=sci_tech)
    the_moon_sci  = Tag("The Moon", parent=sci_tech)
    the_moon_loc  = Tag("The Moon", "Location", parent=travel)
    Session.add_all([
        open_source, the_moon_loc, the_moon_sci
        ])
    Session.commit()

    ###################################################################
    log.info("Populating tables with test data")

    u = User()
    u.username      = "unittest"
    u.name          = "Mr U. Test"
    u.join_date     = datetime.datetime.now()
    u.home_location = "The Moon"
    u.description   = "A user for automated tests to log in as"
    u.status        = "active"

    c = ArticleContent()
    c.title      = "A test article"
    c.content    = """
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
    c.license    = cc_by
    # c.tags       = [open_source, the_moon_loc]

    m = Media()
    m.content     = c
    m.name        = "hello.jpg"
    m.type        = "image"
    m.subtype     = "jpeg"
    m.hash        = "00000000000000000000000000000000"
    m.caption     = "A photo of people saying hello"
    m.credit      = "Shish"
    m.ip          = "0.0.0.0"

    Session.add_all([u, c, m])
    Session.commit()

    ###################################################################
    log.info("Successfully set up tables")

    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)
