from civicboom.lib.base import url, _, config
from civicboom.lib.database.get_cached import get_member, get_member_email
from civicboom.lib.communication.email_lib import send_email
from civicboom.lib.services.janrain import janrain
from civicboom.model import UserLogin
from civicboom.model.meta import Session

import logging
log      = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# Pending Users Allowed URL
#-------------------------------------------------------------------------------
# Users in pending status are forced to complete the registration process.
#   some urls have to be made avalable to pending users (such as signout, etc)
pending_user_allowed_list = ['register/new_user', 'account/', 'widget/', 'misc/', '/accept']


def deny_pending_user(url_to_check):
    for url_safe in pending_user_allowed_list:
        if url_to_check.find(url_safe) >= 0:
            return False
    return True


#-------------------------------------------------------------------------------
# Verify Email
#-------------------------------------------------------------------------------

def validation_url(user, controller, action):
    return url(controller=controller, action=action, id=user.username, hash=user.hash(), sub_domain='www', protocol='https')


def send_verifiy_email(user, controller='account', action='verify_email', message=None, subject=None):
    if not subject:
        subject = _('verify e-mail address')
    if not message:
        message = _('verify this email address')
#    Session.refresh(user)
    validation_link  = validation_url(user, controller, action)
    message          = _('Please %s by clicking on, or copying the following link into your browser: %s') % (message, validation_link)
    if action == 'verify_email':
        send_email(user.email_unverified, subject=subject, content_text=message)
    else:
        user.send_email(subject=subject, content_text=message)
    

def verify_email_hash(user, hash, commit=False):
    user = get_member(user)
    if user and user.hash() == hash:
        if not config['demo_mode']: # AllanC - Demo mode is ALWAYS offline, there is no way we can validate members emails address's. But the hash is correct so return True
            if user.email_unverified:
                user.email            = user.email_unverified
                user.email_unverified = None
            if commit:
                Session.commit()
        return True
    return False

#def send_forgot_password_email(user):
#    validation_link = url(controller='account', action='forgot_password', id=user.username, hash=user.hash(), sub_domain='www', protocol='https')
#    message         = _('Please click or copy the following link into your browser to reset your password: %s' % validation_link)
#    user.send_email(subject=_('reset password'), content_text=message)


#-------------------------------------------------------------------------------
# Accounts
#-------------------------------------------------------------------------------

def associate_janrain_account(user, type, token):
    """
    Associate a login record for a Janrain account
    This is called at:
        1.) Registration
        2.) Linking multiple login accounts to a single Civicboom account
    """
    login = None
    try:
        login = Session.query(UserLogin).filter(UserLogin.token == token).filter(UserLogin.type == type).one()
    except:
        pass
    if login:
        if login.user == user:
            return # If login already belongs to this user then abort
        if login.user: # Warn existing user that account is being reallocated
            login.user.send_email(subject=_('login account reallocated'), content_text=_('your %s account has been allocated to the user %s') % (type, user.username))
        if not config['development_mode']:
            janrain('unmap', identifier=login.token, primaryKey=login.member_id)
        login.user   = user
    else:
        login = UserLogin()
        login.user   = user
        login.type   = type
        login.token  = token
        Session.add(login)
    Session.commit()
    if not config['development_mode']:
        janrain('map', identifier=login.token, primaryKey=login.member_id) # Let janrain know this users primary key id, this is needed for agrigation posts


#-------------------------------------------------------------------------------
# Password Setter
#-------------------------------------------------------------------------------
# AllanC - don't know if this is right place, but related account stuff was the closest I could think of

def set_password(user, new_token, delay_commit=False):
    """
    Set password
    WARNING! We assume the user has already been authenticated
    - remove old password (if found)
    - create new password record
    """
    # search for existing record and remove it
    #
    try:
        for existing_login in [login for login in user.login_details if login.type == 'password']:
            log.debug("removing password for %s" % user.username)
            #if existing_login.token == old_token: raise Exception('old password token does not match - aborting password change')
            Session.delete(existing_login)
            log.debug("removed ok")
    #try: Session.execute(UserLogin.__table__.delete().where(and_(UserLogin.__table__.c.member_id == user.id, UserLogin.__table__.c.token == token)))
    except Exception:
        pass
    # Set new password
    u_login = UserLogin()
    u_login.user   = user
    u_login.type   = 'password'
    u_login.token  = new_token
    Session.add(u_login)
    
    if not delay_commit:
        Session.commit()


def has_account_without_password(user):
    user = get_member(user) or get_member_email(user)
    password_login = None
    if user:
        try:
            password_login = Session.query(UserLogin).filter(UserLogin.user==user).filter(UserLogin.type  == 'password').one()
        except Exception:
            pass
        if not password_login:
            return True
    return False
