from civicboom.lib.base import *

# Database Objects
from civicboom.model.member            import User, UserLogin

# Database Actions
#from civicboom.lib.database.actions    import follow, accept_assignment
from civicboom.lib.database.get_cached import get_member as _get_member

# Communication & Messages
from civicboom.lib.civicboom_lib       import send_verifiy_email, verify_email_hash, validation_url, associate_janrain_account, set_password

# Signin
from civicboom.lib.authentication import signin_user_and_redirect

# Form Validators
import formencode
from civicboom.lib.form_validators.validator_factory import build_schema
from civicboom.lib.form_validators.registration      import RegisterSchemaEmailUsername, UniqueEmailValidator, UniqueUsernameValidator
from formencode import validators#, htmlfill
from civicboom.lib.form_validators.dict_overlay import validate_dict

from civicboom.lib.misc import random_string

log      = logging.getLogger(__name__)

new_user_prefix = "newuser__"


class RegisterController(BaseController):
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
            abort(403)
        
        # Build required fields list from current user data - the template will then display these and a custom validator will be created for them
        c.required_fields = ['username','email','password','dob']
        if not c.logged_in_persona.username.startswith(new_user_prefix):
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
        
        data = {'register':kwargs}
        data = validate_dict(data, schema, dict_to_validate_key='register', template_error='account/register')
        form = data['register']
        
        #try: # Form validation
        #    form = schema.to_python(kwargs) #dict(request.params)
        #except formencode.Invalid, error:  # If the form has errors overlay those errors over the previously rendered form
        #    form_result = error.value
        #    form_errors = error.error_dict or {}
            # htmlfill does not work with HTML5 ... bugger
            # return formencode.htmlfill.render(render(registration_template) , defaults = form_result , errors = form_errors, prefix_error=False)
        
        # If the validator has not forced a page render
        # then the data is fine - save the new user data
        if 'username' in form: c.logged_in_persona.username         = form['username']
        if 'dob'      in form: c.logged_in_persona.config['dob']    = form['dob']
        if 'email'    in form: c.logged_in_persona.email_unverified = form['email']
        if 'password' in form:
            set_password(c.logged_in_persona, form['password'], delay_commit=True)
        c.logged_in_persona.status = "active"
        
        Session.add(c.logged_in_persona) #AllanC - is this needed? Already in session?
        Session.commit()
        
        if c.logged_in_persona.email_unverified:
            send_verifiy_email(c.logged_in_persona)
            set_flash_message(_('Please check your email to validate your email address'))
        
        c.logged_in_persona.send_email(subject=_('Welcome to _site_name'), content_html=render('/email/welcome.mako'))
        
        user_log.info("Registered new user")
        set_flash_message(_("Congratulations, you have successfully signed up to _site_name."))
        signin_user_and_redirect(c.logged_in_persona, 'registration')
        ##redirect('/')


    #---------------------------------------------------------------------------
    # Register - via email (no janrain)
    #---------------------------------------------------------------------------
    @web
    def email(self, **kwargs):
        """
        Register - via email (no janrain)
        User submits a proposed username and email to this action
        A new skeleton user is created for the user to complete the registration
        An email with a verification hash is sent
        """

        # Check the username and email and raise any problems via the flash message session system
        try:
            kwargs = RegisterSchemaEmailUsername().to_python(kwargs) #dict(request.params)
        except formencode.Invalid, error:
            raise action_error(status='invalid', message=error.msg, code=400)
        
        # Create new user
        u = User()
        u.username         = kwargs['username']
        u.email_unverified = kwargs['email']
        Session.add(u)
        Session.commit()
        
        # Automatically Follow Users from config
        for member in [_get_member(username.strip()) for username in config['setting.username_to_auto_follow_on_signup'].split(',')]:
            if member:
                u.follow(member)
        #user_to_auto_follow_on_signup = _get_member(config['setting.username_to_auto_follow_on_signup'])
        #if user_to_auto_follow_on_signup:
        #    u.follow(user_to_auto_follow_on_signup)
        
        # Follow the refered_by user if they exisits
        if 'refered_by' in kwargs:
            refered_by = _get_member(kwargs['refered_by'])
            if refered_by and u.follow(refered_by) == True:
                log.debug("refered_by auto follow message generation not implmented yet")
                #refered_by.send_message(messages.followed_on_signup(member=u)
        
        # Accept assignment
        if 'accept_assignment' in kwargs:
            log.debug("auto accepting not implemented yet")
            # TODO: Implement
            #assignment = get_assignment(request.params['accept_assignment'])
            #accept_assignment_status = accept_assignment(new_member, assignment)
            #if accept_assignment_status == True:
            #    refered_by_member.send_message(messages.assignment_accepted(member=new_member, assignment=assignment))
        
        Session.commit()
        
        if config['demo_mode'] and (c.format=='html' or c.format=='redirect'):
            return redirect(validation_url(u, controller='register', action='new_user'))

        user_log.info("Sending verification email")
        # Send email verification link
        send_verifiy_email(u, controller='register', action='new_user', message=_('complete the registration process'))
        
        return action_ok(_("Thank you. Please check your email to complete the registration process"))
        
        
#-------------------------------------------------------------------------------
# Regisration Utilitys (for import by other modules)
#-------------------------------------------------------------------------------

def register_new_janrain_user(profile):
    """
    With a Janrain user dictonary create a new user with whatever data has been provided as best we can
    If additional information is required the account controler will redirect to the register action to ask for additional details
    """
    Session.flush() # AllanC - for some mythical reason the commit below wont function because the database is in an odd state, this flush makes the commit below work, more investigation may be needed or maybe a newer version of SQL alchemy will fix this issue
    
    u = User()
    try   : u.username         = UniqueUsernameValidator().to_python(profile.get('displayName'))
    except: u.username         = UniqueUsernameValidator().to_python(new_user_prefix+random_string())
    
    try   : u.email            = UniqueEmailValidator().to_python(profile.get('verifiedEmail'))
    except: pass
    
    try   : u.email_unverified = UniqueEmailValidator().to_python(profile.get('email'))
    except: pass
    
    u.name          = profile.get('name', dict()).get('formatted')
    u.status        = "pending"
    #u.avatar        = profile.get('photo') # AllanC - disabled because we cant guarantee https - we need our server to auto copy this and upload it to our own S3 store
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

    
    # Future addition and enhancements
    #   with janrain we could get a list of friends/contnact and automatically follow them?
    #   Could we leverage twitter/facebook OAuth token?
    # Reference - https://rpxnow.com/docs#api_auth_info
    
    return u
