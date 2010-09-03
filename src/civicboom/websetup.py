 # vim: set fileencoding=utf8:

"""Setup the civicboom application"""
from civicboom.config.environment import load_environment
from civicboom.model import meta

from civicboom.model.meta import Base, Session, LegacySession
from civicboom.model import License, Tag, Rating
from civicboom.model import User, Group, UserLogin
from civicboom.model import ArticleContent, CommentContent, DraftContent, AssignmentContent, Media
from civicboom.model import MemberAssignment, Follow
from civicboom.model import Message
from civicboom.lib.services import warehouse as wh
from civicboom.lib.database.get_cached import get_tag
from civicboom.lib.gis import get_location_by_name
from civicboom.lib import worker

import logging
import datetime
from glob import glob
import os
import re
import Image
import tempfile
import hashlib

import pylons.test


log = logging.getLogger(__name__)


def setup_app(command, conf, variables):
    """Place any commands to setup civicboom here"""
    if not pylons.test.pylonsapp: # pragma: no cover -- "if not testing" will not be true for testing...
        load_environment(conf.global_conf, conf.local_conf)

    ###################################################################
    log.info("Creating tables") # {{{

    Base.metadata.drop_all(checkfirst=True, bind=Session.bind)
    Base.metadata.create_all(bind=Session.bind)

    # }}}
    log.info("Creating triggers") # {{{
    sess = Session()
    conn = sess.connection()
#model/member.py:    new_messages     = Column(Boolean(),  nullable=False,   default=False) # FIXME: derived

    conn.execute("""
CREATE OR REPLACE FUNCTION update_follower_count() RETURNS TRIGGER AS $$
    DECLARE
        tmp_member_id integer;
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            tmp_member_id := NEW.member_id;
        ELSIF (TG_OP = 'UPDATE') THEN
            RAISE EXCEPTION 'Can''t alter follows, only add or remove';
        ELSIF (TG_OP = 'DELETE') THEN
            tmp_member_id := OLD.member_id;
        END IF;

        UPDATE member SET num_followers = (
            SELECT count(*)
            FROM map_member_to_follower
            WHERE member_id=tmp_member_id
        ) WHERE id=tmp_member_id;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_follower_count
    AFTER INSERT OR UPDATE OR DELETE ON map_member_to_follower
    FOR EACH ROW EXECUTE PROCEDURE update_follower_count();
    """)
    conn.execute("""
CREATE OR REPLACE FUNCTION update_response_count() RETURNS TRIGGER AS $$
    DECLARE
        tmp_parent_id integer;
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            tmp_parent_id := NEW.parent_id;
        ELSIF (TG_OP = 'UPDATE') THEN
            -- use old because sometimes content will be updated to set parent to
            -- null (disassociating), but there is no use case where the parent is
            -- changed from null to a new value (yet...)
            tmp_parent_id := OLD.parent_id;
        ELSIF (TG_OP = 'DELETE') THEN
            tmp_parent_id := OLD.parent_id;
        END IF;

        IF tmp_parent_id IS NOT NULL THEN
            UPDATE content SET num_responses = (
                SELECT count(*)
                FROM content
                WHERE __type__='article' AND parent_id=tmp_parent_id
            ) WHERE id=tmp_parent_id;

            UPDATE content SET num_comments = (
                SELECT count(*)
                FROM content
                WHERE __type__='comment' AND parent_id=tmp_parent_id
            ) WHERE id=tmp_parent_id;
        END IF;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_response_count
    AFTER INSERT OR UPDATE OR DELETE ON content
    FOR EACH ROW EXECUTE PROCEDURE update_response_count();
    """)
    conn.execute("""
CREATE OR REPLACE FUNCTION update_group_size() RETURNS TRIGGER AS $$
    DECLARE
        tmp_group_id integer;
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            tmp_group_id := NEW.group_id;
        ELSIF (TG_OP = 'UPDATE') THEN
            IF (NEW.member_id != OLD.member_id OR NEW.group_id != OLD.group_id) THEN
                RAISE EXCEPTION 'Can only alter membership types, not relations';
            END IF;
            tmp_group_id := NEW.group_id;
        ELSIF (TG_OP = 'DELETE') THEN
            tmp_group_id := OLD.group_id;
        END IF;

        UPDATE member_group SET num_members = (
            SELECT count(*)
            FROM map_user_to_group
            WHERE group_id=tmp_group_id
        ) WHERE id=tmp_group_id;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_group_size
    AFTER INSERT OR UPDATE OR DELETE ON map_user_to_group
    FOR EACH ROW EXECUTE PROCEDURE update_group_size();
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

        IF qn < 0.0 OR 1.0 < qn THEN
            RETURN 0.0;
        END IF;

        IF qn = 0.5 THEN
            RETURN 0.0;
        END IF;

        w1 := qn;
        IF qn > 0.5 THEN
            w1 := 1.0 - w1;
        END IF;
        w3 := -log(4.0 * w1 * (1.0 - w1));
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
    conn.execute("""
CREATE OR REPLACE FUNCTION update_location_time() RETURNS TRIGGER AS $$
    BEGIN
        IF (
                (NEW.location IS NULL     AND OLD.location IS NOT NULL) OR
                (NEW.location IS NOT NULL AND OLD.location IS NULL    ) OR
                (NOT (NEW.location ~= OLD.location))
        ) THEN
            UPDATE member_user SET location_updated = now() WHERE id=NEW.id;
        END IF;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_location_time
    AFTER UPDATE ON member_user
    FOR EACH ROW EXECUTE PROCEDURE update_location_time();
    """)
    conn.execute("""
ALTER TABLE content ADD COLUMN textsearch tsvector;
CREATE INDEX textsearch_idx ON content USING gin(textsearch);

CREATE OR REPLACE FUNCTION update_content() RETURNS TRIGGER AS $$
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            UPDATE content
                SET textsearch = to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content,''))
                WHERE id = NEW.id;
        ELSIF (TG_OP = 'UPDATE') AND (NEW.title != OLD.title OR NEW.content != OLD.content) THEN
            UPDATE content
                SET textsearch = to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content,'')),
                    update_date = now()
                WHERE id = NEW.id;
        END IF;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_content
    AFTER INSERT OR UPDATE ON content
    FOR EACH ROW EXECUTE PROCEDURE update_content();
    """)
    #}}}
    ###################################################################
    log.info("Populating tables with base data") # {{{

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
    # }}}
    ###################################################################
    if meta.legacy_engine: # pragma: no cover -- legacy should be removed
        log.info("Converting from legacy database") # {{{
        leg_sess = LegacySession()
        leg_conn = leg_sess.connection()

        # functions to convert from old data {{{
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
            tags = [get_tag(n) for n in re.split("[, ]", string_tags)]

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
                return "SRID=4326;POINT(%d %d)" % (row["geolocation_longitude"], row["geolocation_latitude"])

            if "CityId" in row:
                row = list(leg_conn.execute("SELECT latitude,longitude FROM cities WHERE id=%s", row["CityId"]))[0]
                return "SRID=4326;POINT(%d %d)" % (row["longitude"], row["latitude"])
                # see also CountyId, StateId, CountryId, ZipId -- are these needed when we have city?

            if "Address" in row and "Address2" in row:
                addr = ", ".join([a for a in [row["Address"], row["Address2"]] if a])
                lonlat = get_location_by_name(addr)
                return "SRID=4326;POINT(%d %d)" % lonlat

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

                file_hash = "http://cb-wh-live.s3.amazonaws.com/avatars/" + file_hash
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
            u.config["location"]    = get_location(row)
            u.config["description"] = get_description(row)
            u.config["birthday"]    = str(row["Birth"])
            u.config["gender"]      = row["Gender"]
            u.config["twitter_username"]        = row["twitter_username"]
            u.config["broadcast_instant_news"]  = (row["twitter_instantnews"] == 1)
            #u.config["broadcast_content_posts"] = (row["broadcast_content_posts"] == 1)

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
                c.license_id    = unspecified.id
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

        # }}}
    ###################################################################
    else:
        log.info("Populating tables with test data") # {{{

        ###############################################################
        log.debug("Tags")

        open_source   = Tag(u"Open Source", sci_tech)
        the_moon_sci  = Tag(u"The Moon", sci_tech)
        the_moon_loc  = Tag(u"The Moon", travel)

        artist       = Tag(u"Artists", arts)
        mic1         = Tag(u"Michelangelo", artist)
        characters   = Tag(u"Characters", entertainment)
        ninja        = Tag(u"Ninja Turtles", characters)
        mic2         = Tag(u"Michelangelo", ninja)

        Session.add_all([open_source, the_moon_loc, the_moon_sci])
        Session.add_all([mic1, mic2])
        Session.commit()

        ###############################################################
        log.debug("Users")

        u1 = User()
        u1.username      = u"unittest"
        u1.name          = u"Mr U. Test"
        u1.join_date     = datetime.datetime.now()
        u1.home_location = u"The Moon"
        u1.description   = u"A user for automated tests to log in as"
        u1.status        = "active"
        u1.email         = u"bob@bobcorp.com"

        u1_login = UserLogin()
        u1_login.user   = u1
        u1_login.type   = "password"
        u1_login.token  = hashlib.sha1("password").hexdigest()

        u2 = User()
        u2.username      = u"unitfriend"
        u2.name          = u"Mr U's Friend"
        u2.status        = "active"
        u2.email         = u"spam@shishnet.org"

        u2_login = UserLogin()
        u2_login.user   = u2
        u2_login.type   = "password"
        u2_login.token  = hashlib.sha1("password").hexdigest()

        u3 = User()
        u3.username      = u"cookie"
        u3.name          = u"Amy M. Anderson"
        u3.status        = "active"
        u3.email         = u"AmyMAnderson@example.com"
        u3.avatar        = u"http://rav.shishnet.org/Sylph.png"

        u4 = User()
        u4.username      = u"jammy"
        u4.name          = u"Jamie L. Riley"
        u4.status        = "active"
        u4.email         = u"waffleking@example.com"
        u4.avatar        = u"http://rav.shishnet.org/Arrnea.png"

        u5 = User()
        u5.username      = u"Davy_H"
        u5.name          = u"David O. Hughes"
        u5.status        = "active"
        u5.email         = u""

        Session.add_all([u1, u2, u3, u4, u5, u1_login, u2_login])
        Session.commit()

        ###############################################################
        log.debug("Messages")

        m = Message()
        m.source = u1
        m.target = u2
        m.subject = u"Re: singing"
        m.content = u"My singing is fine!"

        m = Message()
        m.source = u2
        m.target = u1
        m.subject = u"Re: Re: singing"
        m.content = u"It is totally not! And to explain, I will use a sentence that is over 50 characters long, to test the Message.__unicode__ truncation feature"

        n = Message()
        n.target = u1
        n.subject = u"Notification! A test"
        n.content = u"A test is happening now :O"

        n = Message()
        n.target = u1
        n.subject = u"Another notification! A test"
        n.content = u"A test part 2 is happening now :O"
        Session.commit()

        ###############################################################
        log.debug("Content")

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
        ca.creator    = u2
        ca.status     = "show"
        ca.license_id = cc_by.id
        ca.tags       = [open_source, the_moon_loc]
        ca.location   = "SRID=4326;POINT(-0.1278328 51.5072648)"

        m = Media()
        # FIXME: Image.open() locks up under nosetests, see Bug #45
        #m.load_from_file("civicboom/public/images/star.png", "star.jpg", "A photo of people saying hello", "Shish")
        m.name        = u"hello.jpg"
        m.type        = "image"
        m.subtype     = "jpeg"
        m.hash        = "00000000000000000000000000000000"
        m.caption     = u"A photo of people saying hello"
        m.credit      = u"Shish"
        ca.attachments.append(m)

        cc1 = CommentContent()
        cc1.title      = u"A test response"
        cc1.content    = u"Here is a response"
        cc1.creator    = u3
        cc1.status     = "show"
        cc1.license_id = cc_by.id
        ca.responses.append(cc1)

        cc2 = CommentContent()
        cc2.title      = u"A test response with media"
        cc2.content    = u"Here is a response by the article author"
        cc2.creator    = u2
        cc2.status     = "show"
        cc2.license_id = cc_by.id
        ca.responses.append(cc2)

        cc3 = CommentContent()
        cc3.title      = u"A test response with media"
        cc3.content    = u"Here is a response with media"
        cc3.creator    = u4
        cc3.status     = "show"
        cc3.license_id = cc_by.id
        ca.responses.append(cc3)

        cc4 = CommentContent()
        cc4.title      = u"A test response with media"
        cc4.content    = u"Here is a response by you (if you = unittest)"
        cc4.creator    = u1
        cc4.status     = "show"
        cc4.license_id = cc_by.id
        ca.responses.append(cc4)

        cc5 = CommentContent()
        cc5.title      = u"A test response with media"
        cc5.content    = u"Here is a response by someone else"
        cc5.creator    = u5
        cc5.status     = "show"
        cc5.license_id = cc_by.id
        ca.responses.append(cc5)

        m = Media()
        # FIXME: Image.open() locks up under nosetests, see Bug #45
        #m.load_from_file("civicboom/public/images/rss_large.png", "rss_large.jpg", "An RSS Icon", "Shish")
        m.name        = u"hello2.3gp"
        m.type        = "video"
        m.subtype     = "3gpp"
        m.hash        = "00000000000000000000000000000000"
        m.caption     = u"A video of people saying hi"
        m.credit      = u"Shish"
        cc2.attachments.append(m)

        dc = DraftContent()
        dc.title      = u"Response!"
        dc.content    = u"I am writing a longer response, worthy of being published separately"
        dc.status     = "show"
        dc.license_id = cc_by.id
        u2.content.append(dc)

        Session.add_all([ca])
        Session.commit()

        ###############################################################
        log.debug("Groups")

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

        ###############################################################
        log.debug("Assignments")

        asc = AssignmentContent()
        asc.title      = u"Silence Mr U. Test"
        asc.content    = u"Get Mr Test to stop singing, write an article about how you did it"
        asc.status     = "show"
        asc.private    = True
        asc.license_id = cc_by.id
        #asc.assigned_to.append(g)
        g.content.append(asc)
        Session.add_all([asc, ])
        Session.commit()

        asc.invite([u1,u2,u3,u4])

        asc2 = AssignmentContent()
        asc2.title      = u"Assignment for the world to see"
        asc2.content    = u"There once was a ugly duckling. Damn it was ugly"
        asc2.status     = "show"
        asc2.license_id = cc_by.id
        u1.content.append(asc2)
        Session.add_all([asc2, ])

        # Get test users to accept the assignment
        asc2.accept(u2)
        asc2.accept(u3)
        asc2.accept(u4)
        Session.commit()
        # }}}
    ###################################################################
    log.info("Successfully set up tables")

    worker.stop_worker()

    # FIXME: is this necessary?
    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)
    log.info("Setup complete")
