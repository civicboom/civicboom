#!/usr/bin/python

import optparse

from paste.deploy import appconfig

from civicboom.config.environment import load_environment


from civicboom.model.meta import Session

from civicboom.model import Rating
from civicboom.model import User, UserLogin
from civicboom.model import ArticleContent, CommentContent, AssignmentContent, Media
from civicboom.model import MemberAssignment
from civicboom.model import Message

from civicboom.lib.services import warehouse as wh
from civicboom.lib.database.get_cached import get_tag, get_license
from civicboom.lib.database.gis import get_location_by_name
from civicboom.lib import worker

from glob import glob
import os
import re
import Image
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import logging
logging.basicConfig(
    level   = logging.INFO,
    format  = "%(asctime)s,%(msecs)03d %(levelname)-5.5s [%(name)s] [%(threadName)s] %(message)s",
    datefmt = "%H:%M:%S"
)
log = logging.getLogger(__name__)


def convert_legacy_database(url): # pragma: no cover - this should only be run as a one-off
        worker.start_worker(8)

        LegacySession = scoped_session(sessionmaker())
        LegacySession.configure(bind=create_engine(url))

        log.info("Converting from legacy database")
        leg_sess = LegacySession()
        leg_conn = leg_sess.connection()

        # functions to convert from old data {{{
        licenses_by_old_id = [
            None, # l_id is 1-based, there is no zero
            get_license(u"Unspecified"),
            get_license(u"CC-BY"),
            get_license(u"CC-BY-ND"),
            get_license(u"CC-BY-NC-ND"),
            get_license(u"CC-BY-NC"),
            get_license(u"CC-BY-NC-SA"),
            get_license(u"CC-BY-SA"),
        ]

        def get_description(row):
            d = ""
            if row["homepage"]:
                d = d + "<a href='"+row["homepage"]+"'>My home page</a>"
            if row["Dream_Assignment"]:
                d = d + "<p>Dream Assignment:<br/>"+row["Dream_Assignment"]
            if row["specialist_topic1"] or row["specialist_catId"]:
                if row["interview_me"] == 1:
                    d = d + "<p>Willing to be interviewed about "
                else:
                    d = d + "<p>Specialises in "
                specs = [
                    row["Specialisation"],
                    row["specialist_topic1"],
                    row["specialist_topic2"],
                    row["specialist_topic3"],
                    row["specialist_topic4"],
                    row["specialist_topic5"],
                ]
                if row["specialist_catId"]:
                    t = get_tag_by_old_category_id(row["specialist_catId"])
                    specs.append(t.name)
                specs_without_nulls = [s for s in specs if s]
                d = d + ", ".join(specs_without_nulls)
                if row["link1_text"] or row["link2_text"] or row["link3_text"]:
                    d = d + "<p>"
            if row["link1_text"] or row["link2_text"] or row["link3_text"]:
                d = d + "Links:"
            if row["link1_text"] and row["link1_url"]:
                d = d + "<a href='"+row["link1_url"]+"'>"+row["link1_text"]+"</a>"
            if row["link2_text"] and row["link2_url"]:
                d = d + "<a href='"+row["link2_url"]+"'>"+row["link2_text"]+"</a>"
            if row["link3_text"] and row["link3_url"]:
                d = d + "<a href='"+row["link3_url"]+"'>"+row["link3_text"]+"</a>"
            return d.decode("ascii")

        # FIXME: we probably want to get rid of deleted users...
        def convert_status(old_status):
            m = {
                "display": "active",
                "pending": "pending", #"pending"
                "suspend": "removed", #"" 
                "deleted": "removed", #"removed"
                "failed":  "removed",
            }
            return m[old_status]

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
            tags = [get_tag(n) for n in re.split("[^a-zA-Z0-9\-]", string_tags) if len(n) > 0]

            if "catId" in row:
                a.tags.append(get_tag_by_old_category_id(row["catId"]))
            if "CatId" in row:
                a.tags.append(get_tag_by_old_category_id(row["CatId"]))

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
                content = content + ("<br/><a href='%s'>%s</a>" % (row["link1_url"], row["link1_text"]))
            if row["link2_text"]:
                content = content + ("<br/><a href='%s'>%s</a>" % (row["link2_url"], row["link2_text"]))
            if row["link3_text"]:
                content = content + ("<br/><a href='%s'>%s</a>" % (row["link3_url"], row["link3_text"]))
            if "link4_text" in row and row["link4_text"]:
                content = content + ("<br/><a href='%s'>%s</a>" % (row["link4_url"], row["link4_text"]))
            if "link5_text" in row and row["link5_text"]:
                content = content + ("<br/><a href='%s'>%s</a>" % (row["link5_url"], row["link5_text"]))
            return content

        def get_tag_by_old_category_id(c_id):
            row = list(leg_conn.execute("SELECT * FROM categories WHERE id=%s", c_id))[0]
            return get_tag(row["Name"])

        def get_location(row):
            if "geolocation_latitude" in row and "geolocation_longitude" in row:
                if row["geolocation_latitude"] and row["geolocation_longitude"]:
                    return "SRID=4326;POINT(%f %f)" % (row["geolocation_longitude"], row["geolocation_latitude"])

            if "CityId" in row:
                if row["CityId"]:
                    # see also CountyId, StateId, CountryId, ZipId -- are these needed when we have city?
                    row = list(leg_conn.execute("SELECT latitude,longitude FROM cities WHERE id=%s", row["CityId"]))[0]
                    return "SRID=4326;POINT(%f %f)" % (row["longitude"], row["latitude"])

            if "Address" in row and "Address2" in row:
                addr = ", ".join([a for a in [row["Address"], row["Address2"]] if a])
                lonlat = get_location_by_name(addr)
                if lonlat:
                    return "SRID=4326;POINT(%f %f)" % lonlat

            return None

        def get_media(row, media_type):
            caption = None
            credit = None
            if "imageCredit" in row and row["imageCredit"]:
                credit = row["imageCredit"].decode("ascii")

            attachments = []
            bases  = glob("../tmp/"+media_type+"_files/"+str(row["id"])+".*")
            extras = glob("../tmp/"+media_type+"_files/"+str(row["id"])+"_*.*")
            for fn in bases + extras:
                log.debug("Guessing that "+fn+" is associated with "+media_type+" "+str(row["id"]))
                attachments.append(Media().load_from_file(fn, os.path.basename(fn).decode("ascii"), caption, credit))
            return attachments

        def get_avatar(uid):
            file_hash = None
            files = glob("../tmp/profilepics/"+str(uid)+".*")
            if len(files) == 1:
                fn = files[0]
                file_hash = wh.hash_file(fn)
                wh.copy_to_warehouse(fn, "avatars-original", file_hash)

                processed = tempfile.NamedTemporaryFile(suffix=".jpg")
                im = Image.open(fn)
                if im.mode != "RGB":
                    im = im.convert("RGB")
                im.thumbnail([128, 128], Image.ANTIALIAS) #AllanC - FIXME size from config? default gravatar size
                im.save(processed.name, "JPEG")
                wh.copy_to_warehouse(processed.name, "avatars", file_hash, "avatar.jpg")
                processed.close()

                file_hash = "https://civicboom-static.s3.amazonaws.com/avatars/" + file_hash
            return file_hash
        # }}}

        log.info("|- Converting reporters to users") # {{{
        reporters_by_old_id = {}
        for row in leg_conn.execute("SELECT * FROM reporters"):
            u = User()
            u.username      = row["ReporterName"]
            u.name          = (" ".join([n for n in [row["FirstName"], row["LastName"]] if n])).strip().decode("utf-8")
            if u.name == "":
                u.name = u.username.decode("ascii")
            u.email         = row["Email"]
            u.join_date     = row["Join_Date"]
            u.status        = convert_status(row["Status"])
            u.last_check    = row["notification_check"]
            u.avatar        = get_avatar(row["id"])
            u.location_home = get_location(row)
            u.config["description"] = get_description(row)
            u.config["birthday"]    = str(row["Birth"])
            u.config["gender"]      = row["Gender"]
            if row["twitter_username"]:
                u.config["twitter_username"]        = row["twitter_username"]
            if row["twitter_instantnews"] == 1:
                u.config["broadcast_instant_news"]  = True
            #if row["broadcast_content_posts"] == 1:
            #    u.config["broadcast_content_posts"] = True

            if row["Password"]:
                u_login = UserLogin()
                u_login.user   = u
                u_login.type   = "password"
                u_login.token  = row["Password"]

#  `Photo` varchar(100) default NULL,
#  `contact_status` tinyint(1) NOT NULL default '1',
#  `affiliationId` int(10) NOT NULL default '2',
#  `instant_news` varchar(200) character set utf8 collate utf8_unicode_ci default NULL,
#  `instant_news_update_time` datetime default NULL,
#  `twitter_password` varchar(100) default NULL,

            if u.status:
                log.debug("   |- %s (%s)" % (u.name, u.username))
                Session.add(u)
                Session.add(u_login)
                reporters_by_old_id[row["id"]] = u
            else:
                log.info("   |- Not importing %s account: %s (%s)" % (row["Status"], u.name, u.username))
        Session.commit()
        # }}}
        log.info("|- Converting assignments to content") # {{{
        assignments_by_old_id = {}
        for row in leg_conn.execute("SELECT * FROM assignments"):
            a               = AssignmentContent()
            a.title         = row["title"].decode("utf-8")
            a.tags          = get_tags(row)
            a.content       = get_content(row).decode("utf-8")
            a.boom_count    = row["boom_count"]
            a.creator       = reporters_by_old_id[row["creatorReporterId"]]
            a.license_id    = licenses_by_old_id[row["CreaviveCommonsLicenceTypeId"]].id
            a.attachments   = get_media(row, "assignment")
            a.assigned_to   = []
            a.creation_date = row["creationDate"]
            a.due_date      = row["expiryDate"]
            a.location      = get_location(row)
#  `cancelled` tinyint(1) NOT NULL default '0',

            log.debug("   |- %s" % (a.title, ))
            Session.add(a)
            assignments_by_old_id[row["id"]] = a
        Session.commit()
        # }}}
        log.info("|- Converting newsarticles to content") # {{{
        newsarticles_by_old_id = {}
        for row in leg_conn.execute("SELECT * FROM newsarticles"):
            if row["status"] == "deleted":
                continue
            a               = ArticleContent()
            a.title         = row["Title"].strip().decode("utf-8") # mobile bug added newlines to everything
            a.content       = get_content(row).decode("utf-8")
            a.creator       = reporters_by_old_id[row["ReporterId"]]
            a.location      = get_location(row)
            a.creation_date = row["creation_time"]
            a.update_date   = row["TimeStamp"]
            a.license_id    = licenses_by_old_id[row["CreaviveCommonsLicenceTypeId"]].id
            a.boom_count    = row["boom_count"]
            a.attachments   = get_media(row, "article")
#  `TypeId` int(10) unsigned NOT NULL default '1',
#  `AssignmentId` int(10) unsigned default NULL,
#  `ParentArticleId` int(10) unsigned default NULL,
#  `interviewId` int(10) unsigned default NULL,
#  `Counter` int(10) NOT NULL default '0',
#  `rating` int(10) NOT NULL default '0',
#  `total_rate` int(10) NOT NULL default '0',
#  `Status` enum('display','pending','suspend','deleted','failed','syndicate','syndicated') default 'display',
#  `IP` varchar(20) NOT NULL,
#  `locked` tinyint(1) NOT NULL default '0' COMMENT 'no further editing allowed',
            log.debug("   |- %3d - %s" % (row["id"], a.title, ))
            Session.add(a)
            newsarticles_by_old_id[row["id"]] = a
        Session.commit()
        # }}}
        log.info("|- Converting comments to content") # {{{
        for row in leg_conn.execute("SELECT * FROM comments"):
            if row["ArticleId"] in newsarticles_by_old_id:
                c               = CommentContent()
                c.parent        = newsarticles_by_old_id[row["ArticleId"]]
                c.title         = u"Re: " + c.parent.title
                c.content       = row["contents"].decode("utf-8")
                c.creator       = reporters_by_old_id[row["ReporterId"]]
                c.creation_date = row["creation_time"]
                c.license_id    = get_license(u"Unspecified").id
                # `status` enum('display','pending','deleted') NOT NULL default 'display',
                log.debug("   |- %3d - %s" % (row["id"], c.title, ))
                Session.add(c)
            else:
                log.info("   |- Comment's parent was deleted: %3d" % (row["id"], ))
        Session.commit()
        # }}}
        log.info("|- Converting ratings to rating") # {{{
        for row in leg_conn.execute("SELECT * FROM ratings"):
            if row["NewsArticleId"] in newsarticles_by_old_id:
                r = Rating()
                r.content    = newsarticles_by_old_id[row["NewsArticleId"]]
                r.member     = reporters_by_old_id[row["RatedByReporterId"]]
                r.rating     = row["Rating"]
                # `update_time` datetime default NULL,
                # `CatId` int(3) unsigned NOT NULL,
                log.debug("   |- %s - %s - %d" % (r.member.username, r.content.title, r.rating))
                Session.add(r)
            else:
                log.info("   |- Rating's parent was deleted: %3d" % (row["id"], ))
        Session.commit()
        # }}}
        log.info("|- Converting assignments_accepted to map_member_to_assignment") # {{{
        for row in leg_conn.execute("SELECT * FROM assignments_accepted"):
            m = MemberAssignment()
            m.content    = assignments_by_old_id[row["assignmentId"]]
            m.member     = reporters_by_old_id[row["reporterId"]]
            m.status     = "accepted" if (row["withdrawn"] == 1) else "withdrawn" # FIXME: pending?
            # `timestamp_` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
            log.debug("   |- %s - %s" % (m.member.username, m.content.title))
            Session.add(m)
        Session.commit()
        # }}}
        log.info("|- Converting fan_relationships to map_follow") # {{{
        for row in leg_conn.execute("SELECT * FROM fan_relationships"):
            member     = reporters_by_old_id[row["followed_reporterId"]]
            follower   = reporters_by_old_id[row["following_reporterId"]]
            member.followers.append(follower)
            log.debug("   |- %s - %s" % (member.username, follower.username))
        Session.commit()
        # }}}
        log.info("|- Converting messages to message") # {{{
        for row in leg_conn.execute("SELECT * FROM messages"):
            m = Message()
            if row["sourceId"]:
                m.source     = reporters_by_old_id[row["sourceId"]]
            if row["destinationId"]:
                m.target     = reporters_by_old_id[row["destinationId"]]
            m.subject    = row["messageText"].decode("utf8")
            m.content    = row["messageText"].decode("utf8")
            m.timestamp  = row["timestamp"]
            log.debug("   |- %s -> %s" % (m.source, m.target))
            Session.add(m)
        Session.commit()
        # }}}

        worker.stop_worker()

if __name__ == '__main__':
    option_parser = optparse.OptionParser()
    option_parser.add_option('--ini',
        help='INI file to use for pylons settings',
        type='str', default='development.ini')
    option_parser.add_option('--url',
        help='legacy database URL',
        type='str', default='mysql://indiconews:indiconews@127.0.0.1/indiconews')
    options, args = option_parser.parse_args()

    # Initialize the Pylons app
    conf = appconfig('config:' + options.ini, relative_to='.')
    load_environment(conf.global_conf, conf.local_conf)

    # Now code can be run, the SQLalchemy Session can be used, etc.
    convert_legacy_database(options.url)
