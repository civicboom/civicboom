 # vim: set fileencoding=utf8:

"""Setup the civicboom application"""
import logging

from civicboom.config.environment import load_environment
from civicboom.model import meta

from civicboom.model.meta import Base, Session, LegacySession
from civicboom.model import License, Tag, Rating
from civicboom.model import User, Group
from civicboom.model import ArticleContent, CommentContent, DraftContent, AssignmentContent, Media
from civicboom.model import MemberAssignment, Follow
from civicboom.model import Message
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

    unspecified = License(u"Unspecified", u"Unspecified", u"", u"")
    cc_by       = License(u"CC-BY",       u"Creative Commons Attribution", u"", u"http://www.creativecommons.org")
    cc_by_nc    = License(u"CC-BY-NC",    u"Creative Commons Attribution Non-Commercial", u"", u"http://www.creativecommons.org")
    cc_by_nc_nd = License(u"CC-BY-NC-ND", u"Creative Commons Attribution Non-Commercial No-Derivs", u"", u"http://www.creativecommons.org")
    cc_by_nc_sa = License(u"CC-BY-NC-SA", u"Creative Commons Attribution Non-Commercial Share-Alike", u"", u"http://www.creativecommons.org")
    cc_by_nd    = License(u"CC-BY-ND",    u"Creative Commons Attribution No-Derivs", u"", u"http://www.creativecommons.org")
    cc_by_sa    = License(u"CC-BY-SA",    u"Creative Commons Attribution Share-Alike", u"", u"http://www.creativecommons.org")
    cc_pd       = License(u"CC-PD",       u"Creative Commons Public Domain", u"", u"http://www.creativecommons.org")
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

    ###################################################################
    if False:
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
        g.content.append(asc)
        Session.add_all([asc, ])
        Session.commit()

    ###################################################################
    else:
        log.info("Converting from legacy database")
        import re
        leg_sess = LegacySession()
        leg_conn = leg_sess.connection()

        licenses_by_old_id = [
            None, # l_id is 1-based, there is no zero
            unspecified,
            cc_by,
            cc_by_nd,
            cc_by_nc_nd,
            cc_by_nc,
            cc_by_nc_sa,
            cc_by_sa,
        ]

        log.info("|- Converting reporters to users")
        reporters_by_old_id = {}
        for row in leg_conn.execute("SELECT * FROM reporters"):
            u = User()
            u.username      = row["ReporterName"]
            u.name          = (" ".join([n for n in [row["FirstName"], row["LastName"]] if n])).strip().decode("utf-8")
            if u.name == "":
                u.name = u.username.decode("ascii")
            u.email         = row["Email"]
            u.join_date     = row["Join_Date"]
            u.home_location = row["CityId"]
            u.description   = u"Automatically imported user"
            u.status        = "active"
            u.last_check    = row["notification_check"]
#  `Password` varchar(40) default NULL,
#  `Birth` date default NULL,
#  `Gender` enum('M','F','U') NOT NULL default 'U',
#  `CityId` int(10) unsigned default NULL,
#  `CountyId` int(10) unsigned default NULL,
#  `StateId` int(10) unsigned default NULL,
#  `CountryId` int(10) unsigned default NULL,
#  `ZipId` int(10) unsigned default NULL,
#  `Address` varchar(255) default NULL,
#  `Address2` varchar(255) default NULL,
#  `Photo` varchar(100) default NULL,
#  `TimeStamp` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
#  `contact_status` tinyint(1) NOT NULL default '1',
#  `Specialisation` varchar(255) default NULL,
#  `Dream_Assignment` varchar(255) default NULL,
#  `Status` enum('display','pending','suspend','deleted','failed') NOT NULL default 'pending',
#  `affiliationId` int(10) NOT NULL default '2',
#  `homepage` varchar(200) default NULL,
#  `instant_news` varchar(200) character set utf8 collate utf8_unicode_ci default NULL,
#  `instant_news_update_time` datetime default NULL,
#  `twitter_username` varchar(100) default NULL,
#  `twitter_password` varchar(100) default NULL,
#  `twitter_instantnews` tinyint(1) default NULL,
#  `twitter_reports` tinyint(1) default NULL,
#  `ArticleViewsCount` int(100) NOT NULL default '0',
#  `NumFollowers` int(10) NOT NULL default '0',
#  `interview_me` tinyint(1) NOT NULL default '0',
#  `specialist_topic1` varchar(200) character set utf8 collate utf8_unicode_ci default NULL,
#  `specialist_topic2` varchar(200) character set utf8 collate utf8_unicode_ci default NULL,
#  `specialist_topic3` varchar(200) character set utf8 collate utf8_unicode_ci default NULL,
#  `specialist_topic4` varchar(200) character set utf8 collate utf8_unicode_ci default NULL,
#  `specialist_topic5` varchar(200) character set utf8 collate utf8_unicode_ci default NULL,
#  `link1_text` varchar(200) character set utf8 collate utf8_unicode_ci default NULL,
#  `link1_url` varchar(200) character set utf8 collate utf8_unicode_ci default NULL,
#  `link2_text` varchar(200) character set utf8 collate utf8_unicode_ci default NULL,
#  `link2_url` varchar(200) character set utf8 collate utf8_unicode_ci default NULL,
#  `link3_text` varchar(200) character set utf8 collate utf8_unicode_ci default NULL,
#  `link3_url` varchar(200) character set utf8 collate utf8_unicode_ci default NULL,
#  `specialist_catId` int(10) unsigned default NULL,

            log.debug("   |- %s (%s)" % (u.name, u.username))
            Session.add(u)
            reporters_by_old_id[row["id"]] = u
        Session.commit()


        # FIXME: put this in helpers, and make it work
        def get_tag(name):
            return uncategorised

        def get_tags(row):
            """
            Several tables share very similar structure, but the
            field names are subtly different. Cry.
            """
            string_tags = ""
            if "tag" in row:
                string_tags = string_tags + row["tag"] + " "
            if "Tags" in row:
                string_tags = string_tags + row["Tags"] + " "
            tags = [get_tag(n) for n in re.split("[, ]", string_tags)]

            if "catId" in row:
                a.tags.append(get_tag_by_old_category_id(row["catId"]))
            if "CatId" in row:
                a.tags.append(get_tag_by_old_category_id(row["catId"]))
            return list(set(tags))

        def get_content(row):
            """
            Rather than freeform HTML, or a separate "links" table,
            several tables have columns for links. Not all tables
            have the same number of links though. Cry.
            """
            content = row["content"]
            if row["link1_text"]:
                content = content + "<p>Links:"
                content = content + ("<br><a href='%s'>%s</a>" % (row["link1_url"], row["link1_text"]))
            if row["link2_text"]:
                content = content + ("<br><a href='%s'>%s</a>" % (row["link2_url"], row["link2_text"]))
            if row["link3_text"]:
                content = content + ("<br><a href='%s'>%s</a>" % (row["link3_url"], row["link3_text"]))
            if "link4_text" in row and row["link4_text"]:
                content = content + ("<br><a href='%s'>%s</a>" % (row["link4_url"], row["link4_text"]))
            if "link5_text" in row and row["link5_text"]:
                content = content + ("<br><a href='%s'>%s</a>" % (row["link5_url"], row["link5_text"]))
            return content

        def get_tag_by_old_category_id(c_id):
            row = list(leg_conn.execute("SELECT * FROM categories WHERE id=%s", c_id))[0]
            return get_tag(row["Name"])

        # FIXME: make this work
        def get_location(row):
#  `CityId` int(10) unsigned default NULL,
#  `CountyId` int(10) unsigned default NULL,
#  `StateId` int(10) unsigned default NULL,
#  `CountryId` int(10) unsigned default NULL,
#  `ZipId` int(10) unsigned default NULL,

#  `CountryId` int(10) unsigned default NULL,
#  `StateId` int(10) unsigned default NULL,
#  `CountyId` int(10) unsigned default NULL,
#  `CityId` int(10) unsigned default NULL,
#  `ZipId` int(10) unsigned default NULL,
            return None

        log.info("|- Converting assignments to content")
        assignments_by_old_id = {}
        for row in leg_conn.execute("SELECT * FROM assignments"):
            a               = AssignmentContent()
            a.title         = row["title"].decode("utf-8")
            a.tags          = get_tags(row)
            a.content       = get_content(row).decode("utf-8")
            a.boom_count    = row["boom_count"]
            a.creator       = reporters_by_old_id[row["creatorReporterId"]]
            a.license_id    = licenses_by_old_id[row["CreaviveCommonsLicenceTypeId"]].id
#  `fileExtension` varchar(50) default NULL,
#  `image` tinyint(1) NOT NULL default '0',
#  `movie` tinyint(1) NOT NULL default '0',
#  `imageCredit` varchar(100) default NULL,
            a.attachments   = []
            a.assigned_to   = []
            a.creation_date = row["creationDate"]
            a.due_date      = row["expiryDate"]
            a.location      = get_location(row)
#  `cancelled` tinyint(1) NOT NULL default '0',

            log.debug("   |- %s" % (a.title, ))
            Session.add(a)
            assignments_by_old_id[row["id"]] = a
        Session.commit()

        log.info("|- Converting newsarticles to content")
        newsarticles_by_old_id = {}
        for row in leg_conn.execute("SELECT * FROM newsarticles"):
            a               = ArticleContent()
            a.title         = row["Title"].strip().decode("utf-8") # mobile bug added newlines to everything
            a.content       = get_content(row).decode("utf-8")
            a.creator       = reporters_by_old_id[row["ReporterId"]]
            a.location      = get_location(row)
            a.creation_date = row["creation_time"]
            a.update_date   = row["TimeStamp"]
            a.license_id    = licenses_by_old_id[row["CreaviveCommonsLicenceTypeId"]].id
            a.boom_count    = row["boom_count"]
#  `TypeId` int(10) unsigned NOT NULL default '1',
#  `AssignmentId` int(10) unsigned default NULL,
#  `ParentArticleId` int(10) unsigned default NULL,
#  `interviewId` int(10) unsigned default NULL,
#  `Counter` int(10) NOT NULL default '0',
#  `Photo` tinyint(1) NOT NULL default '0',
#  `rating` int(10) NOT NULL default '0',
#  `total_rate` int(10) NOT NULL default '0',
#  `Status` enum('display','pending','suspend','deleted','failed','syndicate','syndicated') default 'display',
#  `IP` varchar(20) NOT NULL,
#  `upload_format` varchar(20) NOT NULL,
#  `raw_file` varchar(255) default NULL,
#  `extraimages` tinyint(1) NOT NULL default '0',
#  `image_no2` tinyint(1) NOT NULL default '0',
#  `image_no3` tinyint(1) NOT NULL default '0',
#  `image_no4` tinyint(1) NOT NULL default '0',
#  `image_no5` tinyint(1) NOT NULL default '0',
#  `locked` tinyint(1) NOT NULL default '0' COMMENT 'no further editing allowed',
#  `imageCredit` varchar(100) default NULL,
#  `geolocation_latitude` double default NULL,
#  `geolocation_longitude` double default NULL,

            log.debug("   |- %3d - %s" % (row["id"], a.title, ))
            Session.add(a)
            newsarticles_by_old_id[row["id"]] = a
        Session.commit()

        log.info("|- Converting comments to content")
        for row in leg_conn.execute("SELECT * FROM comments"):
            c               = CommentContent()
            c.parent        = newsarticles_by_old_id[row["ArticleId"]]
            c.title         = u"Re: " + c.parent.title
            c.content       = row["contents"].decode("utf-8")
            c.creator       = reporters_by_old_id[row["ReporterId"]]
            c.creation_date = row["creation_time"]
            c.license_id    = unspecified.id
            # `status` enum('display','pending','deleted') NOT NULL default 'display',
            log.debug("   |- %3d - %s" % (row["id"], c.title, ))
            Session.add(c)
        Session.commit()

        log.info("|- Converting ratings to rating")
        for row in leg_conn.execute("SELECT * FROM ratings"):
            r = Rating()
            r.content    = newsarticles_by_old_id[row["NewsArticleId"]]
            r.member     = reporters_by_old_id[row["RatedByReporterId"]]
            r.rating     = row["Rating"]
            # `update_time` datetime default NULL,
            # `CatId` int(3) unsigned NOT NULL,
            log.debug("   |- %s - %s - %d" % (r.member.username, r.content.title, r.rating))
            Session.add(r)
        Session.commit()

        log.info("|- Converting assignments_accepted to map_member_to_assignment")
        for row in leg_conn.execute("SELECT * FROM assignments_accepted"):
            m = MemberAssignment()
            m.content    = assignments_by_old_id[row["assignmentId"]]
            m.member     = reporters_by_old_id[row["reporterId"]]
            m.withdrawn  = (row["withdrawn"] == 1)
            # `timestamp_` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
            log.debug("   |- %s - %s" % (m.member.username, m.content.title))
            Session.add(m)
        Session.commit()

        log.info("|- Converting fan_relationships to map_follow")
        for row in leg_conn.execute("SELECT * FROM fan_relationships"):
            member     = reporters_by_old_id[row["followed_reporterId"]]
            follower   = reporters_by_old_id[row["following_reporterId"]]
            member.followers.append(follower)
            log.debug("   |- %s - %s" % (member.username, follower.username))
        Session.commit()

        log.info("|- Converting messages to message")
        for row in leg_conn.execute("SELECT * FROM messages"):
            m = Message()
            if row["sourceId"]:
                m.source     = reporters_by_old_id[row["sourceId"]]
            if row["destinationId"]:
                m.target     = reporters_by_old_id[row["destinationId"]]
            m.text       = row["messageText"].decode("utf8")
            m.timestamp  = row["timestamp"]
            log.debug("   |- %s -> %s" % (m.source, m.target))
            Session.add(m)
        Session.commit()

    ###################################################################
    log.info("Successfully set up tables")

    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)
