from civicboom.lib.base import *

from civicboom.lib.communication.email_lib import send_email
from urllib import quote_plus, unquote_plus

class MiscController(BaseController):
    @cacheable(time=600)
    @auto_format_output
    def about(self, id="civicboom"):
        return action_ok(template="misc/about/"+id)

    @cacheable(time=600)
    @auto_format_output
    def help(self, id="civicboom"):
        return action_ok(template="help/"+id)

    #@cacheable(time=600)
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

    @cacheable(time=30)
    @auto_format_output
    def stats(self):
        from civicboom.model import User, Group, Media, Content
        return action_ok(data={
            'users':     Session.query(User).filter(User.status=="active").count(),
            'pending':   Session.query(User).filter(User.status=="pending").count(),
            'groups':    Session.query(Group).count(),
            'media':     Session.query(Media).count(),
            'requests':  Session.query(Content).filter(Content.__type__=="assignment").count(),
            'responses': Session.query(Content).filter(Content.__type__=="article" and Content.parent_id!=None).count(),
            'articles':  Session.query(Content).filter(Content.__type__=="article" and Content.parent_id==None).count(),
            'comments':  Session.query(Content).filter(Content.__type__=="comment").count(),
        })

    @web
    def get_widget(self, id=None):
        c.widget_user_preview = get_member(id)
        return action_ok()

    @auto_format_output
    def feedback(self):
        if not request.POST:
            return action_ok() # Render the feedback form by autolocating the template
        if 'message' in request.POST:
            content_text = "%(from_)s\n\n%(message)s\n\n%(env)s" % dict(message=request.POST.get('message'), env=unquote_plus(request.POST.get('env')), from_=request.POST.get('from') )
            send_email(config['email.contact'], subject=_('_site_name feedback'), content_text=content_text)
            return action_ok(_("Thank you for your feedback"), code=201)
