
from civicboom.lib.base import *

prefix = '/web/design09/misc/'

class MiscController(BaseController):
    def index(self):
        return "misc controller"

    @cacheable(time=600)
    def about(self):
        return render(prefix+"about.mako")

    @cacheable(time=60)
    def titlepage(self):
        return render(prefix+"titlepage.mako")

    @cacheable(time=600)
    def georss(self):
        return render(prefix+"georss.mako")

    @cacheable(time=600)
    def credits(self):
        return render(prefix+"credits.mako")

    def widget_preview(self, id=None):
        if not id: id = "unittest"
        c.widget_user_preview = get_user(id)
        return render("/widget/get_widget_code.mako")

    @cacheable(time=600)
    def close_popup(self):
        return '<script>self.close();</script>'
