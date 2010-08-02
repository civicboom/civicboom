import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from civicboom.lib.base import BaseController, render
from civicboom.model.content           import Content, DraftContent
from civicboom.model.meta              import Session
from sqlalchemy                        import or_

log = logging.getLogger(__name__)
tmpl_prefix = '/web/design09'

class SearchController(BaseController):
    def index(self):
        # Return a rendered template
        #return render('/search.mako')
        # or, return a string
        return 'Hello World. Search for: [box]'

    def content(self, id=None):
        if not id:
            return redirect(url(controller='search', action='index'))
        results = Session.query(Content).filter(or_(Content.title.match(id), Content.content.match(id)))
        return render(tmpl_prefix+"/search/content.mako", extra_vars={"term": id, "results":results})

