import logging

from pylons import request, response, session, tmpl_context as c, url, app_globals
from pylons.controllers.util import abort, redirect
from pylons.decorators.secure import authenticate_form

from civicboom.lib.base import BaseController, render
from civicboom.lib.database.get_cached import get_user
from civicboom.lib.authentication      import authorize, is_valid_user

log = logging.getLogger(__name__)

class UserProfileController(BaseController):
    def view(self, id=None):
        if id:
            c.viewing_user = get_user(id)
        else:
            c.viewing_user = c.logged_in_user
        return render("web/user_profile/view.mako")

    @authorize(is_valid_user)
    def edit(self, id=None):
        c.viewing_user = c.logged_in_user
        return render("web/user_profile/edit.mako")

    @authorize(is_valid_user)
    @authenticate_form
    def save(self, id=None):
        c.viewing_user = c.logged_in_user

        u_config = c.viewing_user.config
        current_keys = u_config.keys()
        for key in request.POST.keys():
            if request.POST[key] == app_globals.user_defaults.get("settings", key):
                if key in current_keys:
                    del u_config[key]
            else:
                c.viewing_user.config[key] = request.POST[key]
        return "Settings saved "+", ".join(request.POST.keys())
