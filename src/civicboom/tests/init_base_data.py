# vim: set fileencoding=utf8:

#from civicboom.tests import *
from civicboom.lib.base import *
from civicboom.model import *

from civicboom.lib.database.get_cached import get_tag, get_license

import hashlib
import datetime
import os

import logging
log = logging.getLogger(__name__)


def init_base_data():
    # Notifications disabled because no i18n is setup
    from pylons import config
    config['feature.notifications'] = False

    ###############################################################
    def test_base():
        log.info("Populating tables with test base data")
        log.debug("Users")

        u1 = User()
        u1.id            = u"unittest"
        u1.name          = u"Mr U. Test"
        u1.join_date     = datetime.datetime.now()
        u1.status        = "active"
        u1.email         = u"test+unittest@civicboom.com"
        u1.location_home = "SRID=4326;POINT(1.0652 51.2976)"
        u1.location_current = "SRID=4326;POINT(1.0803 51.2789)"
        u1.description   = u"A user for automated tests to log in as"

        u1_login = UserLogin()
        u1_login.user   = u1
        u1_login.type   = "password"
        u1_login.token  = hashlib.sha1("password").hexdigest()

        u1.set_payment_account('plus', delay_commit=True)

        Session.add_all([u1, u1_login])
        Session.commit()
        #assert u1.id == 1
        assert u1.login_details[0].type == "password"
        assert u1.login_details[0].token == hashlib.sha1("password").hexdigest()
        assert u1.login_details[0].token != hashlib.sha1("asdfasdf").hexdigest()
        
        #u1_service = Session.query(Service).filter(Service.payment_account_type==u1.payment_account.type).one()
        
        u1.payment_account.do_not_bill = True

        u2 = User()
        u2.id            = u"unitfriend"
        u2.name          = u"Mr U's Friend"
        u2.status        = "active"
        u2.email         = u"test+unitfriend@civicboom.com"

        u2_login = UserLogin()
        u2_login.user   = u2
        u2_login.type   = "password"
        u2_login.token  = hashlib.sha1("password").hexdigest()

        u2_account         = PaymentAccount()
        u2_account.type    = 'plus'
        u2_account.start_date = datetime.datetime.now() - datetime.timedelta(days=27)

        u2.set_payment_account(u2_account, delay_commit=True)
        
        u2.payment_account.do_not_bill = True

        g1 = Group()
        g1.id       = "unitgroup"
        g1.name     = "Test User Group"
        g1.status   = "active"
        g1.join(u1)
        g1.join(u2)

        Session.add_all([g1, u1, u1_login, u2, u2_login])
        Session.commit()

        u1.follow(u2)
        u2.follow(u1)

        assert u1.login_details[0].type == "password"
        assert u1.login_details[0].token == hashlib.sha1("password").hexdigest()
        assert u1.login_details[0].token != hashlib.sha1("asdfasdf").hexdigest()

        u3 = User()
        u3.id            = u"kitten"
        u3.name          = u"Amy M. Kitten"
        u3.status        = "active"
        u3.email         = u"test+kitten@civicboom.com"
        u3.avatar        = u"f86c68ccab304eb232102ac27ba5da061559fde5"
        u3.set_payment_account('free', delay_commit=True)

        u3_login = UserLogin()
        u3_login.user   = u3
        u3_login.type   = "password"
        u3_login.token  = hashlib.sha1("password").hexdigest()

        u4 = User()
        u4.id            = u"puppy"
        u4.name          = u"Jamie L. Puppy"
        u4.status        = "active"
        u4.email         = u"test+puppy@civicboom.com"
        u4.avatar        = u"64387ac53e446d1c93d11eec777cc7fbf4413f63"

        u5 = User()
        u5.id            = u"bunny"
        u5.name          = u"David O. Bunny"
        u5.status        = "active"
        u5.email         = u""
        u5.avatar        = u"2ca1c359d090e6a9a68dac6b3cc7a14d195ef4d8"

        g2 = Group()
        g2.id       = "cuteness"
        g2.name     = "Cute Users United"
        g2.status   = "active"
        g2.join(u3)
        g2.join(u4)
        g2.join(u5)

        Session.add_all([g2, u3, u3_login, u4, u5])
        Session.commit()


        ###############################################################
        log.debug("Content")

        # Create first item of content as content_id=1 for automated document examples to use
        a = ArticleContent()
        a.title   = u"API Documentation: Article"
        a.content = u"test content"
        a.creator = u1
        Session.add(a)
        Session.commit()
        assert a.id == 1

        b = CommentContent()
        b.title   = u"Comment Test"
        b.content = u"test comment"
        b.creator = u1
        b.parent  = a
        Session.add(b)
        Session.commit()
        assert b.id == 2

        c = ArticleContent()
        c.title   = u"API Documentation: Response"
        c.content = u"test response"
        c.creator = u1
        c.parent  = a
        Session.add(c)
        Session.commit()
        assert c.id == 3

        ###############################################################
        log.debug("Messages")
        
        m1 = Message()
        m1.target = u1
        m1.source = u2
        m1.subject = 'Base Message'
        m1.content = 'Base message'
        
        m2 = Message()
        m2.target = u1
        m2.subject = 'Base Notification'
        m2.content = 'Base notification'
        
        Session.add_all([m1,m2])
        Session.commit()
        
        assert m1.id == 1
        assert m2.id == 2
        
        ###############################################################
        log.debug("Settings")
        
        # Set settings var's so in development we dont get the popups all the time
        member_config      = [u1, u2]
        member_config_vars = ['help_popup_created_user',
                              'help_popup_created_group',
                              'help_popup_created_assignment',]
        for member_config_var in member_config_vars:
            for member in member_config:
                member.config[member_config_var] = 'init'

        assert list(Session.query(User).filter(User.id=="MrNotExists")) == []


    def demo_base():
        log.info("Populating tables with demo base data")
        log.debug("Users")

        wh_base = "civicboom/public/warehouse"
        for n in ["avatars", "media-thumbnail"]:
            try:
                os.makedirs("%s/%s" % (wh_base, n))
            except OSError as e:
                pass # dir exists

        def _get_avatar(id):
            src = "%s/%s.png" % (wh_base, id)
            if os.path.exists(src):
                d = file(src).read()
                h = hashlib.sha1(d).hexdigest()
                file("%s/avatars/%s" % (wh_base, h), "wb").write(d)
                return h
            return None

        def _user(id, name, desc='', av=None):
            u = User()
            u.id            = id
            u.name          = name
            u.join_date     = datetime.datetime.now()
            u.status        = "active"
            u.email         = u"test+%s@civicboom.com" % id
            u.description   = desc
            u.avatar        = _get_avatar(id)
            u.set_payment_account('plus', delay_commit=True)
            Session.add_all([u])
            Session.commit()
            return u

        def _group(id, name, members, desc=''):
            g = Group()
            g.id     = id
            g.name   = name
            g.status = "active"
            g.description = desc
            g.avatar = _get_avatar(id)
            for member in members:
                g.join(member)
            return g

        def _content(type, title, content, creator, parent=None, media=[]):
            if type == "draft":
                c = DraftContent()
            if type == "article":
                c = ArticleContent()
            if type == "assignment":
                c = AssignmentContent()
            if type == "comment":
                c = CommentContent()
            c.title   = title
            c.content = content
            c.creator = creator
            c.parent  = parent
            from glob import glob
            for fn in media:
                path = glob("civicboom/public/warehouse/%s.*" % fn)
                if path:
                    path = path[0]
                    data = file(path).read()
                    m = Media()
                    m.name = fn
                    m.type = "image"
                    m.subtype = "png"
                    m.hash = hashlib.sha1(data).hexdigest()
                    m.filesize = len(data)
                    file("%s/media-thumbnail/%s" % (wh_base, m.hash), "wb").write(data)
                    c.attachments.append(m)
            Session.add(c)
            Session.commit()
            return c

        def _msg(src, dst, subject, content, read=False):
            m = Message()
            m.source = src
            m.target = dst
            m.subject = subject
            m.content = content
            m.read = read
            Session.add_all([m])
            Session.commit()
            return m

        # user to log in as
        unittest = _user("unittest", "Jonny Test", "Just your average guy, with an interest in journalism")
        unittest.location_home = "SRID=4326;POINT(1.0652 51.2976)"
        unittest.location_current = "SRID=4326;POINT(1.0803 51.2789)"
        unittest.set_payment_account('plus', delay_commit=True)

        unittest_login = UserLogin()
        unittest_login.user   = unittest
        unittest_login.type   = "password"
        unittest_login.token  = hashlib.sha1("password").hexdigest()

        Session.add_all([unittest, unittest_login])
        Session.commit()

        # A world to interact with. Stuff taken from Deus Ex: Human Revolution :P
        archie = _user("archie", "Archie Reynmann", "Some guy, nothing special")
        morgan = _user("morgan", "Morgan Everett", "Owner of the world's biggest media group")
        bob_page = _user("bob-page", "Bob Page", "Some guy, nothing special")
        walton = _user("walton", "Walton Simons", "Some guy, nothing special")

        picus_group = _group("picus-group", "Picus Communications", [morgan], "One Globe. One source for news")
        mj12 = _group("mj12", "Majestic 12", [morgan, bob_page, walton])  # FIXME: this group wants privacy
        mj12.location_home = "SRID=4326;POINT(-115.746267 37.646401)"

        eliza = _user("eliza", "Eliza Cassan", "Lead anchor for the world's most popular news network")

        picus_tv = _group("picus-tv", "Picus TV", [picus_group, eliza], "One Globe. One source for news")
        picus_daily = _group("picus-daily", "Picus Daily Standard", [picus_group, eliza], "One Globe. One source for news")

        _content("assignment", "Battle of the Bands: Photos wanted" , "[...]", picus_daily)
        _content("assignment", "Travel photo of the day: Send yours for a chance to win an SLR camera" , "[...]", mj12)
        c1 = _content("article", "Bomb Triggered at Sarif Manufacturing Plant", "[...]", picus_daily)
        _content("assignment", "Where in the world is Carmen Sandiego?", "I've been looking for her for ages, no luck :(", unittest, media=["carmen"])
        c11 = _content("article", "Anti-aug terrorist at large", "[...]", picus_daily, parent=c1)
        c2 = _content("article", "Riots break out at Sarif HQ", "[...]", picus_daily)
        _content("assignment", "Egypt: Have you had to cancel your holiday?" , "[...]", walton)
        c21 = _content("assignment", "Wanted: videos from your streets", "We have a camera crew at the center of the riots, but how is the rest of the city holding up?", picus_tv, parent=c2)
        c111 = _content("assignment", "Have you seen Zeke Sanders?", "[...]", picus_tv, parent=c11, media=["m-zeke"])
        _content("assignment", "Have you ever suffered from road rage? Stories wanted", "[...]", bob_page)
        c3 = _content("assignment", "Flooding on East Street", "Reports are coming in that the river is breeching causing fast moving floods around East Street. Are you there? Send us your videos", picus_tv, parent=c2)
        c31 = _content("article", "Video of the floods", "Things are all go round here! Here's an interview with someone at the scene", unittest, media=["flood"])

        d1 = _content("draft", "Report from regional team meeting", "[...]", unittest)
        d2 = _content("draft", "Conference video", "[...]", unittest)
        d3 = _content("draft", "Bankers' bonuses: What I think", "[...]", unittest)
        d4 = _content("draft", "Operation Stack", "[...]", unittest)

        m1 = _msg(eliza, unittest, "Have you got any more photos from the floods?", "We could use some high-quality stills for the print edition")
        m2 = _msg(mj12, unittest, "An offer you won't refuse", "We need someone with skills like yours. Meet us by the old cake factory at midnight.")
        m3 = _msg(morgan, unittest, "Going to the gig tonight?", "Looks like a lot of papers are on the hunt for photos, check it out")

        for n in [eliza, picus_group, picus_tv, picus_daily]:
            n.location_home = "SRID=4326;POINT(-73.549647 45.557904)"
        from random import random
        for n in [c1, c11, c111, c2, c21]:
            n.location_home = "SRID=4326;POINT(%f %f)" % (51+random()-0.5, 0+random()-0.5)


    if config['data_base'] == 'test':  # development, test
        test_base()
    if config['data_base'] == 'demo':  # demo
        demo_base()
    if config['data_base'] == 'none':  # production
        pass
