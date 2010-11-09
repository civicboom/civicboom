"""
Base Formencode Validators
"""

# Formencode Imports
import formencode
from formencode import validators, compound

from pylons.i18n.translation import _


from pylons import tmpl_context as c #for current user password validator

from civicboom.lib.authentication import encode_plain_text_password, get_user_and_check_password


# Misc Imports
import datetime
import hashlib
import re


class DefaultSchema(formencode.Schema):
    allow_extra_fields  = True
    filter_extra_fields = True


class MemberValidator(validators.FancyValidator):
    not_empty = True
    messages = {
        'empty'     : _('You must specify a member'),
        'not_member': _('Not a valid member'),
    }
    def __init__(self, return_object=False, *args, **kwargs):
        validators.FancyValidator.__init__(self, *args, **kwargs)
        self.return_object = return_object
    def _to_python(self, value, state):
        from civicboom.lib.database.get_cached import get_member
        member = get_member(value)
        if not member:
            raise formencode.Invalid(self.message("not_member", state), value, state)
        if self.return_object:
            return member
        return member.id
        


class LocationValidator(validators.FancyValidator):
    not_empty = True
    strip     = True
    messages = {
        'not_in_range': _('location is out of range'),
    }
    def _to_python(self, value, state):
        try:
            (lon, lat) = value.split(" ")
            return "SRID=4326;POINT(%f %f)" % (float(lon), float(lat))
        except:
            return formencode.Invalid(self.message("not_in_range", state), value, state)



class ContentObjectValidator(validators.FancyValidator):
    not_empty = True
    messages = {
        'empty'       : _('You must specify content'),
        'not_member'  : _('Not valid content'),
        'not_viewable': _('content not viewable by your user'),
    }
    def __init__(self, return_object=False, *args, **kwargs):
        validators.FancyValidator.__init__(self, *args, **kwargs)
        self.return_object = return_object
    def _to_python(self, value, state):
        from pylons import tmpl_context as c
        from civicboom.lib.database.get_cached import get_content
        content = get_content(value)
        if not content:
            raise formencode.Invalid(self.message("not_content", state), value, state)
        if not content.viewable_by(c.logged_in_persona):
            raise formencode.Invalid(self.message("not_viewable", state), value, state)
        if self.return_object:
            return content
        return content.id



class ContentUnicodeValidator(validators.UnicodeString):
    not_empty = False
    strip     = True
    def _to_python(self, value, state):
        value = validators.UnicodeString._to_python(self, value, state)
        from civicboom.lib.text import clean_html_markup
        return clean_html_markup(value)


class ContentTagsValidator(validators.FancyValidator):
    not_empty = False
    strip     = True
    def _to_python(self, value, state):
        from civicboom.lib.database.get_cached import get_tag        
        tags_raw = value.split(" ")
        tags     = [get_tag(tag) for tag in tags_raw if tag!=""]
        return tags

class LicenseValidator(validators.FancyValidator):
    not_empty = False
    messages = {
        'empty'      : _('you must specify a licence type'),
        'not_license': _('not a valid licence type'),
    }
    def __init__(self, return_object=False, *args, **kwargs):
        validators.FancyValidator.__init__(self, *args, **kwargs)
        self.return_object = return_object
    def _to_python(self, value, state):
        from civicboom.lib.database.get_cached import get_license
        license = get_license(value)
        if not license:
            raise formencode.Invalid(self.message("not_license", state), value, state)
        if self.return_object:
            return license
        return license.id


class CurrentUserPasswordValidator(validators.FancyValidator):
    not_empty    = True
    messages = {
        'empty'     : _('You must enter your current password'),
        'invalid'   : _('Invalid password'),
    }
    def _to_python(self, value, state):
        if get_user_and_check_password(c.logged_in_persona.username, value):
            return value
        raise formencode.Invalid(self.message("invalid", state), value, state)


class PasswordValidator(validators.FancyValidator):
    min          = 5
    non_letter   = 0
    letter_regex = re.compile(r'[a-zA-Z]')
    not_empty    = True
    messages = {
        'empty'     : _('You must enter a password'),
        'too_few'   : _('Your password must be longer than %(min)i characters'),
        'non_letter': _('You must include at least %(non_letter)i non-letter in your password'),
        }
    def _to_python(self, value, state):
        value = value.strip()
        if len(value) < self.min:
            raise formencode.Invalid(self.message("too_few", state, min=self.min), value, state)
        non_letters = self.letter_regex.sub('', value)
        if len(non_letters) < self.non_letter:
            raise formencode.Invalid(self.message("non_letter", state, non_letter=self.non_letter), value, state)
        return encode_plain_text_password(value)

