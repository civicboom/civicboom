"""
TestController
A conroller for miscilanious test functions
Locked down for use in development mode only
"""
from pylons.controllers.util import abort

from civicboom.model.meta import Session
from civicboom.model import Member
from civicboom.lib.base import BaseController, render, c, config


import logging
log = logging.getLogger(__name__)

class TestController(BaseController):
    def __before__(self, action, **params):
        #if not getattr(app_globals,'development_mode')==True:
        if not config['development_mode']==True:
            return abort(403)
        BaseController.__before__(self)

    def test(self):
        test_text = "test controller action"
        if c.logged_in_user:
            test_text += " user logged in: " + c.logged_in_user.username
        return test_text #render(prefix + 'contact.mako')

    def environ(self):
        env_string = ""
        from pylons import request
        for key in request.environ.keys():
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
