
from civicboom.lib.base import *


class ProfileController(BaseController):

    @auto_format_output()
    @authorize(is_valid_user)
    def index(self):
        c.viewing_user = c.logged_in_user
        return render("web/profile/index.mako")

    @auto_format_output()
    def view(self, id=None):
        if id:
            c.viewing_user = get_user(id)
        else:
            c.viewing_user = c.logged_in_user

        if not c.viewing_user:
            return action_error(_("User does not exist"), code=404)

        return render("web/profile/view.mako")
