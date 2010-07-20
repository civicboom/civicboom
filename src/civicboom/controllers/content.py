"""
Content Controller

For managing content:
-creating/editing
-attaching media
-deleting
-flagging
"""

from civicboom.lib.base import BaseController, render, c
from civicboom.lib.misc import flash_message

import logging
log = logging.getLogger(__name__)

prefix = "/web/content_editor/"


class ContentController(BaseController):
  
  def upload(self):
    return render(prefix + "content_editor.mako")
  
  def upload_media(self,id):
    pass

  def delete(self,id):
    pass
  
  def flag(self,id):
    pass