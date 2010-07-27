
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from formalchemy.ext.pylons.controller import ModelsController
from webhelpers.paginate import Page

from civicboom.lib.base import BaseController, render
from civicboom.lib.userlog import get_engine
from civicboom import model
from civicboom import forms
from civicboom.model import meta

import logging
import re

prefix = '/admin/'

class AdminControllerBase(BaseController):
    model = model # where your SQLAlchemy mappers are
    forms = forms # module containing FormAlchemy fieldsets definitions
    template = "/admin/restfieldset.mako"

    # # Uncomment this to impose an authentication requirement
    # @authorize(SignedIn())
    # def __before__(self):
    #     pass

    def Session(self): # Session factory
        return meta.Session

    ## customize the query for a model listing
    #def get_page(self):
    #    if self.model_name == 'Foo':
    #        return Page(meta.Session.query(model.Foo).order_by(model.Foo.bar)
    #    return super(AdminControllerBase, self).get_page()
    def get_page(self, **kwargs):
        S = self.Session()
        q = S.query(self.get_model())

        # FIXME: SQL injection; regex whitelist *should* stop it
        for name in request.GET.keys():
            col_name = name[name.find("--")+2:]
            value = request.GET[name];
            if re.match("^[a-zA-Z0-9_]+$", col_name) and re.match("^[a-zA-Z0-9_]+$", value):
                if re.match("^[0-9]+$", value):
                    q = q.filter("%s = %s" % (col_name, str(value)))
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
        result = connection.execute(query + where + order, args)
        return render(prefix + "eventlog.mako", extra_vars={"events": list(result)})

AdminController = ModelsController(AdminControllerBase,
                                   prefix_name='admin',
                                   member_name='model',
                                   collection_name='models',
                                  )
