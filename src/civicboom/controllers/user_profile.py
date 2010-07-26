import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from civicboom.lib.base import BaseController, render
from civicboom.lib.database.get_cached import get_user

log = logging.getLogger(__name__)

class UserProfileController(BaseController):
    def view(self, id=None):
        if id:
            c.viewing_user = get_user(id)
        else:
            c.viewing_user = c.logged_in_user
        return render("web/user_profile/view.mako")

    def edit(self):
        c.viewing_user = c.logged_in_user
        return render("web/user_profile/edit.mako")
