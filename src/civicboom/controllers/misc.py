from civicboom.lib.base import BaseController, render, c

import logging
log = logging.getLogger(__name__)

prefix = '/misc/'

class MiscController(BaseController):

  def index(self):
    return "misc controller"
