"""
json protocol suggestion:

    {
        "status": "ok" / "error",                              (required)
        "message": "string to show in app status bar / popup", (optional, should be there if status = error)
        "data": {                                              (optional)
            "foo": "bar", # function-specific data
            "baz": "qux"
        }
    }

then API users can have a call like

    civicboom_json_request(name):
        try:
            req = json.parse(http_get("http://civicboom.com/%s.json" % name))
        except Exception, e:
            req = {"status": "error", "message": "error fetching data from server: "+str(e)}

        if req["status"] == "error":
            if req["message"]:
                error_alert(req["message"])
            return None
        else:
            if req["message"]:
                status_alert(req["message"])
            return req["data"]

    messages = civicboom_json_request("messages/index")
    if messages:
        <do stuff with messages>
    else:
        <the error message has been displayed already, we don't
        really need an else unless we think we can recover from
        the error>
"""

from pylons import request, response, session, tmpl_context as c, url, config
from pylons.controllers.util import abort, redirect
from webhelpers.pylonslib.secure_form import authentication_token

from civicboom.lib.base import BaseController, render
from civicboom.lib.authentication import authorize, is_valid_user

from decorator import decorator
from datetime import datetime
from glob import glob
import json
import hashlib

import logging
log = logging.getLogger(__name__)
user_log = logging.getLogger("user")

template_expire = 14400 # 14400 is 4 hours in seconds
file_parts = {}

class MobileController(BaseController):
    #-----------------------------------------------------------------------------
    # Decorators
    #-----------------------------------------------------------------------------

    # Check logged in - No need for authkit authentication as the mobile app is not a human
    @decorator
    def __logged_in_mobile(func, *args, **kargs):
        if not c.logged_in_user:
            return 'mobile:not_authenticated'
            # return json.dumps({"status": "error", "message": "not authenticated"})
        return func(*args,**kargs)


    #-----------------------------------------------------------------------------
    # Sign in
    #-----------------------------------------------------------------------------  
    @authorize(is_valid_user)
    def signin(self):
        return "mobile:authentication_ok"
        # return json.dumps({"status": "ok", "message": "logged in ok", "data": {"auth_token": authentication_token()}})


    #-----------------------------------------------------------------------------
    # Sign up
    #-----------------------------------------------------------------------------
    def signup(self):
        return "mobile signup" # FIXME: render('web/design09/mobile_signup.mako')


    #-----------------------------------------------------------------------------
    # Latest Version
    #-----------------------------------------------------------------------------  
    def latest_version(self):
        return "1.13"
        # return json.dumps({"status": "ok", "data": {"version": "1.13"}})


    #-----------------------------------------------------------------------------
    # Main App: Accepted Assignments JSON List
    #-----------------------------------------------------------------------------
    @__logged_in_mobile
    def accepted_assignments(self):
        cache_key = gen_cache_key(reporter_assignments_accepted=c.logged_in_reporter.id)
        return json.dumps([{
            "id":                assignment.id,
            "title":             assignment.title,
            "content":           h.truncate(assignment.content, length=max_content_length, indicator='...', whole_word=True),
            "image":             assignment.primary_media.thumbnail_url if assignment.primary_media else None,
            "assigned_by":       assignment.creator.name,
            "assigned_by_image": assignment.creator.avatar_url,
            "expiry_date":       assignment.due_date,
        } for assignment in c.logged_in_user.accepted_assignments])
        # return json.dumps({"status": "ok", "data": ...})


    #-----------------------------------------------------------------------------
    # Main App: Messages
    #-----------------------------------------------------------------------------
    @__logged_in_mobile
    def messages(self):
        #cache_key = gen_cache_key(reporter_messages=c.logged_in_user.id) # This will terminate the method call if the eTags match
        c.logged_in_user.last_check = datetime.now()
        return json.dumps([{
            "id":            message.id,
            "sourceId":      message.source_id,
            "message":       message.content,
            "timestamp":     str(message.timestamp),
            "link":          "",
            "response_type": "",
            "more":          "", # FIXME: protocol -- no more = blank string, more = array of one assignment; should be no more = None, more = one assignment
        } for message in c.logged_in_user.messages_notification[:10]]) # FIXME: do we want notifications AND private messages?
        # return json.dumps({"status": "ok", "data": ...})


    #-----------------------------------------------------------------------------
    # Upload Article
    #-----------------------------------------------------------------------------
    # We can make assumptions here that the mobile app will have done some validation of the input
    # it is not nessisarry to use formencode as the mobile app would have no idea how to interperit the data back
    # We return an OK message or the mobile app will assume an error
    @__logged_in_mobile
    def upload(self):
        # Check form data (if in dev mode show HTML test form else give no data error)
        if not request.POST:
            if config['debug']:
                return render(prefix+'mobile_upload_test.mako')
            return 'mobile:form_data_required'
            # return json.dumps({"status": "error", "message": "form data required"})

        unique_id                   = hashlib.md5(request.POST['uniqueid']).hexdigest()
        mobile_upload_unique_id_key = c.logged_in_user.username + "_" + unique_id

        # check for duplicate upload
        if mobile_upload_reocorded(mobile_upload_unique_id_key):
            return "mobile:upload_ok"
            # return json.dumps({"status": "ok", "message": "article already uploaded"})


        if "syndicate" in request.POST:
            article           = SyndicatedContent()
        else:
            article           = ArticleContent()
        article.creation_time = datetime.now()
        article.creator       = c.logged_in_user
        article.title         = request.POST['title'].encode('utf-8')
        article.content       = clean_article_html(request.POST['content'].encode('utf-8'))
        article.license       = None # CreaviveCommonsLicenceTypeId = 2 #self.form_result['licence']

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
        if dictHasValue(request.POST,'assignment'):
            article.parent_id.creator.send_message(
                message_generator.assignment_response_mobile(
                    reporter=article.reporter,
                    article=article,
                    assignment=article.assignment
                )
            )
        if article.reporter.NumFollowers > 0 and not article.syndicating:
            for follower in article.reporter.followed_by_reporters:
                follower.send_message(
                    message_generator.article_published_by_followed_mobile(
                        reporter=article.reporter,
                        article=article
                    )
                )

        if not article.syndicating:
            profanity_check_article(article)
            twitter_content(article)

        Session.commit()

        return "mobile:upload_ok"
        # return json.dumps({"status": "ok", "message": "upload ok"})

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
    @__logged_in_mobile
    def upload_file(self):
        if not request.POST:
            if config['debug']:
                return render(prefix+'mobile_upload_part_test.mako')
            return 'mobile:form_data_required'
            # return json.dumps({"status": "error", "message": "form data required"})

        part_num    = int(request.POST['part'] )
        parts_count = int(request.POST['parts'])
        unique_id   = hashlib.md5(request.POST['uniqueid']).hexdigest()
        file_base   = os.path.join(config['cache_dir'], "mobile_uploads", c.logged_in_user.username+'_'+unique_id)
        data        = request.POST['file_part'].value

        file(file_base+"_"+str(part_num), "wb").write(data)

        # check to see if any parts are missing, ask for them if needed
        for n in range(0, parts_count): # FIXME: off-by-one at each end?
            if not os.path.exists(file_base+"_"+str(n)): # FIXME: check file content? (compare hash / filesize with client?)
                return 'mobile:next_part_%d' % n
                # return json.dumps({"status": "ok", "message": "part %d/%d uploaded" % (part_num, parts_count), "data": {"next": n}})

        # no parts needed; join the parts into one
        else:
            fp = file(file_base, "wb")
            for n in range(0, parts_count): # FIXME: off-by-one at each end?
                part_file = file_base+"_"+str(n)
                fp.write(file(part_file).read())
                os.unlink(part_file)
            fp.close()
            return 'mobile:upload_ok'
            # return json.dumps({"status": "ok", "message": "upload complete", "data": {"next": None}})


    #-----------------------------------------------------------------------------
    # Log mobile error
    #-----------------------------------------------------------------------------
    # If the mobile app has an error that it is not expecting then it can notify the live server
    # This can then be logged and email sent etc
    def error(self):
        if not request.POST:
            if config['debug']:
                return "mobile error test" # FIXME: render(prefix+'mobile_error_test.mako')
            return 'mobile:form_data_required'
            # return json.dumps({"status": "error", "message": "form data required"})
        if 'error_message' in request.POST:
            send_email(config['email_to'], subject='Mobile Error', content_text=request.POST['error_message'])
            #AllanC - Temp addition to get errors to the mobile developer
            send_email("nert@poik.net"     , subject='Mobile Error', content_text=request.POST['error_message'])
            return "mobile:logged_ok"
            # return json.dumps({"status": "ok", "message": "logged ok"})

