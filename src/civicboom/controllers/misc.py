from civicboom.lib.base import *

class MiscController(BaseController):
    @cacheable(time=600)
    @auto_format_output
    def about(self):
        return action_ok()

    @cacheable(time=600)
    @auto_format_output
    def press(self):
        return action_ok()

    @cacheable(time=600)
    @auto_format_output
    def terms(self):
        return action_ok()

    @cacheable(time=600)
    @auto_format_output
    def privacy(self):
        return action_ok()

    @cacheable(time=60)
    @auto_format_output
    def titlepage(self):
        return action_ok()

    @cacheable(time=600)
    @auto_format_output
    def georss(self):
        return action_ok()

    @cacheable(time=600)
    @auto_format_output
    def credits(self):
        return action_ok()

    @cacheable(time=600)
    @auto_format_output
    def upgrade_account(self):
        return action_ok()

    def widget_preview(self, id=None):
        if not id: id = "unittest"
        c.widget_user_preview = get_member(id)
        return render("/widget/get_widget_code.mako")

    @cacheable(time=600)
    def close_popup(self):
        return '<script>self.close();</script>'
