"""
REST Settings Actions controler

This controller reflects all calls to it's methods to the settings/panel action, for example:
settings/general is sent here, which then in turn returns what would be settings/panel?panel=general
(The former is preferred to keep URLs clean, however both are accepted!)
"""

from civicboom.lib.base import *

from civicboom.controllers.settings import SettingsController

log = logging.getLogger(__name__)


class SettingActionsController(SettingsController):
    """
    Settings Actions and lists relating to an item of content
    
    This reflects calls back to SettingsController.panel to allow for:
    /settings/me/location
    /settings/me/general
    etc.
    """
    def __getattribute__(self,name):
        attr = None
        try:
            attr = SettingsController.__getattribute__(self, name)
        except:
            pass
        if attr:
            return attr
        else:
            c.controller = 'settings'
            return SettingsController.__getattribute__(self, 'panel') #.panel(self, *args, **kwargs)x