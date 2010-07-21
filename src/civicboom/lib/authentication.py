# Pyhton package imports
import hashlib

# Pylons imports
from pylons.templating import render_mako as render

# Authkit imports
from authkit.permissions import RequestPermission
from authkit.authorize   import PermissionError, NotAuthenticatedError
from authkit.authorize   import NotAuthorizedError, middleware
from authkit.authorize.pylons_adaptors import authorize

# Civicboom imports
from civicboom.lib.misc   import flash_message
from civicboom.model      import User, UserLogin
from civicboom.model.meta import Session

from sqlalchemy.orm import join

# Logging
import logging
user_log = logging.getLogger("user")


class ValidIndicoUser(RequestPermission):
    def __init__(self, accept_empty=False):
        self.accept_empty = accept_empty
    def check(self, app, environ, start_response):
        if 'REMOTE_USER' not in environ:
            raise NotAuthenticatedError('Not Authenticated')
        return app(environ, start_response)
is_valid_user = ValidIndicoUser()


# Check if a users username and password are valid
#   function is pointed too from the development.ini file
def valid_username_and_password(environ, username, password):
    def get_username_password(username, password):
        password = hashlib.sha1(password).hexdigest()
        try:
            q = Session.query(User).select_from(join(User, UserLogin, User.login_details))
            q = q.filter(User.username==username)
            q = q.filter(User.status=='active')
            q = q.filter(UserLogin.type=='password')
            q = q.filter(UserLogin.token==password)
            q = q.one()
            return q
        except:
            return None

    user = get_username_password(username, password)
    if user:
        #user_log.info(user) #AllanC - TODO errors? does not have events relation?
        return True
    else:
        flash_message('Incorrect username and password')
        return False


#http://pylonsbook.com/en/1.1/simplesite-tutorial-part-3.html#styling-the-sign-in-screen
def render_signin():
    # Future placeholder for differnt login pages based
    #setup_widget_env()
    #if c.widget_reporter: #if identify_widget_url():
    #  result = render('/design09/widget/widget_signin.mako')
    #elif identify_mobile_url():
    #  result = render('/design09/mobile/mobile_signin.mako')
    #else:
    result = render('/web/account/signin.mako')
    result = result.replace('%', '%%').replace('FORM_ACTION', '%s') #VERY IMPORTANT! because this is executing outside of the normal page framework
    return str(result)

# AllanC - could not get this to work WTF?
# had these in the ini file
# authkit.cookie.badcookie.page = false
# authkit.cookie.badcookie.template.obj = indicofb.lib.auth_permissions:render_badcookie
def render_badcookie():
    flash_message('Your login has expired please log in again')
    return redirect_to('/')
