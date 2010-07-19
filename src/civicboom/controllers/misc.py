from civicboom.lib.base import BaseController, render, c
import logging

user_log = logging.getLogger("user")
prefix = '/misc/'

class MiscController(BaseController):

    def test(self):
      test_text = "test controller action"
      if c.logged_in_user:
        test_text += " user logged in: " + c.logged_in_user.username
      return test_text #render(prefix + 'contact.mako')

    def fill_log(self):
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
