from civicboom.lib.base import *
from civicboom.model import User, Group, Media, Content
from civicboom.model.meta import location_to_string
from civicboom.lib.database.get_cached import get_member as _get_member

from civicboom.lib.communication.email_lib import send_email
from urllib import unquote_plus
import os

from civicboom.lib.form_validators.validator_factory         import DynamicSchema
from formencode.validators import UnicodeString, Email
from civicboom.lib.form_validators.registration import ReCaptchaValidator
from civicboom.lib.form_validators.dict_overlay import validate_dict

from civicboom.controllers.contents import ContentsController
content_search = ContentsController().index

from civicboom.controllers.members import MembersController
member_search = MembersController().index

from civicboom.lib.web import cookie_set

import datetime
import random
import re

static_org_descriptions = {
    'kentonline': 'Join us in making the news in Kent, by telling us your stories, sending in videos, pictures and audio - help us build a news picture of Kent.',
    'gradvine'  : 'Be part of a new online student community with the Gradvine. Get involved in creating your own news and online portfolio: Upload images, video and text then share it with Gradvine...and the world. Our network spans the whole of the UK, with a website just like this for every UK university and town. So your voice will be heard everywhere.'
}

static_org_descriptions.update({
    'unittest'    : static_org_descriptions['kentonline'],
    'unitfriend'  : static_org_descriptions['gradvine']
})


class MiscController(BaseController):
    @cacheable(time=600)
    @auto_format_output
    def about(self, id="civicboom"):
        if c.format in ["html", "mobile"] and os.path.exists(config['path.templates']+"/html/web/misc/about/"+id+".mako"):
            if id == "upgrade_plans":
                pass
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
        if c.logged_in_user:
            return redirect(url(controller="profile", action="index"))
        return action_ok()

    @web
    def new_article(self):
        if config['development_mode']:
            organisations = ['unittest', 'unitfriend']
        else:
            organisations = ['kentonline', 'gradvine']
        data = {'list':[],}
        for org in organisations:
            static_desc = static_org_descriptions.get(org)
            org = _get_member(org)
            push_assignment = org.config.get('push_assignment')
            if push_assignment:
                org_d = org.to_dict()
                org_d.update({'push_assignment': push_assignment, 'description': static_desc or org.description}) 
                data['list'].append(org_d)
        return action_ok(data=data)

    def search_redirector(self):
        if request.GET.get("type") == _("_Users / _Groups"): # these need to match the submit buttons
            return redirect(url(controller="members", action="index", term=request.GET.get("term"), sort="-join_date"))
        elif request.GET.get("type") == _("_Assignments"):
            return redirect(url(controller="contents", action="index", term=request.GET.get("term"), list="assignments_active"))
        elif request.GET.get("type") == _("_Articles"):
            return redirect(url(controller="contents", action="index", term=request.GET.get("term"), list="articles"))
        else:
            return redirect(url(controller="contents", action="index", term=request.GET.get("term"), list="all"))

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
    
    @web
    def get_link_embed(self, type=None, id=None):
        if type not in ['content']:
            raise action_error(code=404, message="Cannot link to this type")
        if not id:
            raise action_error(code=404, message="No id")
        return action_ok(data={'type':type, 'id':id})
    
    @web
    def what_is_a_hub(self):
        return action_ok()
    
    @web
    def how_to(self):
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
  <Param name="src" value="{referrer:source?}"/>
</Url>
<moz:SearchForm>https://www.civicboom.com/contents</moz:SearchForm>
</OpenSearchDescription>""" % (base64.b64encode(file("civicboom/public/images/boom16.ico").read()), )

    def robots(self):
        response.headers['Content-type'] = "text/plain"
        subdomain = request.environ.get("HTTP_HOST", "").split(".")[0]
        if subdomain == "www":
            return """
User-agent: *
Disallow: /misc/get_widget/
Disallow: /misc/about/
Disallow: /misc/help/
Disallow: /media/
Disallow: /*.frag$
"""
        else:
            return "User-agent: *\nDisallow: /\n"

    @web
    def upgrade_request(self, **kwargs):
        if not request.POST:
            return
        schema = DynamicSchema()
        schema.chained_validators = []
        schema.fields['name'] = UnicodeString(not_empty=True)
        schema.fields['phone'] = UnicodeString(not_empty=True)
        schema.fields['email'] = Email(not_empty=True)
        if not c.logged_in_user:
            schema.fields['recaptcha_challenge_field'] = UnicodeString(not_empty=True)
            schema.fields['recaptcha_response_field']  = UnicodeString(not_empty=True)
            schema.chained_validators.append(ReCaptchaValidator(request.environ['REMOTE_ADDR']))
            
        data = {'upgrade_request':kwargs}
        data = validate_dict(data, schema, dict_to_validate_key='upgrade_request')
            
        
        from civicboom.lib.communication.email_lib import send_email
        form_string = ''
        for key,value in kwargs.iteritems():
            form_string += '\n%s: %s' % (key,value)
            
        if c.logged_in_user:
            form_string += '\nlogged_in_user: %s' % (c.logged_in_user.username)
            form_string += '\nlogged_in_persona: %s' % (c.logged_in_persona.username)
        else:
            form_string += '\nUser not logged in!'
        
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
                    kwargs['from'] = request.environ['logged_in_user_email']
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

    #       - can't really be cashed because of the use of 'me'
    # Shish - rather than 'me', pass a 'location' parameter to the frag; this
    #         way a user with a location only gets feature updates every 10
    #         mins, and users without locations all share one featured set
    @web
    @cacheable(time=120, anon_only=False)
    def featured(self):
        """
        Make a numer of querys to get the top interesting content
        The results are randomised so single highest results don't dominate
        A list is kept of all the content before. There should never be any duplicated items
        """
        
        featured_content = []
               
        def rnd_content_items(return_items=1, **kwargs):
            if 'limit' not in kwargs:
                kwargs['limit'] = 3
            # searching due_date limits results to only assignments; if we want
            # all articles, then we don't want to limit to assignments
            #if 'due_date' not in kwargs and kwargs.get('type') == "assignment":
            #    kwargs['due_date'] = ">now"
            kwargs['update_date'] = ">"+str(now() - datetime.timedelta(days=5))
            kwargs['exclude_content'] = ",".join([str(content['id']) for content in featured_content])
            content_list = content_search(**kwargs)['data']['list']
            random.shuffle( content_list['items'] )
            return_list = []
            
            content_list['items'][:return_items]
            #content_list['count'] = len(content_list['items'])
            for content_item in content_list['items']:
                featured_content.append(content_item)
            
            return content_list
        
        
        #return to_apilist(featured_content, obj_type='contents') # AllanC - a liniear list of featured contebt
        
        # Sponsored content dictionary
        #s = {}
        #s['sponsored_responded'    ] = rnd_content_items(return_items=1, sort='-num_responses',              limit=3 )
        #s['sponsored_assignment'   ] = rnd_content_items(return_items=1, sort='-views',  type='assignment',  limit=3 )
        
        # Featured content dictionary
        f = {}
        ##f['top_viewed_assignments' ] = rnd_content_items(return_items=2, sort='-views'        , type='assignment', limit=5)
        f['recent'                 ] = rnd_content_items(return_items=2, sort='-update_date'  , limit=3)
        f['most_responses'         ] = rnd_content_items(return_items=2, sort='-num_responses', limit=3)
        if request.GET.get("location"):
            f['near_me'            ] = rnd_content_items(return_items=2, sort='distance'      , location=request.GET.get("location"), limit=3)
        f['recent_assignments'     ] = rnd_content_items(return_items=2, sort='-update_date'  , list='assignments_active', limit=3)
        
        
        # New members
        m ={}
        m['new_members'] = member_search(sort='-join_date', type='user'                        , limit=3)['data']['list']
        m['new_groups' ] = member_search(sort='-join_date', default_content_visibility='public', limit=3)['data']['list']
        
        # AllanC - HACK HACK!!!
        # The count from the query using the default_content_visibility='public' is wrong .. the content is correct .. the count is broken
        # Set the count FOR THIS LIST ONLY to match the items returned
        m['new_groups' ]['count'] = len(m['new_groups' ]['items'])
        
        return action_ok(
            data={
                #'sponsored' : s,
                'featured'  : f,
                'members'   : m,
            }
        )

    #---------------------------------------------------------------------------
    # Set force_web cookie
    #---------------------------------------------------------------------------
    def force_web(self):
        cookie_set('force_web', 'True', secure=False, sub_domain='') # The force web cookie is for all domains
        from pylons import response
        print response.set_cookie
        referer = current_referer()
        if referer:
            re.sub("(m\.)|(mobile\.)", "www.", referer, 1)
            return redirect(referer)
        return redirect(url(controller='misc', action='titlepage', sub_domain='web'))
