from civicboom.lib.base import BaseController, render, c

from civicboom.lib.database.get_cached import get_user

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

    def georss(self):
        return render(prefix+"georss.mako")

    def credits(self):
        return render(prefix+"credits.mako")

    def widget_preview(self, id=None):
        if not id: id = "unittest"
        c.widget_user_preview = get_user(id)
        return render("/widget/get_widget_code.mako")
        
    def close_popup(self):
        return '<script>self.close();</script>'