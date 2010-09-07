from civicboom.lib.base import *
import hashlib

log = logging.getLogger(__name__)
user_log = logging.getLogger("user")

class SettingsController(BaseController):

    @authorize(is_valid_user)
    def general(self, id=None):
        c.viewing_user = c.logged_in_user
        return render("web/settings/general.mako")

    @https()
    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def save_general(self, id=None, format="html"):
        c.viewing_user = c.logged_in_user
        u_config = c.viewing_user.config
        current_keys = u_config.keys()

        # handle special cases
        if "move_to_gravatar" in request.POST.keys():
            if request.POST["move_to_gravatar"] == "on":
                c.viewing_user.avatar = None
            del request.POST["move_to_gravatar"]

        # FIXME: helper function for "is valid display name", see feature #54
        if "name" in request.POST.keys():
            if len(request.POST["name"]) > 0:
                c.viewing_user.name = request.POST["name"]
            del request.POST["name"]

        # FIXME: check for validity before changing
        if "email" in request.POST.keys():
            if len(request.POST["email"]) > 0:
                c.viewing_user.email = request.POST["email"]
            del request.POST["email"]

        # TODO: figure out stuff for User.logins[].password
        if "current_password" in request.POST.keys():
            hex_curr = hashlib.sha1(request.POST["current_password"]).hexdigest()
            hex_new1 = hashlib.sha1(request.POST["new_password_1"]).hexdigest()
            hex_new2 = hashlib.sha1(request.POST["new_password_2"]).hexdigest()
            if False:
                if hex_curr == c.viewing_user.password:
                    if hex_new1 == hex_new2:
                        c.viewing_user.password = hex_new1
                    else:
                        error = action_error(_("New passwords don't match"))
                else:
                    error = action_error(_("Current password was wrong"))
            del request.POST["current_password"]
            del request.POST["new_password_1"]
            del request.POST["new_password_2"]

        # everything that's left is treated as a config value
        for key in request.POST.keys():
            if request.POST[key] == app_globals.user_defaults.get("settings", key):
                if key in current_keys:
                    del u_config[key]
            else:
                c.viewing_user.config[key] = request.POST[key]

        return action_ok(_("Settings saved"))#+", ".join(request.POST.keys())

    @authorize(is_valid_user)
    def messages(self, id=None):
        c.viewing_user = c.logged_in_user
        return render("web/settings/messages.mako")

    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def save_messages(self, id=None, format="html"):
        c.viewing_user = c.logged_in_user
        from civicboom.lib.communication.messages import generators
        for gen in generators:
            route_name = "route_"+gen[0]
            setting = "".join([
                request.POST.get(gen[0]+"_n", ""),
                request.POST.get(gen[0]+"_e", ""),
                request.POST.get(gen[0]+"_c", ""),
            ])
            if setting == gen[1]:
                if route_name in c.viewing_user.config:
                    del c.viewing_user.config[route_name]
            else:
                c.viewing_user.config[route_name] = setting

        return action_ok(_("Settings saved"))

    @authorize(is_valid_user)
    def location(self, id=None):
        c.viewing_user = c.logged_in_user
        return render("web/settings/location.mako")

    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def save_location(self, id=None, format="html"):
        if "location" in request.POST:
            try:
                (lon, lat) = [float(n) for n in request.POST["location"].split(",")]
            except Exception, e:
                user_log.exception("Unable to understand location '%s'" % str(request.POST["location"]))
                return action_error(_("Unable to understand location '%s'" % str(request.POST["location"])))
        elif "location_name" in request.POST:
            (lon, lat) = (0, 0) # FIXME: guess_lon_lat_from_name(request.POST["location_name"]), see Feature #47
        else:
            return action_error(_("No position specified"))
        c.viewing_user = c.logged_in_user
        c.viewing_user.location = "SRID=4326;POINT(%d %d)" % (lon, lat)
        Session.commit()

        return action_ok(_("Settings saved"))
        #return "Location saved: %s (%s)" % (
        #    request.params.get("location", "[pos]"),
         #   request.params.get("location_name", "[name]"),
        #)
