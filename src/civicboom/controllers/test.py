"""
TestController
A conroller for miscilanious test functions
Locked down for use in development mode only
"""

from civicboom.lib.base   import BaseController, render, c, config, app_globals, abort, session, redirect, flash_message
from civicboom.model.meta import Session
from civicboom.model      import Member

from civicboom.lib.authentication      import authorize, is_valid_user



import logging
log = logging.getLogger(__name__)

class TestController(BaseController):
    
    # Only allow these actions if in development mode
    def __before__(self, action, **params):
        if not config['development_mode']==True:
            return abort(403)
        BaseController.__before__(self)

    def test_memcache(self):
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

    def test_session(self):
        flash_message("hello session test")
        return redirect('/')

    @authorize(is_valid_user)
    def test_logged_in(self):
        return "you are logged in"

    def test_db_read(self):
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
        s = Session
        m = s.query(Member).first()
        m.config["height"] = 41
        m.config["height"] = 42
        m.config["height"] = 43
        return m.config["height"]
