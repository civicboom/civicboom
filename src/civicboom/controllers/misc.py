from civicboom.lib.base import *
from civicboom.model import User, Group, Media, Content
from civicboom.lib.database.get_cached import get_member as _get_member

from civicboom.lib.communication.email_lib import send_email
from urllib import quote_plus, unquote_plus
import os



class MiscController(BaseController):
    @cacheable(time=600)
    @auto_format_output
    def about(self, id="civicboom"):
        if c.format in ["html", "mobile"] and os.path.exists(config['path.templates']+"/html/web/misc/about/"+id+".mako"):
            return action_ok(template="misc/about/"+id)
        else:
            raise action_error(code=404, message="No description for this topic")

    @cacheable(time=600)
    @auto_format_output
    def help(self, id="civicboom"):
        if c.format == "frag" and os.path.exists(config['path.templates']+"/frag/misc/help/"+id+".mako"):
            return action_ok(template="misc/help/"+id)
        else:
            raise action_error(code=404, message="No help for this topic")

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
        return action_ok(data={
            'users':     Session.query(User).filter(User.status=="active").count(),
            'pending':   Session.query(User).filter(User.status=="pending").count(),
            'groups':    Session.query(Group).count(),
            'media':     Session.query(Media).count(),
            'requests':  Session.query(Content).filter(Content.__type__=="assignment").count(),
            'responses': Session.query(Content).filter(Content.__type__=="article").filter(Content.parent_id!=None).count(),
            'articles':  Session.query(Content).filter(Content.__type__=="article").filter(Content.parent_id==None).count(),
            'comments':  Session.query(Content).filter(Content.__type__=="comment").count(),
        })

    @web
    def get_widget(self, id=None):
        c.widget_user_preview = _get_member(id)
        return action_ok()

    def opensearch(self, format="xml"):
        import base64
        return """<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/" xmlns:moz="http://www.mozilla.org/2006/browser/search/">
<ShortName>Civicboom</ShortName>
<Description>Search Civicboom</Description>
<InputEncoding>UTF-8</InputEncoding>
<Image width="16" height="16">data:image/x-icon;base64,%s</Image>
<Url type="text/html" method="get" template="https://www.civicboom.com/contents">
  <Param name="term" value="{searchTerms}"/>
</Url>
<moz:SearchForm>https://www.civicboom.com/contents</moz:SearchForm>
</OpenSearchDescription>""" % (base64.b64encode(file("civicboom/public/images/boom16.ico").read()), )

    @web
    def upgrade_plans(self):
        c.upgrade_plans_title = 'You have reached your Basic account limit for this month.'
        c.upgrade_plans_subtitle = 'If you want to get more from Civicboom you can choose premium or above:'
        return action_ok()
    
    @web
    def feedback(self, **kwargs):
        if not request.POST:
            return action_ok() # Render the feedback form by autolocating the template
        else:
            user_log.info("Sending feedback")
            @authenticate_form
            def submit_feedback(**kwargs):
                if c.logged_in_user:
                    kwargs['from'] = (c.logged_in_user.email or c.logged_in_user.email_unverified) # if isinstance(c.logged_in_user, User) else 'noreply@civicboom.com' # AllanC - should never happen, was just a one off problem when user was upgraded by hand
                else:
                    if kwargs.get('simple_captcha') != 'xyz':
                        raise action_error('invalid capture')
                    
                if not kwargs.get('env'):
                    kwargs['env'] = ''
                    for key,value in request.environ.iteritems():
                        kwargs['env'] += "%s:%s\n" % (key,value)
                if kwargs.get('referer'):
                    kwargs['referer'] = unquote_plus(kwargs['referer'])
                content_text = "%(referer)s\n\n%(category)s\n\n%(from_)s\n\n%(message)s\n\n%(env)s" % dict(message=kwargs.get('message'), env=unquote_plus(kwargs.get('env')), from_=kwargs.get('from'), category=kwargs.get('category'), referer=kwargs.get('referer') )
                send_email(config['email.contact'], subject=_('_site_name feedback'), content_text=content_text, sender=kwargs['from'])
                return action_ok(_("Thank you for your feedback"), code=201)
            return submit_feedback(**kwargs)
