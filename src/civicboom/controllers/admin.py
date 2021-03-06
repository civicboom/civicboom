from civicboom.lib.base import *

import pylons
import pylons.test

from formalchemy.ext.pylons.controller import ModelsController
from webhelpers.paginate import Page

from civicboom.lib.database.userlog import get_engine
from civicboom import model
from civicboom import forms

import re

prefix = '/admin/'


def _get_info(frame):
    reqinfo = 'Unknown'
    f = frame
    while f is not None:
        if f.f_code.co_filename.endswith('/SocketServer.py') and f.f_code.co_name == 'handle_request':
            reqinfo = "Server"
            break
        if f.f_code.co_filename.endswith('/threading.py') and f.f_code.co_name == 'wait':
            reqinfo = "Idle Worker"
            break
        if f.f_code.co_filename.endswith('/reloader.py') and f.f_code.co_name == 'periodic_reload':
            reqinfo = "Pylons Reloader"
            break
        if f.f_code.co_filename.endswith('/lib/base.py') and f.f_code.co_name == '__call__':
            request = f.f_globals.get('request')
            if request is not None:
                reqinfo = (request.environ.get('REQUEST_METHOD', '') + ' ' + request.environ.get('PATH_INFO', ''))
                qs = request.environ.get('QUERY_STRING')
                if qs:
                    reqinfo += '?'+qs
            break
        f = f.f_back
    return reqinfo


class AdminControllerBase(BaseController):
    model = model # where your SQLAlchemy mappers are
    forms = forms # module containing FormAlchemy fieldsets definitions
    template = "/admin/restfieldset.mako"

    # logged in user should = https, and we check for logged in user,
    # but double check here in case we ever need to degrade the main
    # site security
    @https()
    def __before__(self):
        BaseController.__before__(self)
        admins = config['setting.admin_users'].split(",")
        if not (
            c.logged_in_persona and
            c.logged_in_persona.username in admins
        ):
            abort(403)

    # this is used by the superclass somehow
    def Session(self):
        return meta.Session

    ## customize the query for a model listing
    #def get_page(self):
    #    if self.model_name == 'Foo':
    #        return Page(meta.Session.query(model.Foo).order_by(model.Foo.bar)
    #    return super(AdminControllerBase, self).get_page()
    def get_page(self, **kwargs):
        S = meta.Session
        q = S.query(self.get_model())

        # FIXME: SQL injection; regex whitelist *should* stop it
        for name in [n for n in request.GET if "--" in n]:
            col_name = name[name.find("--")+2:]
            value = request.GET[name]
            if re.match("^[a-zA-Z0-9_]+$", col_name) and re.match("^[a-zA-Z0-9_]+$", value):
                if name == "User--id":  # FIXME: haaaaaaaaaack. id alone is ambiguous
                    q = q.filter("member.id = '%s'" % (str(value), ))
                elif re.match("^[0-9]+$", value):
                    q = q.filter("%s = %s" % (col_name, str(value)))
                elif col_name == "status":
                    q = q.filter("%s = '%s'" % (col_name, value))
                else:
                    q = q.filter("%s ILIKE '%s'" % (col_name, "%"+value+"%"))

        options = dict(collection=q, page=int(request.GET.get('page', '1')))
        options.update(request.environ.get('pylons.routes_dict', {}))
        options.update(kwargs)
        collection = options.pop('collection')
        return Page(collection, **options)


    #---------------------------------------------------------------------------
    # custom pages
    #---------------------------------------------------------------------------

    def threads(self):
        import sys
        import traceback
        items = sys._current_frames().items()
        dumps = []
        for thread, frame in items:
            dumps.append({
                "id": str(thread),
                "info": _get_info(frame),
                "trace": "\n".join(traceback.format_stack(frame)),
            })

        from webhelpers.html import HTML, literal
        out = literal()
        out += str(len(items))+" threads:\n"
        for data in dumps:
            out += HTML.br()
            out += HTML.a(data["info"], href="#"+data["id"])
        for data in dumps:
            out += HTML.hr()
            out += HTML.a(data["id"]+": "+HTML.b(data["info"]), name=data["id"])
            out += HTML.p()
            out += HTML.pre(data["trace"])
        return out

    def event_log(self):
        # Old-fashioned SQL building since events aren't part of the
        # SQLAlchemy model; beware of SQL injection
        wheres = ["1=1", ]
        args = []
        if "module" in request.params:
            wheres.append("module = %s")
            args.append(request.params["module"])
        if "line_num" in request.params:
            wheres.append("line_num = %s")
            args.append(int(request.params["line_num"]))
        if "username" in request.params:
            wheres.append("username = %s")
            args.append(request.params["username"])
        if "address" in request.params:
            wheres.append("address = %s")
            args.append(request.params["address"])
        if "url" in request.params:
            wheres.append("url = %s")
            args.append(request.params["url"])

        query = "SELECT * FROM events WHERE "
        where = " AND ".join(wheres)
        order = " ORDER BY date_sent DESC"
        offset = " OFFSET %d" % max(int(request.params.get("offset", "0")), 0)
        limit = " LIMIT 50"
        result = get_engine().execute(query + where + order + offset + limit, args).fetchall()
        return render(prefix + "eventlog.mako", extra_vars={"events": result})

    def user_emails(self, format):
        """
        Output CSV of all users ov civicboom
        """
        
        help_type_filter = request.params.get('help_type')
        
        from civicboom.model import User
        response.headers['Content-type'] = "text/csv; charset=utf-8"
        csv = []
        for user in Session.query(User).all():
            if user.config.get('no_marketing_emails'):
                continue
            if help_type_filter and user.config.get('help_type', 'ind') != help_type_filter:
                continue
            csv.append(','.join([user.username, user.name or "", user.email_normalized or "", user.status]))
        return "\n".join(csv)
    
    

    def moderate(self):
        """
        This is a hack and a minor security hole,
        but it makes Lizzie happy.

        The security hole is that it is an unchecked
        GET request, so that it works straight from
        the email client. It also works straight from
        another site's IMG tag.

        To minimise the impact of this, content is
        only hidden, not removed.
        """
        k = request.params['kay']
        c = get_content(request.params['content_id'])

        if not c:
            user_log.info("Admin tried to moderate content, it wasn't found")
            return "Content not found"

        if len(c.flags) == 0:
            user_log.info("Admin tried to moderate content, it wasn't flagged")
            return "Content is not flagged"

        if k == "yay":
            c.flags = []
            Session.commit()
            user_log.info("Admin moderated content as OK")
            return "Flags removed"

        if k == "nay":
            c.visible = False
            Session.commit()
            user_log.info("Admin moderated content as Bad")
            return "Content hidden"

        return "Unknown status"


AdminController = ModelsController(AdminControllerBase,
                                   prefix_name='admin',
                                   member_name='model',
                                   collection_name='models',
                                  )
