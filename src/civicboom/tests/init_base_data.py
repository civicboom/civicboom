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

        # AllanC - the follow action requires members/index controller call - this isnt active for the base setup
        #          Here is an alternate way of adding followers without needing the site active
        #def follow(follower,followed):
        #        follow = Follow()
        #        follow.member_id   = followed.id
        #        follow.follower_id = follower.id
        #        assert follow.member_id
        #        assert follow.follower_id
        #        Session.add(follow)


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
        u1.email         = u"test+unittest@civicboom.com"
        u1.location_home = "SRID=4326;POINT(1.0652 51.2976)"
        u1.location_current = "SRID=4326;POINT(1.0803 51.2789)"
        u1.config['home_location'] = u"The Moon"
        u1.description   = u"A user for automated tests to log in as"

        u1_login = UserLogin()
        u1_login.user   = u1
        u1_login.type   = "password"
        u1_login.token  = hashlib.sha1("password").hexdigest()

        #u1_account         = PaymentAccount()
        #u1_account.type    = 'plus'
        #u1.payment_account = u1_account
        u1.set_payment_account('plus', delay_commit=True)

        Session.add_all([u1, u1_login])
        Session.commit()
        assert u1.id == 1
        assert u1.login_details[0].type == "password"
        assert u1.login_details[0].token == hashlib.sha1("password").hexdigest()
        assert u1.login_details[0].token != hashlib.sha1("asdfasdf").hexdigest()


        u2 = User()
        u2.username      = u"unitfriend"
        u2.name          = u"Mr U's Friend"
        u2.status        = "active"
        u2.email         = u"test+unitfriend@civicboom.com"

        u2_login = UserLogin()
        u2_login.user   = u2
        u2_login.type   = "password"
        u2_login.token  = hashlib.sha1("password").hexdigest()

        u2_account         = PaymentAccount()
        u2_account.type    = 'plus'
        u2_account.start_date = datetime.datetime.now() - datetime.timedelta(days=32)

        u2.set_payment_account(u2_account, delay_commit=True)

        Session.add_all([u2, u2_login])
        Session.commit()
        assert u2.id == 2
        
        u2_service = Session.query(Service).filter(Service.payment_account_type==u2_account.type).one()
        
        u2_billing = BillingAccount()
        u2_billing.provider = "manual"
        u2_billing.reference= "BACS"
        u2_billing.payment_account = u2.payment_account
        
        Session.commit()
        
        u2_invoice1 = Invoice(u2_account)
        u2_invoice1.due_date = u2_account.start_date
        u2_invoice1.timestamp = u2_account.start_date + datetime.timedelta(minutes=1)
        u2_invoice1line = InvoiceLine(u2_invoice1, u2_service, 'month', u2_account.start_date)
        
        Session.add_all([u2_invoice1, u2_invoice1line])
        
        Session.commit()
        u2_invoice1.status = "billed"
        Session.commit()
        
        u2_trans = BillingTransaction()
        u2_trans.amount =u2_invoice1.total
        u2_trans.billing_account = u2_billing
        u2_trans.invoice = u2_invoice1
        u2_trans.status = "complete"
        
        Session.add(u2_trans)
        u2_invoice1.status = "paid"
        Session.commit()
        
        
        

        #follow(u1,u2)
        #follow(u2,u1)
        u1.follow(u2)
        u2.follow(u1)
        
        

        u3 = User()
        u3.username      = u"kitten"
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
        u4.username      = u"puppy"
        u4.name          = u"Jamie L. Puppy"
        u4.status        = "active"
        u4.email         = u"test+puppy@civicboom.com"
        u4.avatar        = u"64387ac53e446d1c93d11eec777cc7fbf4413f63"

        u5 = User()
        u5.username      = u"bunny"
        u5.name          = u"David O. Bunny"
        u5.status        = "active"
        u5.email         = u""
        u5.avatar        = u"2ca1c359d090e6a9a68dac6b3cc7a14d195ef4d8"

        Session.add_all([u3, u3_login, u4, u5])
        Session.commit()


        # test data for kent messenger demo
        u6 = User()
        u6.username      = u"kentmessenger"
        u6.name          = u"Kent Messenger"
        u6.status        = "active"
        u6.email         = u"test+kentmessenger@civicboom.com"
        u6.avatar        = u"c6de15ac51375c845b275229b9666afff96bebe8"

        u6_login = UserLogin()
        u6_login.user   = u6
        u6_login.type   = "password"
        u6_login.token  = hashlib.sha1("password").hexdigest()

        u7 = User()
        u7.username      = u"mobiletest"
        u7.name          = u"Mr. Mobile User"
        u7.status        = "active"
        u7.email         = u"test+mobiletest@civicboom.com"
        u7.avatar        = u"585c9c9f719fe5e09fe656e7b8212f8ac32e17ba"

        u7_login = UserLogin()
        u7_login.user   = u7
        u7_login.type   = "password"
        u7_login.token  = hashlib.sha1("password").hexdigest()

        Session.add_all([u6, u6_login, u7, u7_login])
        u6.follow(u7, delay_commit=True)
        u6.follow(u3, delay_commit=True)
        u6.follow(u4, delay_commit=True)
        u6.follow(u5, delay_commit=True)
        Session.commit()

        #follow(u6,u7)
        #follow(u6,u3)
        #follow(u6,u4)
        #follow(u6,u5)


        # test data for commercial first demo
        u8 = User()
        u8.username      = u"cfirst"
        u8.name          = u"Commercial First"
        u8.status        = "active"
        u8.email         = u"test+cfirst@civicboom.com"
        u8.avatar        = u"a1763e442301d1434304fa10b0af986445d697c9"

        u8_login = UserLogin()
        u8_login.user   = u8
        u8_login.type   = "password"
        u8_login.token  = hashlib.sha1("password").hexdigest()

        Session.add_all([u8, u8_login])

        u8.follow(u7, delay_commit=True)
        u8.follow(u3, delay_commit=True)
        u8.follow(u4, delay_commit=True)
        u8.follow(u5, delay_commit=True)
        Session.commit()

        #follow(u8,u7)
        #follow(u8,u3)
        #follow(u8,u4)
        #follow(u8,u5)

        #Session.commit();

        # Create first item of content as content_id=1 for automated document examples to use
        a = ArticleContent()
        a.title   = u"API Documentation: Article"
        a.content = u"test content"
        a.creator = u1
        Session.add(a)
        Session.commit()

        b = CommentContent()
        b.title   = u"Comment Test"
        b.content = u"test comment"
        b.creator = u1
        b.parent  = a
        Session.add(b)
        Session.commit()

        c = ArticleContent()
        c.title   = u"API Documentation: Response"
        c.content = u"test response"
        c.creator = u1
        c.parent  = a
        Session.add(c)
        Session.commit()

        # Set settings var's so in development we dont get the popups all the time
        member_config      = [u1, u2]
        member_config_vars = ['help_popup_created_user',
                              'help_popup_created_group',
                              'help_popup_created_assignment',]
        for member_config_var in member_config_vars:
            for member in member_config:
                member.config[member_config_var] = 'init'

        assert list(Session.query(User).filter(User.id==0)) == []
        assert list(Session.query(User).filter(User.username=="MrNotExists")) == []
