import formencode
from formencode import validators, compound

from base import DefaultSchema, UniqueUsernameValidator, UniqueEmailValidator





class RegisterSchemaEmailUsername(DefaultSchema):
  username  = UniqueUsernameValidator(not_empty=True)
  email     = UniqueEmailValidator   (not_empty=True, resolve_domain=True)

