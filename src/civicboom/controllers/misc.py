from civicboom.lib.base import *

class MiscController(BaseController):
    @cacheable(time=600)
    @auto_format_output
    def about(self, id="civicboom"):
        return action_ok(template="misc/about/"+id)

    @cacheable(time=600)
    @auto_format_output
    def help(self, id="civicboom"):
        return action_ok(template="help/"+id)

    @cacheable(time=600)
    @auto_format_output
    def echo(self):
        return action_ok(data={
            "GET": request.GET.dict_of_lists(),
            "POST": request.POST.dict_of_lists()
        })

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
    def upgrade_account(self):
        return action_ok()

    @web
    def get_widget(self, id=None):
        c.widget_user_preview = get_member(id)
        return action_ok()

    #@web
    #def get_mobile(self, id=None):
    #    return action_ok()


    @cacheable(time=600)
    def close_popup(self):
        return '<script>self.close();</script>'
