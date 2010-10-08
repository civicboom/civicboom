"""
Base Formencode Validators
"""

# Formencode Imports
import formencode
from formencode import validators, compound

from pylons.i18n.translation import _


from pylons import tmpl_context as c #for current user password validator

from civicboom.lib.authentication import encode_plain_text_password, get_user_and_check_password

from civicboom.lib.form_validators.registration import UniqueUsernameValidator

# Misc Imports
import datetime
import hashlib
import re


class DefaultSchema(formencode.Schema):
    allow_extra_fields  = True
    filter_extra_fields = True



class CurrentUserPasswordValidator(validators.FancyValidator):
    not_empty    = True
    messages = {
        'empty'     : _('You must enter your current password'),
        'invalid'   : _('Invalid password'),
    }
    def _to_python(self, value, state):
        if get_user_and_check_password(c.logged_in_user.username, value):
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

