from civicboom.lib.base import BaseController, c, render, request, url, app_globals, _, flash_message, config, abort, action_redirector, redirect

import formencode

# Database Objects
from civicboom.model.member            import User, UserLogin
from civicboom.model.meta              import Session

# Database Actions
from civicboom.lib.database.get_cached import get_user
from civicboom.lib.database.actions    import follow, accept_assignment

# Communication & Messages
from   civicboom.lib.communication.email             import send_email
#import civicboom.lib.communication.messages as messages

# Form Validators
from civicboom.lib.form_validators.validator_factory import build_schema
from civicboom.lib.form_validators.registration      import RegisterSchemaEmailUsername, UniqueEmailValidator, UniqueUsernameValidator
from formencode import validators, htmlfill

from civicboom.lib.misc import random_string

import logging
log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")

new_user_prefix = "newuser"

class RegisterController(BaseController):
    """
    Registration process can be done in 2 ways:
        1.a) Collect email address and username
            - this can be done from a variaty of sources (e.g widget, webpage or mobile)
            - server creates new reporter record and sends validation email
        1.b) User forwarded from validation email
            - validates email hash
            - collects password and addtional data
            
        2.a) Janrain
        2.b) additional details
    """

    #---------------------------------------------------------------------------
    # Register new user
    #---------------------------------------------------------------------------    
    def new_user(self, id=None):
        """
        Register new user - look at exisiting user record and identify additioinal required fields to complete upload
        """
        registration_template = "/web/account/register.mako"
        
        c.new_user = get_user(id)
        
        # Validate User
        if c.logged_in_user and c.logged_in_user == c.new_user: # from janrain login
            pass
        elif 'hash' in request.params and c.new_user.hash() == request.params['hash']: # or from email hash
            c.logged_in_user = c.new_user
        else:
            abort(401)
        
        # Build required fields list from current user data - the template will then display these and a custom validator will be created for them
        c.required_fields = ['username','email','password','dob']
        if not c.logged_in_user.username.startswith(new_user_prefix): c.required_fields.remove('username')
        if c.logged_in_user.email != u""                            : c.required_fields.remove('email')
        if len(c.logged_in_user.login_details) > 0                  : c.required_fields.remove('password')
        if c.logged_in_user.config["dob"] != u""                    : c.required_fields.remove('dob')
        
        # If no post data, display the registration form with required fields
        if request.environ['REQUEST_METHOD'] == 'GET':
            return render(registration_template)
        
        try: # Form validation
            # Build a dynamic validation scema based on these required fields and validate the form
            schema = build_schema(*c.required_fields)
            schema.fields['terms'] = validators.NotEmpty(messages={'missing': 'You must agree to the terms and conditions'}) # In addtion to required fields add the terms checkbox validator
            form = schema.to_python(dict(request.params))
        except formencode.Invalid, error:  # If the form has errors overlay those errors over the previously rendered form
            form_result = error.value
            #try: del form_result['recaptcha_challenge_field']
            #except: pass
            form_errors = error.error_dict or {}
            print form_errors
            return formencode.htmlfill.render(render(registration_template), defaults=form_result, errors=form_errors, prefix_error=False)
        
        # If the validator has not forced a page render
        # then the data is fine - save the new user data
        if 'username' in form: c.logged_in_user.username      = form['username']
        if 'email'    in form: c.logged_in_user.email         = form['email']
        if 'dob'      in form: c.logged_in_user.config['dob'] = form['dob']
        if 'password' in form:
            u_login = UserLogin()
            u_login.user   = c.logged_in_user()
            u_login.type   = 'password'
            u_login.token  = form['password']
            Session.add(u_login)
        c.logged_in_user.status = "active"
        
        Session.add(c.logged_in_user) #Already in session?
        Session.commit()
        
        flash_message(_("Congratulations, you have successfully signed up to _site_name."))
        redirect('/')


    #---------------------------------------------------------------------------
    # Register - via email (no janrain)
    #---------------------------------------------------------------------------
    @action_redirector()
    def email(self):
        """
        Register - via email (no janrain)
        User submits a proposed username and email to this action
        A new skeleton user is created for the user to complete the registration
        An email with a verification hash is sent
        """
        
        # Check the username and email and raise any problems via the flash message session system
        try:
            form = RegisterSchemaEmailUsername().to_python(dict(request.params))
        except formencode.Invalid, error:
            return unicode(error)
        
        # Create new user
        u = User()
        u.username  = form['username']
        u.email     = form['email']
        Session.add(u)
        Session.commit()
        
        # Automatically Follow Civicboom
        follow(get_user('civicboom'), u)
        
        # Follow the refered_by user if they exisits
        if 'refered_by' in request.params:
            refered_by = get_user(request.params['refered_by'])
            if follow(refered_by, u) == True:
                log.debug("message generation not implmented yet")
                #refered_by.send_message(messages.followed_on_signup(reporter=u)
        
        # Accept assignment
        if 'accept_assignment' in request.params:
            log.debug("auto accepting not implemented yet")
            # TODO: Implement
            #assignment = get_assignment(request.params['accept_assignment'])
            #accept_assignment_status = accept_assignment(new_reporter, assignment)
            #if accept_assignment_status == True:
            #    refered_by_reporter.send_message(messages.assignment_accepted(reporter=new_reporter, assignment=assignment))
        
        Session.commit()
        
        # Send email verification link
        Session.refresh(u) #Needed for make_hash below becaususe the object must be persistant
        validation_link = url(controller='register', action='new_user', id=u.id, host=app_globals.site_host, hash=u.hash())
        message         = _('Please complete the registration process by clicking on, or copying the following link into your browser: %s') % (validation_link)
        send_email(u, subject='verify e-mail address', content_text=message)
        
        return _("Thank you. Please check your email to complete the registration process")
        
        
#-------------------------------------------------------------------------------
# Regisration Utilitys (for import by other modules)
#-------------------------------------------------------------------------------

def register_new_janrain_user(profile):
    """
    With a Janrain user dictonary create a new user with whatever data has been provided as best we can
    If additional information is required the account controler will redirect to the register action to ask for additional details
    """
    u = User()
    try   : u.username = UniqueUsernameValidator().to_python(profile.get('displayName'))
    except: u.username = unicode(new_user_prefix+random_string())
    try   : u.email    = UniqueEmailValidator().to_python(profile.get('verifiedEmail') or profile.get('email'))
    except: pass
    u.name          = profile.get('name').get('formatted')
    u.avatar        = profile.get('photo')
    u.webpage       = profile.get('url')
    u.status        = "pending"
    #u.location      = get_location_from_json(profile.get('address'))
    
    u_login = UserLogin()
    u_login.user   = u
    u_login.type   = profile['providerName']
    u_login.token  = profile['identifier']

    Session.add(u)
    Session.add(u_login)
    Session.commit()
    
    u.config['dob'] = profile.get('birthday') #Config vars? auto commiting?
    #u.config['url']  = profile.get('url')
    
    # Future addition and enhancements
    #   with janrain we could get a list of friends/contnact and automatically follow them?
    #   Could we leverage twitter/facebook OAuth token?
    # Reference - https://rpxnow.com/docs#api_auth_info
    
    return u