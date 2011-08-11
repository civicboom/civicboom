#!/usr/bin/python

import optparse
import pylons
from paste.deploy import appconfig
from civicboom.config.environment import load_environment

from boto.s3.connection import S3Connection
import magic

import logging
logging.basicConfig(
    level   = logging.INFO,
    format  = "%(asctime)s,%(msecs)03d %(levelname)-5.5s [%(name)s] [%(threadName)s] %(message)s",
    datefmt = "%H:%M:%S"
)
log = logging.getLogger(__name__)

def upload(prefix):
    config = pylons.config

    connection = S3Connection(config["api_key.aws.access"], config["api_key.aws.secret"])
    bucket = connection.get_bucket(config["warehouse.s3.bucket"])

    for key in bucket.list(prefix=prefix):
        print key,
#        if key.get_metadata("Cache-Control"):
#            print "already cached"
#            continue
        key.open()
        sample = key.read(4096)
        key.close()
        metadata = {
            'Content-Type': magic.from_buffer(sample, mime=True),
            'Cache-Control': 'public, max-age=31536000',
            #'Expires': 'Sun, 17 Mar 2023 17:48:53 GMT', # FIXME: now() + 1 year
            #'Content-Disposition': 'inline; filename='+__http_escape(filename) if filename else 'inline',
        }

        key.copy(bucket.name, key.key, metadata=metadata)
        key.set_acl('public-read')
        print "updated"


if __name__ == '__main__':
    option_parser = optparse.OptionParser()
    option_parser.add_option('--ini',
        help='INI file to use for pylons settings',
        type='str', default='development.ini')
    option_parser.add_option('--prefix',
        help='which folder to sync',
        type='str', default='avatars')
    options, args = option_parser.parse_args()

    # Initialize the Pylons app
    conf = appconfig('config:' + options.ini, relative_to='.')
    load_environment(conf.global_conf, conf.local_conf)

    # Now code can be run, the SQLalchemy Session can be used, etc.
    upload(options.prefix)
