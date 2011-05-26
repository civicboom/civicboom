from civicboom.lib.base import *
from civicboom.model import User, Group, Media, Content
from civicboom.lib.database.get_cached import get_member as _get_member

from civicboom.lib.communication.email_lib import send_email
from urllib import quote_plus, unquote_plus
import os

from civicboom.controllers.contents import ContentsController
content_search = ContentsController().index
import datetime
import random


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
        # caching different pages for different r= params is ok; but can't
        # cache different content for different UAs :(  Workaround: if r=qr,
        # redirect to an un-cached page
        if request.GET.get("r") == "qr":
            return redirect(url(controller="misc", action="qr"))
        return action_ok()

    # don't cache this, it does UA-specific things
    @auto_format_output
    def qr(self):
        ua = request.environ.get("HTTP_USER_AGENT",'').lower()
        # currently the landing page only makes sense for android
        #if "android" not in ua:
        #    return redirect("/")
        return action_ok()

    @cacheable(time=600)
    @auto_format_output
    def georss(self):
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

    def robots(self):
        response.headers['Content-type'] = "text/plain"
        subdomain = request.environ.get("HTTP_HOST", "").split(".")[0]
        if subdomain in ["api-v1", ]:
            return "User-agent: *\nDisallow: /\n"
        else:
            return """
User-agent: *
Disallow: /misc/get_widget/
"""

    @web
    @auth
    def upgrade_request(self, **kwargs):
        if not request.POST:
            return
        
        from civicboom.lib.communication.email_lib import send_email
        form_string = ''
        for key,value in kwargs.iteritems():
            form_string += '\n%s: %s' % (key,value)
        send_email(config['email.contact'], subject='Civicboom', content_text='upgrade account request: %s' % form_string)
        
        return action_ok(_('upgrade request sent'))

    @web
    def upgrade_popup(self, **kwargs):
        return action_ok()

    @web
    def browser_unsupported(self, **kwargs):
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
                    kwargs['from'] = (c.logged_in_user.email or c.logged_in_user.email_unverified)
                else:
                    if kwargs.get('simple_captcha') != 'xyz':
                        raise action_error('invalid capture')
                    
                if not kwargs.get('env'):
                    kwargs['env'] = ''
                    for key,value in request.environ.iteritems():
                        kwargs['env'] += "%s:%s\n" % (key,value)
                if kwargs.get('referer'):
                    kwargs['referer'] = unquote_plus(kwargs['referer'])
                content_text = "%(referer)s\n\n%(category)s\n\n%(from_)s\n\n%(message)s\n\n%(env)s" % dict(
                    message=kwargs.get('message'),
                    env=unquote_plus(kwargs.get('env')),
                    from_=kwargs.get('from'),
                    category=kwargs.get('category'),
                    referer=kwargs.get('referer')
                )
                send_email(config['email.contact'], subject=_('_site_name feedback'), content_text=content_text, reply_to=kwargs['from'])
                return action_ok(_("Thank you for your feedback"), code=201)
            return submit_feedback(**kwargs)


    #---------------------------------------------------------------------------
    # Featured content query
    #---------------------------------------------------------------------------
    @web
    #@cacheable(time=600)
    def featured(self):
        """
        Make a numer of querys to get the top interesting content
        The results are randomised so single highest results don't dominate
        """
        
        featured_content = []
        
        def rnd_content_items(return_items=1, **kwargs):
            if 'limit' not in kwargs:
                kwargs['limit'] = 3
            if 'after' not in kwargs:
                kwargs['after'] = now() - datetime.timedelta(days=7)
            kwargs['exclude_content'] = [content['id'] for content in featured_content] #",".join([str(
            content_items = content_search(**kwargs)['data']['list']['items']
            random.shuffle( content_items )
            return_list = []
            for i in range(return_items):
                if content_items:
                    content_item = content_items.pop()
                    featured_content.append(content_item)
                    return_list     .append(content_item)
            return return_list
        
        #return to_apilist(featured_content, obj_type='content') # AllanC - a liniear list of featured contebt
        
        return action_ok(
            data={
                'top_viewed_assignments' : rnd_content_items(return_items=2, sort='-views'        , type='assignment', limit=5),
                'most_responses'         : rnd_content_items(return_items=2, sort='-num_responses'                   , limit=5),
                'near_me'                : rnd_content_items(return_items=2,                        location='me'    , limit=5),
                'recent_assignments'     : rnd_content_items(return_items=2, sort='-update_date'  , type='assignment', limit=5),
                'recent'                 : rnd_content_items(return_items=2, sort='-update_date'  , type='article'   , limit=5),
            }
        )