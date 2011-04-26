"""
Task Controller
Maintinence tasks that can be tiggered via cron jobs

All tasks are locked down to be executed by localhost only
See the companion script "tasks.py" in the project root for details on how to
setup a cron job to run these tasks
"""

from civicboom.lib.base import *

import datetime

log = logging.getLogger(__name__)

response_completed_ok = "task:ok" #If this is changed please update tasks.py to reflect the same "task ok" string


class TaskController(BaseController):
    
    #---------------------------------------------------------------------------
    # Security: Restict Calls to Localhost
    #---------------------------------------------------------------------------
    
    def __before__(self, action, **params):
        ##  Only accept requests from 127.0.0.1 as we never want these being
        ##  run by anyone other than the server at set times the server cron
        ##  system should have a script that makes URL requests at localhost
        ##  to activate these actions
        ##  Shish - no REMOTE_ADDR = "paster request foo.ini /task/blah" from
        ##  the command line
        if not (
                'REMOTE_ADDR' not in request.environ or
                request.environ['REMOTE_ADDR'] == "127.0.0.1" or
                request.environ['REMOTE_ADDR'] == request.environ.get('SERVER_ADDR', '0.0.0.0')
            ):
            return abort(403)
        user_log.info("Performing task '%s'" % (action, ))
        BaseController.__before__(self)


    #---------------------------------------------------------------------------
    # Expire Syndication Content
    #---------------------------------------------------------------------------

    def expire_syndication_articles(self):
        """
        Description to follow
        """
        pass


    #---------------------------------------------------------------------------
    # Remove Ghost Users
    #---------------------------------------------------------------------------

    def remove_ghost_user(self):
        """
        Users who do not complete the signup process by entering an email
        address that is incorrect or a bots or cant use email should be
        removed if they have still not signed up after 4 Days
        """
        from civicboom.model.member import User
        ghost_expire = datetime.datetime.now() - datetime.timedelta(days=4)
        for u in Session.query(User).filter(~User.login_details.any()).filter(User.join_date < ghost_expire).all():
            Session.delete(u)
            # It may be nice to log numbers here to aid future business desctions
        Session.commit()
        # AllanC - the method above could be inefficent. could just do it at the DB side?
        return response_completed_ok


    #---------------------------------------------------------------------------
    # Assignment Reminder Notifications
    #---------------------------------------------------------------------------

    def assignment_near_expire(self):
        """
        Users who have accepted assigments but have not posted response
        question should be reminded via a notification that the assingment
        has not long left
        """
        from sqlalchemy import and_
        from civicboom.model.content import AssignmentContent
        
        def get_assignments_by_date(date_start, date_end):
            return Session.query(AssignmentContent).filter(and_(AssignmentContent.due_date >= date_start, AssignmentContent.due_date <= date_end)).all()

        def get_responded(assignment):
            return [response.creator_id for response in assignment.responses]
            
        date_7days_time = datetime.datetime.now() + datetime.timedelta(days=6)
        date_1days_time = datetime.datetime.now() # + datetime.timedelta(days=1)
        date_1day       =                           datetime.timedelta(days=1)
        
        for assignment in get_assignments_by_date(date_start=date_7days_time, date_end=date_7days_time + date_1day): # Get all assignments due in 7 days
            responded_member_ids = get_responded(assignment)                                                         #   Get a list of all the members that have responded to this assignment
            for member in assignment.accepted_by:                                                                    #   For all members accepted this assignment
                if member.id not in responded_member_ids:                                                            #     Check if they have responded with an article
                    member.send_notification( messages.assignment_due_7days(member, assignment=assignment) )              #     if not send a reminder notification
                    
        for assignment in get_assignments_by_date(date_start=date_1days_time, date_end=date_1days_time + date_1day): #Same as above but on day before
            responded_member_ids = get_responded(assignment)
            for member in assignment.accepted_by:
                if member.id not in responded_member_ids:
                    member.send_notification( messages.assignment_due_1day(member, assignment=assignment) )
                    
        Session.commit()
        return response_completed_ok


    #---------------------------------------------------------------------------
    # Message Clean
    #---------------------------------------------------------------------------

    def message_clean(self):
        """
        The message table could expand out of control and the old messages
        need to be removed automatically from the db
        """
        pass


    #---------------------------------------------------------------------------
    # Sync Warehouse Media
    #---------------------------------------------------------------------------

    def sync_public_to_warehouse(self):
        """
        Copies files in the public data folder (should just be CSS / small images)
        to whatever warehouse we're using (eg Amazon S3). Should be called whenever
        the server software package is upgraded.
        """
        from boto.s3.connection import S3Connection
        from boto.s3.key import Key
        import magic
        import os
        import hashlib

        done = []
        if config["warehouse"] == "s3":
            log.info("Syncing /public to s3")
            connection = S3Connection(config["aws_access_key"], config["aws_secret_key"])
            bucket = connection.get_bucket(config["s3_bucket_name"])
            bucket.set_acl('public-read')
            #bucket.configure_versioning(True)
            for dirpath, subdirs, filenames in os.walk("./civicboom/public/"):
                for fname in filenames:
                    fname = os.path.join(dirpath, fname)
                    kname = fname[fname.find("public"):]
                    k = bucket.get_key(kname)
                    if k and k.etag.strip('"') == hashlib.md5(file(fname).read()).hexdigest():
                        done.append("No change: "+kname)
                        continue
                    k = Key(bucket)
                    k.key = kname
                    k.set_metadata('Cache-Control', 'public')
                    k.set_metadata('Content-Type', magic.from_file(fname, mime=True))
                    k.set_contents_from_filename(fname)
                    k.set_acl('public-read')
                    done.append("Synced: "+kname)
        return "\n".join(done)


    def purge_unneeded_warehouse_media(self):
        """
        Compare the warehouse files with the database media list.
        If media records have been removed then we can safly remove them from the warehouse
        """
        #        it also may be worth looking for media records without an associated content record and removeing them as well
        pass


    #---------------------------------------------------------------------------
    # Test Task
    #---------------------------------------------------------------------------

    def test(self):
        return "<task happened>"
