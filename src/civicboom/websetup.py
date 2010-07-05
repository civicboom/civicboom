 # vim: set fileencoding=utf8:

"""Setup the civicboom application"""
import logging

from civicboom.config.environment import load_environment
from civicboom.model import meta

from civicboom.model.meta import Base, Session
from civicboom.model import License, Tag
from civicboom.model import User, Group
from civicboom.model import ArticleContent, CommentContent, DraftContent, AssignmentContent, Media
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

    ###################################################################
    log.info("Populating tables with test data")

    open_source   = Tag(u"Open Source", sci_tech)
    the_moon_sci  = Tag(u"The Moon", sci_tech)
    the_moon_loc  = Tag(u"The Moon", travel)
    Session.add_all([
        open_source, the_moon_loc, the_moon_sci
        ])
    Session.commit()

    artist       = Tag(u"Artists", arts)
    mic1         = Tag(u"Michelangelo", artist)
    characters   = Tag(u"Characters", entertainment)
    ninja        = Tag(u"Ninja Turtles", characters)
    mic2         = Tag(u"Michelangelo", ninja)
    Session.add_all([
        mic1, mic2
        ])
    Session.commit()

    u1 = User()
    u1.username      = u"unittest"
    u1.name          = u"Mr U. Test"
    u1.join_date     = datetime.datetime.now()
    u1.home_location = u"The Moon"
    u1.description   = u"A user for automated tests to log in as"
    u1.status        = "active"

    u2 = User()
    u2.username      = u"unitfriend"
    u2.name          = u"Mr U's Friend"
    u2.join_date     = datetime.datetime.now()
    u2.home_location = u"The Moon"
    u2.description   = u"A user for automated tests to log in as"
    u2.status        = "active"

    ca = ArticleContent()
    ca.title      = u"A test article"
    ca.content    = u"""
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
    ca.creator    = u1
    ca.status     = "show"
    ca.license_id = cc_by.id
    ca.tags       = [open_source, the_moon_loc]

    m = Media()
    m.name        = u"hello.jpg"
    m.type        = "image"
    m.subtype     = "jpeg"
    m.hash        = "00000000000000000000000000000000"
    m.caption     = u"A photo of people saying hello"
    m.credit      = u"Shish"
    ca.attachments.append(m)

    cc = CommentContent()
    cc.title      = u"A test response"
    cc.content    = u"Here is a response"
    cc.creator    = u2
    cc.status     = "show"
    cc.license_id = cc_by.id
    ca.responses.append(cc)

    cc2 = CommentContent()
    cc2.title      = u"A test response with media"
    cc2.content    = u"Here is a response with media"
    cc2.creator    = u2
    cc2.status     = "show"
    cc2.license_id = cc_by.id

    m = Media()
    m.name        = u"hello2.jpg"
    m.type        = "video"
    m.subtype     = "3gpp"
    m.hash        = "00000000000000000000000000000000"
    m.caption     = u"A video of people saying hi"
    m.credit      = u"Shish"
    cc2.attachments.append(m)

    ca.responses.append(cc2)

    dc = DraftContent()
    dc.title      = u"Response!"
    dc.content    = u"I am writing a longer response, worthy of being published separately"
    dc.status     = "show"
    dc.license_id = cc_by.id
    u2.content.append(dc)

    Session.add_all([u1, u2])
    Session.commit()


    g = Group()
    g.username      = u"p.a.t.t.y."
    g.name          = u"People Against Test's Torturous Yodelling"
    g.join_date     = datetime.datetime.now()
    g.home_location = u"The Moon"
    g.description   = u"Mr U. Test's awful singing has gone on long enough!"
    g.status        = "active"
    g.members.append(u2)
    Session.add_all([g, ])
    Session.commit()

    asc = AssignmentContent()
    asc.title      = u"Silence Mr U. Test"
    asc.content    = u"Get Mr Test to stop singing, write an article about how you did it"
    asc.status     = "show"
    asc.private    = True
    asc.license_id = cc_by.id
    asc.assigned_to.append(g)
    g.content.append(u2)
    Session.add_all([asc, ])
    Session.commit()

    ###################################################################
    log.info("Successfully set up tables")

    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)
