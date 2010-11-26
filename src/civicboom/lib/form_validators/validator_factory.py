from base         import DefaultSchema, PasswordValidator
from registration import MinimumAgeValidator, ReCaptchaValidator, UniqueEmailValidator, UniqueUsernameValidator
from formencode.validators import FieldsMatch, UnicodeString

#-------------------------------------------------------------------------------
# Schema Factory
#-------------------------------------------------------------------------------

class DynamicSchema(DefaultSchema):
    filter_extra_fields = True
    allow_extra_fields  = True


def build_schema(*args, **kargs):
    """
    Given a list of strings will attach best match validator to them
    Given a set of kargs win the form of string:validator will create a new dynamic validator
    """
    schema = DynamicSchema()
    schema.chained_validators = []
    if kargs:
        for key in kargs:
            schema.fields[key] = kargs[key]
    elif args:
        for field in args:
            if field=='username': schema.fields[field] = UniqueUsernameValidator(not_empty=True)
            if field=='email'   : schema.fields[field] = UniqueEmailValidator(not_empty=True)
            if field=='dob'     : schema.fields[field] = MinimumAgeValidator(not_empty=True)
            if field=='password':
                schema.fields[field]                = PasswordValidator()
                schema.fields['password_confirm']   = PasswordValidator()
                from pylons import request
                schema.chained_validators.append(FieldsMatch('password', 'password_confirm'))

                schema.fields['recaptcha_challenge_field'] = UnicodeString(not_empty=True)
                schema.fields['recaptcha_response_field']  = UnicodeString(not_empty=True)
                schema.chained_validators.append(ReCaptchaValidator(request.environ['REMOTE_ADDR']))
                #setattr(schema, 'chained_validators', [FieldsMatch('password', 'password_confirm'),
                                                       #ReCaptchaValidator(request.environ['REMOTE_ADDR']),
                #                                      ])
    return schema
