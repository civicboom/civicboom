"""
TestController
A conroller for miscilanious test functions
Locked down for use in development mode only
"""

from civicboom.lib.base import *
from time import sleep

log = logging.getLogger(__name__)


class TestController(BaseController):
    
    # Only allow these actions if in development mode
    def __before__(self, action, **params):
        if not config['development_mode']==True:
            return abort(403)
        BaseController.__before__(self)

    def memcache(self):
        mc = app_globals.memcache
        
        print "old: %s" % mc.get("old_key")
        mc.set("some_key", "Some value")
        mc.set("some_key", "Some value again!", time=60)
        mc.set("old_key" , "some value"       , time=2)
        mc.set("another_key", 3)
        mc.delete("another_key")
        mc.set("key", "1")   # note that the key used for incr/decr must be a string.
        mc.incr("key")
        mc.decr("key")
        mc.incr("key")
        print "value: %s" % mc.get("some_key")
        print "inc  : %s" % mc.get("key")

    def session(self):
        flash_message("hello session test")
        return redirect('/')

    @authorize(is_valid_user)
    def logged_in(self):
        return "you are logged in"

    def db_read(self):
        from civicboom.lib.database.get_cached import get_licenses
        print "printing licence names"
        for licence in get_licenses():
            print licence.name

    def environ(self):
        env_string = ""
        from pylons import request
        keys = request.environ.keys()
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
        m.send_message(messages.msg_test(text="hello o/"))

    def email_render(self):
        from webhelpers.html import literal
        c.email_content = literal("<h1>Email Test OK!</h1>")
        return render('email/base_email_from_plaintext.mako')

    def new_random_user(self):
        from civicboom.model.member import User, UserLogin
        from civicboom.lib.authentication import encode_plain_text_password
        from civicboom.lib.misc import random_string
        
        u = User()
        u.username = unicode(random_string())
        
        u_login = UserLogin()
        u_login.user   = u
        u_login.type   = 'password'
        u_login.token  = encode_plain_text_password('password')

        Session.add(u)
        Session.add(u_login)
        
        Session.commit()
        
    def content_morph(self):
        from civicboom.lib.database.polymorphic_helpers import morph_content_to
        morph_content_to(2, "article")

    def ssi(self):
        return '[Start] <!--#include virtual="/test/include1"--> <!--#include virtual="/test/include2"--> [End]'

    def psi(self):
        return "[Start] "+self.include1()+" "+self.include2()+" [End]"

    @cacheable(time=10)
    def include1(self):
        sleep(3)
        return "hello"

    @cacheable(time=10)
    def include2(self):
        sleep(3)
        return "world"

    #@cacheable(time=10)
    def include3(self):
        return "speed"

    def abort_test(self, id):
        return abort(int(id))