import logging

from pylons import request, response, session, tmpl_context as c, url, app_globals
from pylons.controllers.util import abort, redirect
from pylons.decorators.secure import authenticate_form

from civicboom.lib.base import BaseController, render
from civicboom.lib.database.get_cached import get_user
from civicboom.lib.authentication      import authorize, is_valid_user

import hashlib

log = logging.getLogger(__name__)

class UserProfileController(BaseController):
    def index(self):
        c.viewing_user = c.logged_in_user
        return render("web/user_profile/index.mako")

    def view(self, id=None):
        if id:
            c.viewing_user = get_user(id)
        else:
            c.viewing_user = c.logged_in_user
        return render("web/user_profile/view.mako")
