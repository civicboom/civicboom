"""
Task Controller
Maintinence tasks that can be tiggered via cron jobs

All tasks are locked down to be executed by localhost only
See the companion script "tasks.py" in the project root for details on how to
setup a cron job to run these tasks
"""

from pylons                  import request, url, config
from pylons.controllers.util import abort, redirect

from civicboom.lib.base import BaseController, render

from boto.s3.connection import S3Connection
from boto.s3.key import Key
import magic
import os
import logging
import datetime
import hashlib


log = logging.getLogger(__name__)
response_completed_ok = "task:ok" #If this is changed please update tasks.py to reflect the same "task ok" string


class TaskController(BaseController):
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
                request.environ['REMOTE_ADDR'] == request.environ['SERVER_ADDR']
            ):
            return abort(403)
        BaseController.__before__(self)

    def index(self):
        return "timed task controller"

    def expire_syndication_articles(self):
        """
        Description to follow
        """
        pass

    def remove_ghost_reporters(self):
        """
        Users who do not complete the signup process by entering an email
        address that is incorrect or a bots or cant use email should be
        removed if they have still not signed up after 1 week
        """
        pass

    def assignment_near_expire(self):
        """
        Users who have accepted assigments but have not posted response
        question should be reminded via a notification that the assingment
        has not long left
        """
        pass

    def message_clean(self):
        """
        The message table could expand out of control and the old messages
        need to be removed automatically from the db
        """
        pass

    def sync_public_to_warehouse(self):
        """
        Copies files in the public data folder (should just be CSS / small images)
        to whatever warehouse we're using (eg Amazon S3). Should be called whenever
        the server software package is upgraded.
        """
        done = []
        if config["warehouse"] == "s3":
            log.info("Syncing /public to s3")
            connection = S3Connection(config["aws_access_key"], config["aws_secret_key"])
            bucket = connection.get_bucket(config["s3_bucket_name"])
            bucket.set_acl('public-read')
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
                    k.set_metadata('Content-Type', magic.from_file(fname, mime=True))
                    k.set_contents_from_filename(fname)
                    k.set_acl('public-read')
                    done.append("Synced: "+kname)
        return "\n".join(done)

    def purdge_unneeded_warehouse_media(self):
        """
        Compare the warehouse files with the database media list.
        If media records have been removed then we can safly remove them from the warehouse
        """
        #        it also may be worth looking for media records without an associated content record and removeing them as well
        pass