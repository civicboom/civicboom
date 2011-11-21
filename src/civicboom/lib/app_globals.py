"""The application's Globals object"""


import redis
import os

from cbutils.redis_ import redis_from_url

import time

import logging
log = logging.getLogger(__name__)

class Globals(object):
    """
    Globals acts as a container for objects available throughout the life of the application
    """

    def __init__(self, config):
        """
        One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable
        """
    
        if os.path.exists(".version"):
            self.version   = file(".version").read().strip()
        else:  # pragma: no cover - all released versions have a version
            self.version   = None

        version_dev = int(time.time()) # DRAT! a hack for adding a timestamp for dev cache eTag versions ... whatever you do .. DONT set seld.version to anything if your in develop :( .. just dont

        self.memcache = redis_from_url(config['worker.queue.url'])

