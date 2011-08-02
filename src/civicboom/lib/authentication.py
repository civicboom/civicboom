"""
Tools used for Authentication of users
"""

# Pylons imports
from pylons import session # needed for invalidating the session
from civicboom.lib.base import *
from civicboom.lib.database.get_cached import get_membership, get_member #note get_member should override base:get_member

from pylons.i18n import _ #WHY THE *** IS THIS NEEDED!! .. it's part of lib.base above?! but without it, it's not imported

# Civicboom imports
from civicboom.model      import User, UserLogin, GroupMembership
from civicboom.model.meta import Session
from civicboom.model.member import lowest_role, has_role_required

from civicboom.lib.web     import multidict_to_dict, cookie_set, cookie_delete

from cbutils.misc import make_username


#, current_url, current_referer, 
#from civicboom.lib.helpers import url_from_widget


# Other imports
from sqlalchemy import or_, and_
from sqlalchemy.orm import join

# Pyhton package imports
import hashlib
from decorator import decorator
import json
from urllib import quote_plus, unquote_plus

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
        q = q.filter(User.username   == make_username(username))
        q = q.filter(User.status     == 'active'  )
        q = q.filter(UserLogin.type  == 'password')
        q = q.filter(UserLogin.token == encode_plain_text_password(password))
        q = q.one()
        return q
    except:
        # AllanC - Added fallback to search for email as some users get confised as to how to identify themselfs
        #          emails are not indexed? performance? using this should be safe as our username policy prohibits '@' and '.'
        try:
            q = Session.query(User).select_from(join(User, UserLogin, User.login_details))
            q = q.filter(User.email      == username  )
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

@decorator
def authorize(_target, *args, **kwargs):
    """
    Check if logged in user has been set
    If not sends you to a login page
    Once you log in, it sends you back to the original url call.
    """
    # CHECK Loggin in
    if c.logged_in_user:
        # Reinstate any session encoded POST data if this is the first page since the login_redirect
        if session_get('login_redirect'):
            json_post = session_remove('login_redirect_action')
            if json_post:
                kwargs.update(json.loads(unquote_plus(json_post)))
                # This will fail the auth_token as a new session will have been created and it will ask the user again if they want to perform the action
            
        # Make original method call
        result = _target(*args, **kwargs)
        return result

    # ELSE: not logged in
    else:
        login_expire_time = config['setting.session.login_expire_time']

        # If request was a browser - prompt for login
            #raise action_error(message="implement me, redirect authentication needs session handling of http_referer")
        if c.format == "redirect":
            session_set('login_action_referer', current_referer(), login_expire_time)
            # The redirect auto formater looked for this and redirects as appropriate
        if c.format == "html" or c.format == "redirect":
            login_redirect_url = current_url()
            if 'signout' in login_redirect_url: ## AllanC - bugfix - impaticent people who click signout beofre the page is loaded, dont allow signout as an actions!!
                login_redirect_url = None
            if login_redirect_url:
                # save the the session POST data to be reinstated after the redirect
                login_redirect_action = None
                if request.POST:
                    try:
                        login_redirect_action = json.dumps(multidict_to_dict(request.POST))
                    except:
                        set_flash_message(_('error saving POST operation, please login and try the action again. If the problem persists please contact us'))
                        log.error(        _('POST was unable to encode to put in session as the POST has file data encoded in it'))
                else:
                    login_redirect_action = json.dumps(dict())
                if login_redirect_action:
                    login_redirect_action = quote_plus(login_redirect_action)
                    session_set('login_redirect'       , login_redirect_url    , login_expire_time) # save timestamp with this url, expire after x min, if they do not complete the login process
                    session_set('login_redirect_action', login_redirect_action , login_expire_time)
            return redirect(url(controller='account', action='signin')) #This uses the from_widget url call to ensure that widget actions preserve the widget env
        
        # If API request - error unauthorised
        else:
            raise action_error(message="unauthorised", code=403) #Error to be formared by auto_formatter


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
    # Copy old session data
    session_old = {}
    for key, value in session.iteritems():
        session_old[key] = value
        #log.debug('Copying session keys to secure session %s:%s' % (key,value))
    
    # Destroy old session
    session.invalidate()
    
    # Instate new session with old vars under the new session id
    for key, value in session_old.iteritems():
        session[key] = value
    
    session_set('logged_in_user'        , user.username) # Set server session username so we know the actual user regardless of persona
    #session_set('logged_in_persona_path', user.id      )
    cookie_set("logged_in", "True", secure=False)
    
    user_log.info("logged in with %s" % login_provider)   # Log user login


# GregM: Added prompt_aggregate to allow new users to be prompted with janrain
# Proto: Added redirect_url for redirection after registering
def signin_user_and_redirect(user, login_provider=None, prompt_aggregate=None, redirect_url=None):
    """
    Perform the sigin for a user
    """
    signin_user(user, login_provider)
    
    # Redirect them back to where they were going if a redirect was set
    login_redirector()

    # If no redirect send them to private profile
    #return redirect(url(controller="profile", action="index"))
    if redirect_url:
        return redirect(redirect_url)
    elif prompt_aggregate:
        return redirect("/profile?prompt_aggregate=%s" % (prompt_aggregate))
    else:
        return redirect("/profile")


def signout_user(user):
    user_log.info("logged out")
    session.clear()
    cookie_delete("logged_in")
    #session_delete("login_redirect_url") #unneeded? session.clear() handls this?
    #session_delete("login_redirect_action")


def set_persona(persona):
    assert c.logged_in_user
    persona = get_member(persona)
    if   persona == c.logged_in_persona:
        return True
    elif persona == c.logged_in_user:
        # If trying to fall back to self login then remove persona selection
        session_remove('logged_in_persona'     )
        session_remove('logged_in_persona_role')
        session_remove('logged_in_persona_path')
        c.logged_in_persona      = c.logged_in_user
        c.logged_in_persona_role = 'admin'
        return True
    else:
        membership = get_membership(persona, c.logged_in_persona)
        
        if not membership:
            raise action_error(_('not a member of this group'), code=403)
        if membership.status != "active":
            raise action_error(_('not an active member of this group'), code=403)
        
        role = lowest_role(membership.role, c.logged_in_persona_role)
        
        session_set('logged_in_persona'     , persona.username)
        session_set('logged_in_persona_role', role)
        
        persona_path = session_get('logged_in_persona_path') or str(c.logged_in_user.id)
        persona_path = persona_path.split(',') #if isinstance(persona_path, basestring) else []
        if str(persona.id) in persona_path:
            persona_path = persona_path[0:persona_path.index(str(persona.id))] #Truncate the list at the occourance of this usename
        persona_path.append(persona.id)
        session_set('logged_in_persona_path', ','.join([str(i) for i in persona_path]))
        
        # From this point this user is logged in as this persona
        c.logged_in_persona      = persona
        c.logged_in_persona_role = role
        return True
    return False


def get_lowest_role_for_user(user_list=None):
    """
    user_list is a list of integers
    the first id should always the curent logged in user id (this is appended by base)
    """
    if not user_list:
        user_list = session_get('logged_in_persona_path')
    
    if isinstance(user_list, basestring):
        user_list = [int(i) for i in user_list.split(',')]
        
    if not isinstance(user_list, list):
        return None
    
    roles = Session.query(GroupMembership).filter(or_(*[and_(GroupMembership.member_id==user_list[i], GroupMembership.group_id==user_list[i+1]) for i in range(len(user_list)-1)])).all()
    
    if len(roles) != len(user_list) - 1:
        # If not all the records exisit for the user_list given then some of the links could not be found and the route is invalid. No permissions should be returned
        # Warning is logged - this could mean a permission/membership has changed since the user logged in
        # AllanC - If the warning is spamming the logs it should be removed, but I wanted to catch the error out of paranoia
        log.warn('logged_in_persona_path is invalid - preventing return of group role')
        session_remove('logged_in_persona_path')
        session_remove('logged_in_persona'     )
        return None
    
    role = 'admin'
    for r in roles:
        role = lowest_role(role, r.role)
    return role

    # AllanC - old and poo recursive way to do this
    #def role_recurse(user_list, current_lowest_role):
    #    def first_role(user_list):
    #        try:
    #            return Session.query(GroupMembership).filter(GroupMembership.member_id == user_list[0]).filter(GroupMembership.group_id == user_list[1]).one().role
    #        except:
    #            return None
    #    if   len(user_list)> 2:
    #        return lowest_role(role_recurse(user_list[1:], first_role(user_list)) , current_lowest_role)
    #    elif len(user_list)==2:
    #        return lowest_role(                            first_role(user_list)  , current_lowest_role)
    #    else:
    #        return 'admin' # if there is only one name in the list they are the user and therefor an admin
    #return role_recurse(user_list, 'admin')
