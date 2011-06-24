from base         import DefaultSchema, PasswordValidator
from registration import MinimumAgeValidator, ReCaptchaValidator, UniqueEmailValidator, UniqueUsernameValidator
from formencode.validators import FieldsMatch, UnicodeString
from formencode.api import Validator

from pylons import config


#-------------------------------------------------------------------------------
# Schema Factory
#-------------------------------------------------------------------------------

class DynamicSchema(DefaultSchema):
    filter_extra_fields = True
    allow_extra_fields  = True


def build_schema(*args, **kwargs):
    """
    Given a list of strings will attach best match validator to them
    Given a set of kargs win the form of string:validator will create a new dynamic validator
    """
    schema = DynamicSchema()
    schema.chained_validators = []
    if kwargs:
        for key in kwargs:
            if isinstance(kwargs[key], Validator):
                schema.fields[key] = kwargs[key]
    elif args:
        for field in args:
            if field=='username':
                schema.fields[field] = UniqueUsernameValidator(not_empty=True)
            if field=='email':
                schema.fields[field] = UniqueEmailValidator(not_empty=True)
            if field=='dob':
                schema.fields[field] = MinimumAgeValidator(not_empty=True)
            if field=='password':
                schema.fields[field]                = PasswordValidator()
                schema.fields['password_confirm']   = PasswordValidator()
                from pylons import request
                schema.chained_validators.append(FieldsMatch('password', 'password_confirm'))
                
                if config['test_mode'] or not config['online']: # If in test mode we should bypass captcha validation
                    pass
                else:
                    schema.fields['recaptcha_challenge_field'] = UnicodeString(not_empty=True)
                    schema.fields['recaptcha_response_field']  = UnicodeString(not_empty=True)
                    schema.chained_validators.append(ReCaptchaValidator(request.environ['REMOTE_ADDR']))
                    
            #setattr(schema, 'chained_validators', [FieldsMatch('password', 'password_confirm'),
                                                   #ReCaptchaValidator(request.environ['REMOTE_ADDR']),
            #                                      ])
    return schema
