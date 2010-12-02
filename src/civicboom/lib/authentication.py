"""
Tools used for Authentication of users
"""

# Pylons imports
from civicboom.lib.base import *
from civicboom.lib.database.get_cached import get_membership

# Civicboom imports
from civicboom.model      import User, UserLogin, Member
from civicboom.model.meta import Session

from civicboom.lib.web     import session_set, session_get, session_remove, multidict_to_dict, current_url
from civicboom.lib.helpers import url_from_widget

# Other imports
from sqlalchemy.orm import join

# Pyhton package imports
import hashlib
from decorator import decorator
import json

# Logging
import logging
log = logging.getLogger(__name__)
user_log = logging.getLogger("user")



#-------------------------------------------------------------------------------
# Standard Tools
#-------------------------------------------------------------------------------

def encode_plain_text_password(password):
    return hashlib.sha1(password).hexdigest()

def get_user_and_check_password(username, password):
    """
    Called by account controller and/or AuthKit valid_password to return a user from local db
    """
    try:
        q = Session.query(User).select_from(join(User, UserLogin, User.login_details))
        q = q.filter(User.username   == username  )
        q = q.filter(User.status     == 'active'  )
        q = q.filter(UserLogin.type  == 'password')
        q = q.filter(UserLogin.token == encode_plain_text_password(password))
        q = q.one()
        return q
    except:
        return None


def get_user_from_openid_identifyer(identifyer):
    """
    Called by account controller to return a user from our db from an openid identifyer
    """
    try:
        q = Session.query(User).select_from(join(User, UserLogin, User.login_details))
        #q = q.filter(User.status     == 'active'  ) # the base controler checks for pending status and redirects to login page accordingly
        q = q.filter(UserLogin.token == identifyer )
        q = q.one()
        return q
    except:
        return None



#-------------------------------------------------------------------------------
# AuthKit
#-------------------------------------------------------------------------------
# This section could be block remmed or removed and the rest of the site will still function as authorise is overwritten in the Custom Login Section

def is_valid_user(u):
    return u


#-------------------------------------------------------------------------------
# Custom Authentication
#-------------------------------------------------------------------------------

# Todo - look into how session is verifyed - http://pylonshq.com/docs/en/1.0/sessions/#using-session-in-secure-forms
#        what is the secure form setting for?

# AllanC - these should look at config['ssl']
#          do we always want logged_in users to always use HTTPS?
#          what about the https() decorator on signin paying attention to config['ssl']
protocol_for_login   = "https"
protocol_after_login = "https"
if   config['ssl'] == 'default_when_logged_in':
    pass
elif config['ssl'] == 'disabled':
    protocol_for_login   = "http"
    protocol_after_login = "http"
elif config['ssl'] == 'login_process_only':
    protocol_after_login = "http"
elif config['ssl'] == 'enforce_when_logged_in':
    # TODO:
    # AllanC - this should be equivelent of putting https on the top of every method call, we force logged in users to use https by forcefully redirecting them
    log.info('config[ssl]=enforce_when_logged_in is set and is currenlty not implemented')
    

def authorize(authenticator):
    """
    Check if logged in user has been set
    If not sends you to a login page
    Once you log in, it sends you back to the original url call.
    """
    @decorator
    def wrapper(_target, *args, **kwargs):

        # CHECK Loggin in
        if authenticator(c.logged_in_user):
            # Reinstate any session encoded POST data if this is the first page since the login_redirect
            if not session_get('login_redirect'):
                json_post = session_remove('login_redirect_post')
                if json_post:
                    kwargs.update(json.loads(json_post))
                    # AllanC - now unneeded - we dont need a user confirm as we can overlay post data over kwargs
                    #post_overlay = json.loads(json_post)
                    #c.target_url = current_url()
                    #c.post_values = post_overlay
                    #from pylons.templating import render_mako as render # FIXME: how is this not imported from base? :/
                    #return render("web/misc/confirmpost.mako")

            # Make original method call
            result = _target(*args, **kwargs)
            return result

        # ELSE Unauthorised
        else:
            # If request was a browser - prompt for login
            if c.format == "redirect":
                #TODO
                raise action_error(message="implement me, redirect authentication needs session handling of http_referer")
            if c.format == "html":
                redirect_url = current_url(protocol=protocol_after_login)
                session_set('login_redirect'     , redirect_url, 60 * 10) # save timestamp with this url, expire after 5 min, if they do not complete the login process
                # save the the session POST data to be reinstated after the redirect
                if request.POST:
                    session_set('login_redirect_post', json.dumps(multidict_to_dict(request.POST)), 60 * 10) # save timestamp with this url, expire after 5 min, if they do not complete the login process
                return redirect(url_from_widget(controller='account', action='signin', protocol=protocol_for_login)) #This uses the from_widget url call to ensure that widget actions preserve the widget env

            # If API request - error unauthorised
            else:
                raise action_error(message="unauthorised", code=403) #Error to be formared by auto_formatter

    return wrapper

def login_redirector():
    """
    If this method returns (rather than aborting with a redirect) then there is no login_redirector
    """
    login_redirect = session_remove('login_redirect')
    if login_redirect:
        return redirect(login_redirect)


def signin_user(user, login_provider=None):
    """
    Perform the sigin for a user
    """
    user_log.info("logged in with %s" % login_provider)   # Log user login
    #session_set('user_id' , user.id      ) # Set server session variable to user.id
    session_set('username', user.username) # Set server session username so we know the actual user regardless of persona
    response.set_cookie(
        "civicboom_logged_in", "True",
        int(config["beaker.session.timeout"]),
        secure=(request.environ['wsgi.url_scheme']=="https"),
        httponly=True
    )

def signin_user_and_redirect(user, login_provider=None):
    """
    Perform the sigin for a user
    """
    signin_user(user, login_provider)
    
    if 'popup_close' in request.params:
        # Redirect to close the login frame, but keep the login_redirector for a separte call later
        return redirect(url(controller='misc', action='close_popup'))

    # Redirect them back to where they were going if a redirect was set
    login_redirector()

    # If no redirect send them to private profile
    return redirect(url(controller="profile", action="index"))
    
def signout_user(user):
    user_log.info("logged out")
    session.clear()
    response.delete_cookie("civicboom_logged_in")
    #session.save()
    #flash_message("Successfully signed out!")

def set_persona(persona):
    persona = get_member(persona)
    if (persona == c.logged_in_user):        
        # If trying to fall back to self login then remove persona selection
        session_remove('username_persona')
        return True
    else:
        membership = get_membership(persona, c.logged_in_user)
        if not membership:
            raise action_error(_('not a member of this group'), code=403)
        if membership.status != "active":
            raise action_error(_('not an active member of this group'), code=403)
        #if isintance(persona, Member):
        #    persona = persona.username
        session_set('username_persona', persona.username)
        return True
    return False
