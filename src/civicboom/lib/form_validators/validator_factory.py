from base         import DefaultSchema, PasswordValidator
from registration import MinimumAgeValidator, ReCaptchaValidator, UniqueEmailValidator, UniqueUsernameValidator
from formencode.validators import FieldsMatch

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
            if field=='username': schema.fields[field] = UniqueUsernameValidator()
            if field=='email'   : schema.fields[field] = UniqueEmailValidator()
            if field=='dob'     : schema.fields[field] = MinimumAgeValidator()
            if field=='password':
                schema.fields[field]                = PasswordValidator()
                schema.fields['password_confirm']   = PasswordValidator()
                from pylons import request
                setattr(schema, 'chained_validators', [FieldsMatch('password', 'password_confirm'),
                                                       #ReCaptchaValidator(request.environ['REMOTE_ADDR']),
                                                      ])
    return schema
