from civicboom.lib.base import BaseController, render, c

import logging
log = logging.getLogger(__name__)

prefix = '/web/design09/misc/'

class MiscController(BaseController):

  def index(self):
    return "misc controller"

  def about(self):
    return render(prefix+"about.mako")
    
  def titlepage(self):
    return render(prefix+"titlepage.mako")