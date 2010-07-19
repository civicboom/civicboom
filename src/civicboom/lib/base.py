"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons import request, app_globals, tmpl_context as c

from civicboom.model import meta
from civicboom.lib.database.get_cached import get_user

import logging
log = logging.getLogger(__name__)

class BaseController(WSGIController):

    def __before__(self):
      # AllanC
      # AuthKit would have already authenticated any cookies & sessions by this point
      # so lookup the reporter of the remote user
      # (someone who is slightly more security savy may want to double check the implications of this)
      c.logged_in_user = None
      try:    c.logged_in_user = get_user(request.environ['REMOTE_USER'])
      except: pass


    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()
