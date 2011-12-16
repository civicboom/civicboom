"""
Base Formencode Validators
"""

# Formencode Imports
import formencode
from formencode import validators



from pylons.i18n.translation import _ # AllanC - unneeded as global _ shoudl now be in use


from cbutils.text import clean_html_markup, strip_html_tags
from cbutils.misc import timedelta_from_str

# Misc Imports
from dateutil.parser import parse as parse_date
import re
import cgi


def x_(s):
    # see lib/base:x_
    return s


class DefaultSchema(formencode.Schema):
    allow_extra_fields  = True
    filter_extra_fields = True

class IntervalValidator(validators.UnicodeString):
    if_empty   = None
    """
    Validate a timedelta inteval form a string
    """
    messages = {
        'empty'         : x_('You must specify an interval'),
        'invalid_format': x_('invalid format: interval should be in json or hour=3,seconds=4 etc'),
    }
    def _to_python(self, value, state):
        timedelta_kwargs = validators.UnicodeString._to_python(self, value, state)
        try:
            value = timedelta_from_str(timedelta_kwargs)
        except Exception as e:
            raise formencode.Invalid(self.message("invalid_format", state), value, state)
        return value

class UnicodeStripHTMLValidator(validators.UnicodeString):
    def _to_python(self, value, state):
        value = validators.UnicodeString._to_python(self, value, state)
        return strip_html_tags(value).strip()


class MemberValidator(validators.FancyValidator):
    not_empty = True
    messages = {
        'empty'     : x_('You must specify a member'),
        'not_member': x_('Not a valid member'),
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
        'not_in_range': x_('location is out of range'),
    }

    def _to_python(self, value, state):
        try:
            value = value.replace(",", " ")
            (lon, lat) = value.split(" ")
            return "SRID=4326;POINT(%f %f)" % (float(lon), float(lat))
        except:
            raise formencode.Invalid(self.message("not_in_range", state), value, state)


class ContentObjectValidator(validators.FancyValidator):
    not_empty = True
    #if_missing = ''
    #if_empty   = ''
    messages = {
        'empty'       : x_('You must specify content'),
        'not_content' : x_('Not valid content'),
        'not_viewable': x_('content not viewable by your user'),
        'not_owner'   : x_('You are not the owner of this piece of content'),
        'not_type'    : x_('This piece of content is not: %(content_type)s')
    }

    def __init__(self, return_object=False, persona_owner=False, content_type=None, *args, **kwargs):
        validators.FancyValidator.__init__(self, *args, **kwargs)
        self.return_object = return_object
        self.persona_owner = persona_owner
        self.content_type  = content_type

    def _to_python(self, value, state):
        from pylons import tmpl_context as c
        from civicboom.lib.database.get_cached import get_content
        content = get_content(value)
        if not content:
            raise formencode.Invalid(self.message("not_content", state), value, state)
        if not content.viewable_by(c.logged_in_persona):
            raise formencode.Invalid(self.message("not_viewable", state), value, state)
        if self.persona_owner and content.creator.id != c.logged_in_persona.id:
            raise formencode.Invalid(self.message("not_owner", state), value, state)
        if self.content_type and content.__type__ != self.content_type:
            raise formencode.Invalid(self.message("not_type", state, content_type=self.content_type), value, state)
        if self.return_object:
            return content
        return content.id



class CleanHTMLValidator(validators.UnicodeString):
    """
    A validator that returns purifyed HTML with only basic A P H? B I UL LI and OL tags (without attrs)
    See cb_lib for more details
    """
    not_empty = False
    strip     = True

    def __init__(self, html='clean_html_markup', *args, **kwargs):
        self.html = html
        return validators.UnicodeString.__init__(self, *args, **kwargs)

    def _to_python(self, value, state):
        value = validators.UnicodeString._to_python(self, value, state)
        if self.html=='clean_html_markup':
            return clean_html_markup(value)
        # AllanC - this is depricated? use UnicodeStripHTML instead
        #if self.html=='strip_html_tags':
        #    return strip_html_tags(value)
        raise Exception('validator not setup correctly')


class ContentTagsValidator(validators.FancyValidator):
    not_empty  = False
    strip      = True
    if_missing = []
    if_empty   = []

    def _to_python(self, value, state):
        from civicboom.lib.database.get_cached import get_tag
        tags_raw = value.split(" ")
        tags     = [get_tag(tag) for tag in tags_raw if tag!=""]
        return tags


class LicenseValidator(validators.FancyValidator):
    not_empty = False
    messages = {
        'empty'      : x_('you must specify a licence type'),
        'not_license': x_('not a valid licence type'),
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


class PrivateContentValidator(validators.StringBool):
    messages = {
        'not_account_type': x_('unable to use private content features without account upgrade'),
    }

    def _to_python(self, value, state):
        value = validators.StringBool._to_python(self, value, state)
        from pylons import tmpl_context as c
        if value and not c.logged_in_persona.has_account_required('plus'):
            raise formencode.Invalid(self.message('not_account_type', state), value, state)
        return value

# AllanC - TODO - can this be merged with the validator above, they are doing the same thing just with a differnt message return
class ModerateResponseValidator(validators.StringBool):
    messages = {
        'not_account_type': x_('unable to use content moderation features without account upgrade'),
    }

    def _to_python(self, value, state):
        value = validators.StringBool._to_python(self, value, state)
        from pylons import tmpl_context as c
        if value and not c.logged_in_persona.has_account_required('plus'):
            raise formencode.Invalid(self.message('not_account_type', state), value, state)
        return value


class CurrentUserPasswordValidator(validators.FancyValidator):
    not_empty    = True
    messages = {
        'empty'     : x_('You must enter your current password'),
        'invalid'   : x_('Invalid password'),
    }

    def _to_python(self, value, state):
        from pylons import tmpl_context as c
        from civicboom.lib.authentication import get_user_and_check_password
        if get_user_and_check_password(c.logged_in_persona.username, value):
            return value
        raise formencode.Invalid(self.message("invalid", state), value, state)


class PasswordValidator(validators.FancyValidator):
    min          = 5
    non_letter   = 0
    letter_regex = re.compile(r'[a-zA-Z]')
    not_empty    = True
    messages = {
        'empty'        : x_('You must enter a password'),
        'too_few'      : x_('Your password must be longer than %(min)i characters'),
        'non_letter'   : x_('You must include at least %(non_letter)i non-letter in your password'),
        'repeated_char': x_('Your password consists of a single character repeated. You may have copy and pasted your password'),
    }

    def _to_python(self, value, state):
        from civicboom.lib.authentication import encode_plain_text_password
        value = value.strip()
        if len(value) < self.min:
            raise formencode.Invalid(self.message("too_few", state, min=self.min), value, state)
        non_letters = self.letter_regex.sub('', value)
        if len(non_letters) < self.non_letter:
            raise formencode.Invalid(self.message("non_letter", state, non_letter=self.non_letter), value, state)

        def check_string_repeated(value):
            first = value[0]
            for i in range(len(value)):
                if value[i] != first:
                    return False
            return True
        if check_string_repeated(value):
            raise formencode.Invalid(self.message("repeated_char", state), value, state)
        
        return encode_plain_text_password(value)


# http://osdir.com/ml/python.formencode/2008-09/msg00003.html
#class IsoFormatDateConverter(validators.DateConverter):
class IsoFormatDateConverter(validators.FancyValidator):
    """
    Like formencode.validators.DateConverter, but accepts ISO 8601 YYYY-mm-dd
    """
    #month_style = 'dd/mm/yyyy'

    def _to_python(self, value, state):
        try:
            value = parse_date(value, dayfirst=True, yearfirst=True)#.strftime("%d/%m/%Y")
        except ValueError:
            raise formencode.Invalid("Invalid date", value, state)
        return value #super(IsoFormatDateConverter, self)._to_python(value, state)


class SetValidator(validators.FancyValidator):
    not_empty    = False
    separator    = ','
    set=[]
    messages = {
        'invalid'   : x_('Some item(s) not in set'),
        'empty'     : x_('Set cannot be empty'),
    }

    def _to_python(self, value, state):
        value = value.strip()
        values = value.split(self.separator)
        if len(values) == 0 and not_empty:
            raise formencode.Invalid(self.message("empty", state), value, state)
        elif len(values) == 0:
            return values
        
        for value in values:
            if not value in self.set:
                raise formencode.Invalid(self.message("invalid", state), value, state)
        return values


class EmptyValidator(validators.FancyValidator):
    messages = {
        'invalid'   : x_('You cannot enter a value here due to other errors'),
    }

    def _to_python(self, value, state):
        if len(value) > 0:
            raise formencode.Invalid(self.message("invalid", state), value, state)
        else:
            return value

class FileTypeValidator(validators.FancyValidator):
    messages = {
        'invalid'   : x_('The file uploaded is not of a valid type, please try a different format.'),
    }
    file_type_re = re.compile('^[-\w\+]+/[-\w\+]+$')

    def _to_python(self, value, state):
        if isinstance(value, cgi.FieldStorage):
            if self.file_type_re.match(value.type) == None:
                raise formencode.Invalid(self.message("invalid", state), value, state)
        return value
