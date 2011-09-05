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

        # Notifications disabled because no i18n is setup
        from pylons import config
        config['feature.notifications'] = False


        ###############################################################
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
        assert u1.id == 1
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

        # Set settings var's so in development we dont get the popups all the time
        member_config      = [u1, u2]
        member_config_vars = ['help_popup_created_user',
                              'help_popup_created_group',
                              'help_popup_created_assignment',]
        for member_config_var in member_config_vars:
            for member in member_config:
                member.config[member_config_var] = 'init'

        assert list(Session.query(User).filter(User.id=="MrNotExists")) == []
