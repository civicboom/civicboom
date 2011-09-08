"""
TestController
A conroller for miscilanious test functions
Locked down for use in development mode only
"""

from civicboom.lib.base import *
from civicboom.lib.web import cookie_get, cookie_set, cookie_delete

from cbutils.misc import set_now

from paste.deploy.converters import asbool

import datetime
from time import sleep, time
from dateutil.parser import parse as parse_date


log = logging.getLogger(__name__)


class TestController(BaseController):
    
    # Only allow these actions if in development mode
    def __before__(self, action, **params):
        if not config['development_mode']==True:
            return abort(403)
        BaseController.__before__(self)

    def memcache(self):
        mc = app_globals.memcache
        
        log.debug("old: %s" % mc.get("old_key"))
        mc.set("some_key", "Some value")
        mc.set("some_key", "Some value again!", time=60)
        mc.set("old_key" , "some value"       , time=2)
        mc.set("another_key", 3)
        mc.delete("another_key")
        mc.set("key", "1")   # note that the key used for incr/decr must be a string.
        mc.incr("key")
        mc.decr("key")
        mc.incr("key")
        log.debug("value: %s" % mc.get("some_key"))
        log.debug("inc  : %s" % mc.get("key"))

    def session(self):
        flash_message("hello session test")
        return redirect('/')

    def extra(self):
        from civicboom.model import Content
        c = Session.query(Content).get(1)
        #c.extra_fields['moo'] = 'cake'
        #c.extra_fields['pie'] = 3.14159
        c.extra_fields['hits'] = c.extra_fields.get('hits', 0) + 1
        #c.extra_fields['hits'] = 42
        Session.commit()
        return str(c.extra_fields)

    @authorize
    def logged_in(self):
        return "you are logged in"

    def db_read(self):
        from civicboom.lib.database.get_cached import get_licenses
        log.debug("printing licence names")
        for licence in get_licenses():
            log.debug(licence.name)

    def environ(self):
        env_string = ""
        from pylons import request
        keys = list(request.environ.keys())
        keys.sort()
        for key in keys:
            env_string += "<b>%s</b>:%s<br/>\n" % (key,request.environ[key])
        return env_string

    def fill_log(self):
        user_log = logging.getLogger("user")
        user_log.debug("debug")
        user_log.info("info")
        user_log.warning("warning")
        user_log.error("error")
        user_log.critical("critical")
        return 'Log events added'

    def fail(self):
        return None + None

    def ping(self):
        return 'pong'

    def setting(self):
        from civicboom.model.member import Member
        m = Session.query(Member).first()
        m.config["height"] = 41
        m.config["height"] = 42
        m.config["height"] = 43
        return m.config["height"]

    def send_message(self):
        from civicboom.model.member import Member
        import civicboom.lib.communication.messages as messages
        m = Session.query(Member).first()
        m.send_notification(messages.msg_test(text="hello o/"))

    def send_email(self):
        from civicboom.lib.database.get_cached import get_member
        m = get_member("mobiletest")
        m.send_email(subject="Test Email", content_text="This is testing the email module. Hello")
        return "email test sent"

    def email_render(self):
        from webhelpers.html import literal
        c.email_content = literal("<h1>Email Test OK!</h1>")
        return render('email/base_email_from_plaintext.mako')

    def new_random_user(self):
        from civicboom.model.member import User, UserLogin
        from civicboom.lib.authentication import encode_plain_text_password
        from cbutils.misc import random_string
        
        u = User()
        u.username = unicode(random_string())
        
        u_login = UserLogin()
        u_login.user   = u
        u_login.type   = 'password'
        u_login.token  = encode_plain_text_password('password')

        Session.add(u)
        Session.add(u_login)
        
        Session.commit()
        
    def post_faker(self):
        return render("test_post_faker.mako")
        
    def content_morph(self):
        from civicboom.lib.database.polymorphic_helpers import morph_content_to
        morph_content_to(2, "article")

    def abort(self, id):
        return abort(int(id))

    @web_params_to_kwargs
    def recaptcha(self, **kwargs):
        c.kwargs = kwargs
        from pylons import request

        if request.environ['REQUEST_METHOD'] == 'POST':
            from civicboom.lib.services.reCAPTCHA import reCAPTCHA_verify
            reponse = reCAPTCHA_verify(
                remote_ip = request.environ['REMOTE_ADDR'],
                challenge = kwargs['recaptcha_challenge_field'],
                response  = kwargs['recaptcha_response_field'],
            )
            c.kwargs['response'] = reponse
        
        return render('/test/test_recaptha.mako')

    def frag(self, **kwargs):
        return render('/test/test_frag.mako')


    def toggle_cache(self):
        """
        For development, caching done by nginx can be disabled
        """
        if cookie_get("nocache"):
            cookie_delete("nocache")
            return "cache enabled"
        else:
            cookie_set("nocache", "caching disabled while this cookie exists")
            return "cache disabled"

    def toggle_force_mobile(self):
        """
        For development, allow faking of mobile subdomain by setting a force_mobile cookie
        """
        if cookie_get("force_mobile"):
            cookie_delete("force_mobile")
            return "not force_mobile"
        else:
            cookie_set("force_mobile","force the mobile version of the site for development")
            return "force_mobile"


    #---------------------------------------------------------------------------
    # runtime Config var modification
    #---------------------------------------------------------------------------

    @web_params_to_kwargs
    def config_var(self, key=None, value=None):
        """
        Used to get and set config vars from automated tests
        """
        if isinstance(key, basestring):
            if isinstance(value, basestring):
                # Preserve the data type of the existing config var
                if isinstance(config[key], bool):
                    config[key] = asbool(value)
                elif isinstance(config[key], int):
                    config[key] = int(value)
                else:
                    config[key] = value
                log.info('set config[%s] = %s' % (key, value))
            return '{"%s":"%s"}' % (key, config.get(key))

    #---------------------------------------------------------------------------
    # Runtime server_datetime modification - for automated tests
    #---------------------------------------------------------------------------

    @web_params_to_kwargs
    def server_datetime(self, new_datetime=None):
        """
        Used to get set date for automated tests
        """
        if new_datetime=='now':
            set_now() # Reset any existing date
        try:
            set_now(parse_date(new_datetime, dayfirst=True, yearfirst=True))
        except:
            pass
        
        return '{"datetime":"%s"}' % now()


    #---------------------------------------------------------------------------
    # Upgrade User to Group
    #---------------------------------------------------------------------------

    @web_params_to_kwargs
    def upgrade_user_to_group(self, **kwargs):
        from civicboom.lib.database.actions import upgrade_user_to_group
        upgrade_user_to_group(
            kwargs.get('member_to_upgrade_to_group'),
            kwargs.get('new_admins_username'),
            kwargs.get('new_group_username')
        )
        redirect_to_referer()

    #---------------------------------------------------------------------------
    # Upgrade Account
    #---------------------------------------------------------------------------
    @web_params_to_kwargs
    def set_account_type(self, id, account_type='plus', do_not_bill=True):
        """
        this is tempory measure for upgrading accounts
        It is used by the automated tests and should never be triggered by an actual user
        
        TODO needs to be upgraded to take param of account it is going too
        """
        if get_member(id).set_payment_account(account_type):
            # If account_type is free then no payment account is set on the member
            if account_type != 'free':
                Session.commit()
                get_member(id).payment_account.do_not_bill = do_not_bill
            Session.commit()
            return 'ok'
