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
        if pylons.test.pylonsapp:
            # allow tests to see admin?
            # this could be done better when we have a proper admin definiton
            return
        if (not c.logged_in_user) or (c.logged_in_user.username not in ["Shish", "unittest"]): # pragma: no cover - tests take the shortcut above
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
        for name in request.GET.keys():
            col_name = name[name.find("--")+2:]
            value = request.GET[name];
            if re.match("^[a-zA-Z0-9_]+$", col_name) and re.match("^[a-zA-Z0-9_]+$", value):
                if re.match("^[0-9]+$", value):
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

        connection = get_engine().connect()
        query = "SELECT * FROM events WHERE "
        where = " AND ".join(wheres)
        order = " ORDER BY date_sent DESC"
        limit = " LIMIT 50"
        result = connection.execute(query + where + order + limit, args)
        return render(prefix + "eventlog.mako", extra_vars={"events": list(result)})

AdminController = ModelsController(AdminControllerBase,
                                   prefix_name='admin',
                                   member_name='model',
                                   collection_name='models',
                                  )
