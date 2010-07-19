from civicboom.lib.base import BaseController, render, c

prefix = '/misc/'

class MiscController(BaseController):

    def test(self):
      test_text = "test controller action"
      if c.logged_in_user:
        test_text += " user logged in: " + c.logged_in_user.username
      return test_text #render(prefix + 'contact.mako')
