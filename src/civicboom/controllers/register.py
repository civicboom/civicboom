from civicboom.lib.base import BaseController, render, request, url, abort, redirect, c, app_globals, _, session, flash_message, redirect_to_referer

from civicboom.model.member            import User, UserLogin
from civicboom.model.meta              import Session

from civicboom.lib.database.get_cached import get_user
from civicboom.lib.database.actions    import follow, accept_assignment

import logging
log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class RegisterController(BaseController):
    
    def new_user(self, id=None):
        pass

    def email(self):
        # Check the form and riase any problems with the flash message session system
        try:
            form = RegisterSchemaEmailUsername().to_python(dict(request.params))
        except formencode.Invalid, error:
            return unicode(error)

        # Create new user
        u = User()
        u.username  = form['username']
        u.email     = form['email']
        Session.add(u)
        
        
        # Automatically Follow Civicboom
        follow(get_user('civicboom'), u)
    
        # Follow the refered_by user if they exisits
        if 'refered_by' in request.params:
            refered_by = get_user(request.params['refered_by'])
            follow_status = follow(refered_by, u)
            if follow_status == True:
                message_generator.followed_on_signup(refered_by, reporter=u)
        
        # Accept assignment
        if 'accept_assignment' in request.params:
            pass
            # TODO: Implement
            #assignment = get_assignment(request.params['accept_assignment'])
            #accept_assignment_status = accept_assignment(new_reporter, assignment)
            #if accept_assignment_status == True:
            #    message_generator.assignment_accepted(refered_by_reporter,reporter=new_reporter, assignment=assignment)


        Session.commit()

        # Send email verification link
        Session.refresh(u) #Needed for make_hash below becaususe the object must be persistant
        hash            = make_hash_for_reporter(new_reporter)
        validation_link = c.server_name + url_for(controller='register', action='validate_and_register', email=new_reporter.Email, hash=hash)
        message         = 'Please complete the registration process by clicking on, or copying the following link into your browser: %s' % (validation_link)
        send_email(new_reporter, subject='verify e-mail address', content_text=message)
    
        return "Thank you. Please check your email to complete the registration process"
