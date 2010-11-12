# vim: set fileencoding=utf8:

#from civicboom.tests import *
from civicboom.lib.base import *
from civicboom.model import *

from civicboom.lib.database.get_cached import get_tag, get_license

import hashlib
import datetime

import logging
log = logging.getLogger(__name__)


def init_base_data():
        log.info("Populating tables with base test data")

        # Notifications disabled because no it8n is setup
        from pylons import config
        config['feature.notifications'] = False


        ###############################################################
        log.debug("Tags")

        open_source   = Tag(u"Open Source", get_tag("science and technology"))
        the_moon_sci  = Tag(u"The Moon"   , get_tag("science and technology"))
        the_moon_loc  = Tag(u"The Moon"   , get_tag("travel"))

        artist       = Tag(u"Artists", get_tag("arts"))
        mic1         = Tag(u"Michelangelo", artist)
        characters   = Tag(u"Characters", get_tag("entertainment"))
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
        u1.status        = "active"
        u1.email         = u"bob@bobcorp.com"
        u1.config['home_location'] = u"The Moon"
        u1.config['description']   = u"A user for automated tests to log in as"

        u1_login = UserLogin()
        u1_login.user   = u1
        u1_login.type   = "password"
        u1_login.token  = hashlib.sha1("password").hexdigest()

        Session.add_all([u1, u1_login]); Session.commit();
        assert u1.id == 1
        assert u1.login_details[0].type == "password"
        assert u1.login_details[0].token == hashlib.sha1("password").hexdigest()
        assert u1.login_details[0].token != hashlib.sha1("asdfasdf").hexdigest()


        u2 = User()
        u2.username      = u"unitfriend"
        u2.name          = u"Mr U's Friend"
        u2.status        = "active"
        u2.email         = u"spam@shishnet.org"

        u2_login = UserLogin()
        u2_login.user   = u2
        u2_login.type   = "password"
        u2_login.token  = hashlib.sha1("password").hexdigest()

        Session.add_all([u2, u2_login]); Session.commit();
        assert u2.id == 2


        u3 = User()
        u3.username      = u"kitten"
        u3.name          = u"Amy M. Kitten"
        u3.status        = "active"
        u3.email         = u"AmyMAnderson@example.com"
        u3.avatar        = u"http://static.civicboom.com/public/images/test/avatar_kitten.jpg"

        u4 = User()
        u4.username      = u"puppy"
        u4.name          = u"Jamie L. Puppy"
        u4.status        = "active"
        u4.email         = u"waffleking@example.com"
        u4.avatar        = u"http://static.civicboom.com/public/images/test/avatar_puppy.jpg"

        u5 = User()
        u5.username      = u"bunny"
        u5.name          = u"David O. Bunny"
        u5.status        = "active"
        u5.email         = u""
        u5.avatar        = u"http://static.civicboom.com/public/images/test/avatar_bunny.jpg"

        Session.add_all([u3, u4, u5]); Session.commit()


        # test data for kent messenger demo
        u6 = User()
        u6.username      = u"kentmessenger"
        u6.name          = u"Kent Messenger"
        u6.status        = "active"
        u6.email         = u"admin@civicboom.com"
        u6.avatar        = u"http://static.civicboom.com/public/images/test/avatar_km.png"

        u6_login = UserLogin()
        u6_login.user   = u6
        u6_login.type   = "password"
        u6_login.token  = hashlib.sha1("password").hexdigest()

        u7 = User()
        u7.username      = u"mobiletest"
        u7.name          = u"Mr. Mobile User"
        u7.status        = "active"
        u7.email         = u"admin@civicboom.com"
        u7.avatar        = u"http://static.civicboom.com/public/images/test/avatar_mobiletest.jpg"

        u7_login = UserLogin()
        u7_login.user   = u7
        u7_login.type   = "password"
        u7_login.token  = hashlib.sha1("password").hexdigest()

        Session.add_all([u6, u6_login, u7, u7_login]);
        u6.followers.append(u7)
        u6.followers.append(u3)
        u6.followers.append(u4)
        u6.followers.append(u5)
        Session.commit();


        assert list(Session.query(User).filter(User.id==0)) == []
        assert list(Session.query(User).filter(User.username=="MrNotExists")) == []

        ###############################################################
        
        u1.follow(u2)
        u2.follow(u1)

        ###############################################################
        log.debug("Content")

        ca = ArticleContent()
        ca.title      = u"A test article by the test user"
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
        #ca.status     = "show"
        ca.license    = get_license("CC-BY")
        ca.tags       = [open_source, the_moon_loc]
        ca.location   = "SRID=4326;POINT(1.0707 51.2999)"

        m = Media()
        # FIXME: Image.open() locks up under nosetests, see Bug #45
        #m.load_from_file("civicboom/public/images/star.png", "star.jpg", "A photo of people saying hello", "Shish")
        m.name        = u"hello.jpg"
        m.type        = "video"
        m.subtype     = "x-ms-asf"
        m.hash        = "89e69557a19a5b168cafc8a56493a08022a49cdd"
        m.caption     = u"A photo of people saying hello"
        m.credit      = u"Shish"
        ca.attachments.append(m)

        Session.add(ca); Session.commit();
        assert ca.id == 1
        assert ca.__type__ == "article"
        assert ca.creator.username == "unittest"


        ca2 = ArticleContent()
        ca2.title      = u"A test article by someone else"
        ca2.content    = u"Content #2 should be owned by unitfriend for testing purposes"
        ca2.creator    = u2
        #ca2.status     = "show"
        ca2.license    = get_license("CC-BY")
        ca2.location   = "SRID=4326;POINT(1.0672 51.2961)"
        ca2.tags       = [open_source, the_moon_loc]

        Session.add(ca2); Session.commit();
        assert ca2.id == 2
        assert ca2.__type__ == "article"
        assert ca2.creator.username == "unitfriend"


        c = DraftContent()
        c.title      = u"A test draft by the test user"
        c.content    = u"Content #3 should be owned by unittest for testing purposes"
        c.creator    = u1
        #c.status     = "show"
        c.license    = get_license("CC_BY")
        c.tags       = [open_source, the_moon_loc]

        Session.add(c); Session.commit();
        assert c.id == 3
        assert c.__type__ == "draft"
        assert c.creator.username == "unittest"


        c = DraftContent()
        c.title      = u"A test draft by someone else"
        c.content    = u"Content #4 should be owned by unitfriend for testing purposes"
        c.creator    = u2
        #c.status     = "show"
        c.license    = get_license("CC-BY")
        c.tags       = [open_source, the_moon_loc]

        Session.add(c); Session.commit();
        assert c.id == 4
        assert c.__type__ == "draft"
        assert c.creator.username == "unitfriend"


        c = CommentContent()
        c.title      = u"A test response"
        c.content    = u"Here is a response by the test user"
        c.creator    = u1
        #c.status     = "show"
        #c.license    = get_license("CC_BY")
        ca2.responses.append(c)

        Session.add(c); Session.commit();
        assert c.id == 5
        assert c.__type__ == "comment"
        assert c.creator.username == "unittest"
        assert c.parent.creator.username == "unitfriend"


        c = CommentContent()
        c.title      = u"A test response"
        c.content    = u"Here is a response by the article writer"
        c.creator    = u2
        #c.status     = "show"
        #c.license    = get_license("CC_BY")
        ca2.responses.append(c)

        Session.add(c); Session.commit();
        assert c.id == 6
        assert c.__type__ == "comment"
        assert c.creator.username == "unitfriend"
        assert c.parent.creator.username == "unitfriend"


        c = CommentContent()
        c.title      = u"A test response"
        c.content    = u"Here is a response by someone who is neither the current user nor the article author"
        c.creator    = u3
        #c.status     = "show"
        #c.license    = get_license("CC_BY")
        ca2.responses.append(c)

        Session.add(c); Session.commit();
        assert c.id == 7
        assert c.__type__ == "comment"
        assert c.parent.creator.username == "unitfriend"


        c = ArticleContent()
        c.title      = u"deleteme"
        c.content    = u"this is here to test that the logged in user can delete their own articles with DELETE"
        c.creator    = u1
        #c.status     = "show"
        c.location   = "SRID=4326;POINT(1.0713 51.2974)"
        c.license    = get_license("CC-BY")

        Session.add(c); Session.commit();
        assert c.id == 8
        assert c.__type__ == "article"
        assert c.creator.username == "unittest"


        c = ArticleContent()
        c.title      = u"deleteme"
        c.content    = u"this is here to test that the logged in user can delete their own articles with _method=DELETE"
        c.creator    = u1
        #c.status     = "show"
        #c.license    = get_license("CC_BY")
        c.location   = "SRID=4326;POINT(1.0862 51.2776)"

        Session.add(c); Session.commit();
        assert c.id == 9
        assert c.__type__ == "article"
        assert c.creator.username == "unittest"


        cc2 = CommentContent()
        cc2.title      = u"A comment"
        cc2.content    = u"Here is a response by the article author"
        cc2.creator    = u1
        #cc2.status     = "show"
        #cc2.license    = get_license("CC_BY")
        ca.responses.append(cc2)

        cc3 = CommentContent()
        cc3.title      = u"A test response with media"
        cc3.content    = u"Here is a response with media"
        cc3.creator    = u4
        #cc3.status     = "show"
        #cc3.license    = get_license("CC_BY")
        ca.responses.append(cc3)

        cc4 = CommentContent()
        cc4.title      = u"A test response with media"
        cc4.content    = u"Here is a response by you (if you = unittest)"
        cc4.creator    = u1
        #cc4.status     = "show"
        #cc4.license_id = cc_by.id
        ca.responses.append(cc4)

        cc5 = CommentContent()
        cc5.title      = u"A test response with media"
        cc5.content    = u"Here is a response by someone else"
        cc5.creator    = u5
        #cc5.status     = "show"
        #cc5.license_id = cc_by.id
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

        dc1 = DraftContent()
        dc1.title      = u"Delete me with DELETE"
        dc1.content    = u"I am writing a longer response, worthy of being published separately"
        #dc1.status     = "show"
        dc1.license    = get_license("CC-BY")
        u1.content.append(dc1)

        dc2 = DraftContent()
        dc2.title      = u"Delete me with fakeout"
        dc2.content    = u"I am writing a longer response, worthy of being published separately"
        #dc2.status     = "show"
        dc2.license    = get_license("CC-BY")
        u1.content.append(dc2)

        res1 = ArticleContent()
        res1.title      = u"A response article"
        res1.content    = u"oh me oh my"
        res1.creator    = u2
        #res1.status     = "show"
        res1.license    = get_license("CC-BY-NC")
        res1.parent     = ca
        res1.location   = "SRID=4326;POINT(1.0794 51.2794)"


        Session.add_all([ca, ca2, dc1, dc2, res1])
        Session.commit()

        ###############################################################
        log.debug("Groups")

        g = Group()
        g.username      = u"patty"
        g.name          = u"People Against Test's Torturous Yodelling"
        g.join_date     = datetime.datetime.now()
        g.home_location = u"The Moon"
        g.description   = u"Mr U. Test's awful singing has gone on long enough!"
        g.status        = "active"
        gm = GroupMembership()
        gm.member = u2
        gm.role   = "admin"
        g.members_roles.append(gm)
        Session.add_all([g, ])
        
        Session.commit()
        
        g.join(u1)
        g.invite(u3)
        g.set_role(u1,"editor")
        g.join(u4)
        g.remove_member(u4)
        


        ###############################################################
        log.debug("Assignments")

        asc = AssignmentContent()
        asc.title      = u"Silence Mr U. Test"
        asc.content    = u"Get Mr Test to stop singing, write an article about how you did it"
        #asc.status     = "show"
        asc.private    = True
        asc.license    = get_license("CC-BY")
        #asc.assigned_to.append(g)
        g.content.append(asc)
        Session.add_all([asc, ])
        Session.commit()

        asc.invite([u1,u2,u3,])

        asc2 = AssignmentContent()
        asc2.title      = u"Assignment for the world to see"
        asc2.content    = u"There once was a ugly duckling. Damn it was ugly"
        #asc2.status     = "show"
        asc2.license    = get_license("CC-BY-NC")
        u1.content.append(asc2)
        Session.add_all([asc2, ])
        
        # Get test users to accept the assignment
        asc2.accept(u3)
        asc2.accept(u4)
        Session.commit()
