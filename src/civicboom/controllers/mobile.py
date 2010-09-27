from civicboom.lib.base import *

from civicboom.model              import Media, ArticleContent, SyndicatedContent
from civicboom.lib                import helpers as h
from civicboom.lib.communication  import messages
from civicboom.lib.text           import clean_html

from decorator import decorator
from datetime import datetime
from glob import glob
import os
import json
import hashlib

log = logging.getLogger(__name__)
user_log = logging.getLogger("user")


#-----------------------------------------------------------------------------
# Decorators
#-----------------------------------------------------------------------------

# Check logged in - No need for redirect to HTML signin form as the mobile app is not a human
@decorator
def _logged_in_mobile(func, *args, **kargs):
    if not c.logged_in_user:
        return action_error("not authenticated", code=403)
    return func(*args, **kargs)


class MobileController(BaseController):
    #-----------------------------------------------------------------------------
    # Sign in
    #-----------------------------------------------------------------------------  
    @auto_format_output()
    @authorize(is_valid_user)
    def signin(self):
        return action_ok("logged in ok", {"auth_token": authentication_token()})


    #-----------------------------------------------------------------------------
    # Sign up
    #-----------------------------------------------------------------------------
    def signup(self):
        return "mobile signup" # FIXME: render('web/design09/mobile_signup.mako')


    #-----------------------------------------------------------------------------
    # Latest Version
    #-----------------------------------------------------------------------------  
    @auto_format_output()
    def latest_version(self, format="html"):
        if format == "html":
            # HTML format = really old; the only HTML output we want to support
            # is the "you need to upgrade" bit; everything else in the controller
            # can break compatability
            return "1.14"
        else:
            return action_ok(data={"version": "1.14"})


    #-----------------------------------------------------------------------------
    # Upload Article
    #-----------------------------------------------------------------------------
    # We can make assumptions here that the mobile app will have done some validation of the input
    # it is not nessisarry to use formencode as the mobile app would have no idea how to interperit the data back
    # We return an OK message or the mobile app will assume an error
    @_logged_in_mobile
    @auto_format_output()
    def upload(self):
        # Check form data (if in dev mode show HTML test form else give no data error)
        if not request.POST:
            if config['debug']:
                return "mobile upload test" # FIXME: render(prefix+'mobile_upload_test.mako')
            return action_error("form data required", code=400)

        unique_id                   = hashlib.md5(request.POST['uniqueid']).hexdigest()
        mobile_upload_unique_id_key = c.logged_in_user.username + "_" + unique_id

        # check for duplicate upload, see feature #29
        if app_globals.memcache.get("mobile-upload-complete:"+unique_id):
            return "mobile:upload_ok"
            return action_error("article already uploaded", code=409)


        if "syndicate" in request.POST:
            article           = SyndicatedContent()
        else:
            article           = ArticleContent()
        article.creation_time = datetime.now()
        article.creator       = c.logged_in_user
        article.title         = request.POST['title'].encode('utf-8')
        article.content       = clean_html(request.POST['content'].encode('utf-8'))
        article.license       = None # FIXME: CreaviveCommonsLicenceTypeId = 2 #self.form_result['licence'] # see bug #48

        if "geolocation_longitude" in request.POST and "geolocation_latitude" in request.POST:
            article.location = "SRID=4326;POINT(%d %d)" % (
                float(request.POST['geolocation_longitude']),
                float(request.POST['geolocation_latitude'])
            )

        if 'assignment' in request.POST:
            article.parent_id = int(request.POST['assignment'])

        # Check for separately uploaded files and processed them accordingly
        file_base = os.path.join(config['cache_dir'], "mobile_uploads", c.logged_in_user.username+'_'+unique_id)
        for filename in glob(file_base+"*"):
            m = Media()
            m.load_from_file(filename)
            article.attachments.append(m)

        Session.add(article)
        Session.commit() # (once commited the article with have an ID) idea?: Session.flush() will also get ID without commit? will it not?
        user_log.info("upload mobile article '%s'" % article.title)

        # Generate Messages
        if 'assignment' in request.POST:
            article.parent_id.creator.send_message(
                messages.assignment_response_mobile(
                    reporter=article.reporter,
                    article=article,
                    assignment=article.assignment
                )
            )
        if article.reporter.NumFollowers > 0 and not article.syndicating:
            for follower in article.reporter.followed_by_reporters:
                follower.send_message(
                    messages.article_published_by_followed_mobile(
                        reporter=article.reporter,
                        article=article
                    )
                )

        # FIXME: reimplement these differently
        #if not article.syndicating:
        #    profanity_check_article(article)
        #    twitter_content(article)

        Session.commit()
        app_globals.memcache.set("mobile-upload-complete:"+unique_id, True)

        return action_ok("upload ok", code=201)

    #-----------------------------------------------------------------------------
    # Upload File Part
    #-----------------------------------------------------------------------------
    # Potentialy on flakey mobile connections the connection can drop all over the place
    # The solution was to implment a custom mobile multi part system.
    # The client splits the large file into binary chuncks (of equal size) and sends them to the server with a part number
    # The server then concatinates the part to the end of the main file
    # Because we cant guarentee that messages can get back to the server we implement the following
    #    Client sends chunk 0
    #    Server makes new file
    #    Server sends back gimmi 1
    #    Client responds with chunk 1
    #     if client does not give 1 then server takes the data, does nothing with it and asks again
    #     Server asks gimi 1
    #     until server is given 1
    #    If the server dies and restarts mid way and recives a later segment (e.g part 69) then it may respond with gimmi 0, the client should oblige
    #    The client can expect to be asked to send the previous chunk again, the next chunk or the first chunk
    # Client can assume the server will not ask for parts out of sequence e.g gimmi 24 then gimmi 28 should not happen
    #
    # Note for future multiple files the client could just add a single didget to the end of the uniqueid i.e if uniqueid = 0000, client could send 00001 for file 1 and 00002 for file 2
    # because the upload code looks for all files containing the uniqueid then they should still trigger
    @_logged_in_mobile
    @auto_format_output()
    def upload_file(self):
        if not request.POST:
            if config['debug']:
                return "mobile upload part test" # FIXME: render(prefix+'mobile_upload_part_test.mako')
            return action_error("form data required", code=400)

        part_num    = int(request.POST['part'] )
        parts_count = int(request.POST['parts'])
        unique_id   = hashlib.md5(request.POST['uniqueid']).hexdigest()
        file_base   = os.path.join(config['cache_dir'], "mobile_uploads", c.logged_in_user.username+'_'+unique_id)
        data        = request.POST['file_part'].value

        file(file_base+"_"+str(part_num), "wb").write(data)

        # check to see if any parts are missing, ask for them if needed
        for n in range(0, parts_count):
            if not os.path.exists(file_base+"_"+str(n)): # FIXME: check file content? (compare hash / filesize with client?), see feature #29
                return action_ok("part %d/%d uploaded" % (part_num, parts_count), data={"next": n}, code=202)

        # no parts needed; join the parts into one
        else:
            fp = file(file_base, "wb")
            for n in range(0, parts_count):
                part_file = file_base+"_"+str(n)
                fp.write(file(part_file).read())
                os.unlink(part_file)
            fp.close()
            return action_ok("upload complete", data={"next": None}, code=201)


    #-----------------------------------------------------------------------------
    # Log mobile error
    #-----------------------------------------------------------------------------
    # If the mobile app has an error that it is not expecting then it can notify the live server
    # This can then be logged and email sent etc
    def error(self):
        from civicboom.lib.communication.email import send_email
        if not request.POST:
            if config['debug']:
                return "mobile error test" # FIXME: render(prefix+'mobile_error_test.mako')
            return action_error("form data required", code=401)
        if 'error_message' in request.POST:
            send_email(config['email_to'], subject='Mobile Error', content_text=request.POST['error_message'])
            #AllanC - Temp addition to get errors to the mobile developer
            send_email("nert@poik.net"   , subject='Mobile Error', content_text=request.POST['error_message'])
            return action_ok("logged ok", code=201)

