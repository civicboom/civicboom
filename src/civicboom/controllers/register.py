"""
Registration process can be done in 2 ways:
    1.a) Collect email address and username
        - this can be done from a variaty of sources (e.g widget, webpage or mobile)
        - server creates new user record and sends validation email
    1.b) User forwarded from validation email
        - validates email hash
        - collects password and addtional data
        
    2.a) Janrain
    2.b) additional details
"""

from civicboom.lib.base import *

# Database Objects
from civicboom.model.member            import User, UserLogin

# Database Actions
#from civicboom.lib.database.actions    import follow, accept_assignment
from civicboom.lib.database.get_cached import get_member as _get_member

# Communication & Messages
from civicboom.lib.accounts       import send_verifiy_email, verify_email_hash, validation_url, associate_janrain_account, set_password

# Signin
from civicboom.lib.authentication import signin_user_and_redirect

# Email - to be removed - this was a short term import
from civicboom.lib.communication.email_lib import send_email

# Form Validators
import formencode
from civicboom.lib.form_validators.validator_factory import build_schema
from civicboom.lib.form_validators.registration      import RegisterSchemaEmailUsername, UniqueEmailValidator, UniqueUsernameValidator
from formencode import validators#, htmlfill
from civicboom.lib.form_validators.dict_overlay import validate_dict

from cbutils.misc import random_string, calculate_age

from civicboom.lib.form_validators.base import IsoFormatDateConverter
api_datestr_to_datetime = IsoFormatDateConverter().to_python
#from civicboom.lib.helpers import api_datestr_to_datetime #This is not suffience because some of the DOB's are not in API form. We may need to normaliz this in future

log      = logging.getLogger(__name__)

new_user_prefix = "newuser__"


class RegisterController(BaseController):
    """
    @title Register
    @doc register
    @desc register users of civicboom
    """

    #---------------------------------------------------------------------------
    # Register new user
    #---------------------------------------------------------------------------
    @web
    def new_user(self, id=None, **kwargs):
        """
        Register new user - look at exisiting user record and identify additioinal required fields to complete upload
        """
        registration_template = "/html/web/account/register.mako"
        
        c.new_user = _get_member(id)
        
        # Validate User
        if c.logged_in_persona and c.logged_in_persona == c.new_user: # from janrain login
            pass
        elif verify_email_hash(c.new_user, kwargs.get('hash')): # or from email hash
            c.logged_in_user    = c.new_user #fake logged in user for rendering template
            c.logged_in_persona = c.new_user
        else:
            raise action_error(code=403, message="Unable to verify email hash - it may already have been validated?")
        
        # Build required fields list from current user data - the template will then display these and a custom validator will be created for them
        c.required_fields = ['username','email','password','name','dob']
        if not c.logged_in_persona.id.startswith(new_user_prefix):
            c.required_fields.remove('username')
        if c.logged_in_persona.email or c.logged_in_persona.email_unverified:
            c.required_fields.remove('email')
        if len(c.logged_in_persona.login_details) > 0:
            c.required_fields.remove('password')
        if c.logged_in_persona.config["dob"] != u"":
            c.required_fields.remove('dob')
        
        # If no post data, display the registration form with required fields
        if request.environ['REQUEST_METHOD'] == 'GET':
            return render(registration_template)

        # Build a dynamic validation scema based on these required fields and validate the form
        schema = build_schema(*c.required_fields)
        schema.fields['terms'] = validators.NotEmpty(messages={'missing': 'You must agree to the terms and conditions'}) # In addtion to required fields add the terms checkbox validator
        schema.fields['name']  = validators.NotEmpty(messages={'missing': 'Please give us your full name as you wish it to appear on your profile'})
        schema.fields['help_type'] = formencode.validators.OneOf(['org','ind'], messages={'missing': 'Please select a help type'}) #, if_missing='ind'
        # schema.fields['help_type'] = validators.NotEmpty(messages={'missing': 'Please select a user type'})
        data = {'register':kwargs}
        data = validate_dict(data, schema, dict_to_validate_key='register', template_error='account/register')
        form = data['register']
        
        #try: # Form validation
        #    form = schema.to_python(kwargs) #dict(request.params)
        #except formencode.Invalid as error:  # If the form has errors overlay those errors over the previously rendered form
        #    form_result = error.value
        #    form_errors = error.error_dict or {}
            # htmlfill does not work with HTML5 ... bugger
            # return formencode.htmlfill.render(render(registration_template) , defaults = form_result , errors = form_errors, prefix_error=False)
        
        # If the validator has not forced a page render
        # then the data is fine - save the new user data
        if 'username' in form:
            c.logged_in_persona.id               = form['username']
        if 'name'     in form:
            c.logged_in_persona.name             = form['name']
        if 'dob'      in form:
            c.logged_in_persona.config['dob']    = str(form['dob'])
        if 'email'    in form:
            c.logged_in_persona.email_unverified = form['email']
        if 'password' in form:
            set_password(c.logged_in_persona, form['password'], delay_commit=True)
        c.logged_in_persona.status = "active"
        if form['help_type'] == 'org':
            c.logged_in_persona.extra_fields['help_type'] = form['help_type']
        
        # AllanC - in offline demo mode ensure every user has the maximum user rights
        if config['demo_mode']:
            c.logged_in_persona.account_type = 'corp_plus'
        
        Session.add(c.logged_in_persona) #AllanC - is this needed? Already in session?
        Session.commit()
        
        if c.logged_in_persona.email_unverified:
            send_verifiy_email(c.logged_in_persona)
            set_flash_message(_('Please check your email to validate your email address'))
        
        c.logged_in_persona.send_email(subject=_('Welcome to _site_name'), content_html=render('/email/welcome.mako', extra_vars={'registered_user':c.logged_in_persona}))
        
        # AllanC - Temp email alert for new user
        send_email(config['email.event_alert'], subject='new signup', content_text='%s - %s - %s - %s' % (c.logged_in_persona.id, c.logged_in_persona.name, c.logged_in_persona.email_normalized, form['help_type']))
        
        user_log.info("Registered new user")
        set_flash_message(_("Congratulations, you have successfully signed up to _site_name."))
        # GregM: prompt_aggregate on new user :D
        ##signin_user_and_redirect(c.logged_in_persona, 'registration', prompt_aggregate=True)
        signin_user_and_redirect(c.logged_in_persona, 'registration', redirect_url=url(controller='misc', action='how_to'))
        ##redirect('/')

    @web
    def check_email(self, **kwargs):
        return action_ok(code=200, template="account/check_email")

    #---------------------------------------------------------------------------
    # Register - via email (no janrain)
    #---------------------------------------------------------------------------
    @web
    def email(self, **kwargs):
        """
        POST /register/email: Register a new user via email
        @type action
        @api register 1.0 (WIP)
        
        @param username
        @param email
        @param follow        (optional) a comma separted list of users this registered user will follow on registration
        @param follow_mutual (optional) a comma separted list of users who will follow this user
        
        @return 200 registered ok
        An email with a verification hash is sent
        
        @comment AllanC follow_mutual will not function unless allow_registration_follows is set in user settings for that user
        @comment AllanC GET triggers HTML page
        """
        
        # record the username exactly as given (eg Bob Bobson), the validator
        # will return a valid username (bob-bobson). Have the username exactly
        # as given as their default display name.
        given_username = kwargs.get("username", "")

        # Check the username and email and raise any problems via the flash message session system
        try:
            kwargs = RegisterSchemaEmailUsername().to_python(kwargs) #dict(request.params)
        except formencode.Invalid as error:
            raise action_error(status='invalid', message=error.msg, code=400)
        
        # Create new user
        u = User()
        u.id               = kwargs['username']
        u.email_unverified = kwargs['email']
        u.name             = given_username  # display name will be asked for in step #2. For now, copying username is a good enough space filler
        Session.add(u)
        Session.commit()
        
        # Automatically Follow Users from config and referers from other sites
        follow_username_list = []
        for username_list in [config['setting.username_to_auto_follow_on_signup'], kwargs.get('follow',''), kwargs.get('follow_mutual','')]:
            follow_username_list += username_list.split(',')
        for member in [_get_member(username.strip()) for username in follow_username_list                     ]:
            if member:
                u.follow(member)
        for member in [_get_member(username.strip()) for username in kwargs.get('follow_mutual','').split(',')]:
            if member and member.config['allow_registration_follows']:
                member.follow(u)
        
        # Accept assignment
        if 'accept_assignment' in kwargs:
            log.debug("auto accepting not implemented yet")
            # TODO: Implement
            #assignment = get_assignment(request.params['accept_assignment'])
            #accept_assignment_status = accept_assignment(new_member, assignment)
            #if accept_assignment_status == True:
            #    refered_by_member.send_notification(messages.assignment_accepted(member=new_member, assignment=assignment))
        
        Session.commit()
        
        if config['demo_mode'] and (c.format=='html' or c.format=='redirect'):
            return redirect(validation_url(u, controller='register', action='new_user'))

        user_log.info("Sending verification email to %s (%s)" % (u.id, u.email_unverified))
        # Send email verification link
        send_verifiy_email(u, controller='register', action='new_user', message=_('complete the registration process'))
        
        if c.format in ["html", "redirect"]:
            return redirect(url(controller="register", action="check_email"))
        
        return action_ok(_("Thank you. Please check your email to complete the registration process"))
        
        
#-------------------------------------------------------------------------------
# Regisration Utilitys (for import by other modules)
#-------------------------------------------------------------------------------

def _fetch_avatar(url):
    try:
        import urllib2
        import tempfile
        import cbutils.warehouse as wh
        import Image

        with tempfile.NamedTemporaryFile(suffix=".jpg") as original:
            data = urllib2.urlopen(url).read()
            original.write(data)
            original.flush()
            h = wh.hash_file(original.name)
            wh.copy_to_warehouse(original.name, "avatars-original", h)
            
            with tempfile.NamedTemporaryFile(suffix=".jpg") as processed:
                size = (160, 160)
                im = Image.open(original.name)
                if im.mode != "RGB":
                    im = im.convert("RGB")
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(processed.name, "JPEG")
                wh.copy_to_warehouse(processed.name, "avatars", h)
            return h
    except Exception as e:
        log.exception("Error fetching janrain user's avatar")
        return None


def register_new_janrain_user(profile):
    """
    With a Janrain user dictonary create a new user with whatever data has been provided as best we can
    If additional information is required the account controler will redirect to the register action to ask for additional details
    """
    Session.flush() # AllanC - for some mythical reason the commit below wont function because the database is in an odd state, this flush makes the commit below work, more investigation may be needed or maybe a newer version of SQL alchemy will fix this issue
    
    u = User()
    try:
        u.id               = UniqueUsernameValidator().to_python(profile.get('displayName'))
    except Exception:
        u.id               = UniqueUsernameValidator().to_python(new_user_prefix+random_string())
    
    try:
        u.email            = UniqueEmailValidator().to_python(profile.get('verifiedEmail'))
    except Exception:
        pass
    
    try:
        u.email_unverified = UniqueEmailValidator().to_python(profile.get('email'))
    except Exception:
        pass
    
    u.name          = profile.get('name', dict()).get('formatted')
    u.status        = "pending"
    u.avatar        = _fetch_avatar(profile.get('photo'))
    #u.location      = get_location_from_json(profile.get('address'))
    
    Session.add(u)
    
    #u_login = UserLogin()
    #u_login.user   = u
    #u_login.type   = profile['providerName']
    #u_login.token  = profile['identifier']
    #Session.add(u_login)
    associate_janrain_account(u, profile['providerName'], profile['identifier'])
    
    #Session.commit() # unneeded as associate_janrain_account has a commit in to map accounts
    
    u.config['dob']     = profile.get('birthday') #Config vars? auto commiting?
    u.config['website'] = profile.get('url')
    
    try:
        age = calculate_age(api_datestr_to_datetime(u.config['dob']))
        if age < config['setting.age.min_signup']:
            log.info('janrain dob is lower than min age: %s' % u.config['dob'])
            raise Exception('janrain dob is lower than min age')
    except:
        del u.config['dob']
    
    # Future addition and enhancements
    #   with janrain we could get a list of friends/contnact and automatically follow them?
    #   Could we leverage twitter/facebook OAuth token?
    # Reference - https://rpxnow.com/docs#api_auth_info
    
    return u
