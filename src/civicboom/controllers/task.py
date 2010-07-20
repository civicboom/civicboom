"""
Task Controller
Maintinence tasks that can be tiggered via cron jobs

All tasks are locked down to be executed by localhost only
See the companion script "tasks.py" in the project root for details on how to
setup a cron job to run these tasks

"""

import logging
import datetime

log = logging.getLogger(__name__)


response_completed_ok = "task:ok" #If this is changed please update tasks.py to reflect the same "task ok" string



class TaskController(BaseController):

  def __before__(self, action, **params):
    ##  Only accept requests from 127.0.0.1 as we never want these being run by anyone other than the server at set times
    ##  the server cron system should have a script that makes URL requests at localhost to activate these actions
    if not (request.environ['REMOTE_ADDR'] == "127.0.0.1" or request.environ['REMOTE_ADDR'] == request.environ['SERVER_ADDR']):
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
    Users who do not complete the signup process by entering an email address that is incorrect or a bots or cant use email should be removed if they have still not signed up after 1 week
    """
    pass

  def assignment_near_expire(self):
    """
    Users who have accepted assigments but have not posted response question should be reminded via a notification that the assingment has not long left
    """
    pass
  
  def message_clean(self):
    """
    The message table could expand out of control and the old messages need to be removed automatically from the db
    """
    pass