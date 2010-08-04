"""
Base Formencode Validators
"""

# Formencode Imports
import formencode
from formencode import validators, compound

# Database Objects
from civicboom.model.meta              import Session
from civicboom.model.member            import User, Member

# Other
from civicboom.lib.misc           import calculateAge
from civicboom.lib.authentication import encode_plain_text_password

# Misc Imports
import datetime
import hashlib
import re


class DefaultSchema(formencode.Schema):
    allow_extra_fields  = True
    filter_extra_fields = True


class MinimumAgeValidator(validators.FancyValidator):
    """Checks that date is ok and doesn't allow under 16"""
    age_min = 16
    def _to_python(self, value, state):
         try:
             date = datetime.datetime.strptime(value, '%d/%m/%Y')
         except exceptions.ValueError:
              raise formencode.Invalid("Please enter your date of birth with the format DD/MM/YYYY", value, state)
         if calculateAge(date) < self.age_min:
              raise formencode.Invalid(_("Sorry, you have to be over %d to use this site") % self.age_min, value, state)
         return date

class PasswordValidator(validators.FancyValidator):
    min          = 5
    non_letter   = 0
    letter_regex = re.compile(r'[a-zA-Z]')
    not_empty    = True
    messages = {
        'empty'     : 'You must enter a password',
        'too_few'   : 'Your password must be longer than %(min)i characters',
        'non_letter': 'You must include at least %(non_letter)i non-letter in your password',
        }
    def _to_python(self, value, state):
        value = value.strip()
        if len(value) < self.min:
            raise formencode.Invalid(self.message("too_few", state, min=self.min), value, state)
        non_letters = self.letter_regex.sub('', value)
        if len(non_letters) < self.non_letter:
            raise formencode.Invalid(self.message("non_letter", state, non_letter=self.non_letter), value, state)
        return encode_plain_text_password(value)

class UniqueUsernameValidator(validators.FancyValidator):
    min =  4
    max = 32
    messages = {
        'too_few'       : 'Your username must be longer than %(min)i characters',
        'too_long'      : 'Your username must be shorter than %(max)i characters',
        'username_taken': 'The username %(name)s is no longer available, please try a different one'
        }
    def _to_python(self, value, state):
        value = value.strip()
        # TODO: Strip or alert any characters that make it non URL safe
        if len(value) <= self.min:
            raise formencode.Invalid(self.message("too_few", state, min=self.min), value, state)
        if len(value) >= self.max:
            raise formencode.Invalid(self.message("too_long", state, max=self.max), value, state)
        if Session.query(Member).filter(Member.username==value).count() > 0:
            raise formencode.Invalid(self.message("username_taken", state, name=value), value, state)
        return value

class UniqueEmailValidator(validators.Email):
    def _to_python(self, value, state):
        if Session.query(User).filter(User.email==value).count() > 0:
            raise formencode.Invalid('This email address is already registered with us. Please use a different address, or retrieve your password using the password recovery link.', value, state)
        return value


#-------------------------------------------------------------------------------
# Schema Factory
#-------------------------------------------------------------------------------

class DynamicSchema(DefaultSchema):
    pass

def build_schema(*args, **kargs):
    """
    Given a list of strings will attach e best match validator to them
    Given a set of kargs win the form of string:validator will create a new dynamic validator
    """
    schema = DynamicSchema()
    if kargs:
        for key in kargs:
            setattr(schema, key, kargs[key])
    elif args:
        for field in args:
            if field=='username': setattr(schema, field, UniqueUsernameValidator())
            if field=='email'   : setattr(schema, field, UniqueEmailValidator()   )
            if field=='dob'     : setattr(schema, field, MinimumAgeValidator()    )
            if field=='password': setattr(schema, field, PasswordValidator()      )
    return schema