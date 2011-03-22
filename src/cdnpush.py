#!/usr/bin/python

import optparse
import os
from ConfigParser import SafeConfigParser

from boto.s3.connection import S3Connection
from boto.s3.key import Key
import magic
import fnmatch

import logging
logging.basicConfig(
    level   = logging.INFO,
    format  = "%(asctime)s %(levelname)-5.5s %(message)s",
    datefmt = "%H:%M:%S"
)
log = logging.getLogger(__name__)


def upload(config, filename, keyname):
    connection = S3Connection(config.get("DEFAULT", "aws_access_key"), config.get("DEFAULT", "aws_secret_key"))
    bucket = connection.get_bucket(config.get("DEFAULT", "s3_bucket_name"))

    key = Key(bucket)
    key.key = keyname
    metadata = {
        'Content-Type': magic.from_file(filename, mime=True),
        'Cache-Control': 'public, max-age=31536000',
        #'Expires': 'Sun, 17 Mar 2023 17:48:53 GMT', # FIXME: now() + 1 year? necessary at all?
        #'Content-Disposition': 'inline; filename='+__http_escape(filename) if filename else 'inline',
    }

    log.info("Uploading %s (%s)" % (keyname, metadata['Content-Type']))
    key.set_contents_from_filename(filename, headers=metadata)
    key.set_acl('public-read')


if __name__ == '__main__':
    option_parser = optparse.OptionParser()
    option_parser.add_option('--ini',
        help='INI file to use for pylons settings',
        type='str', default='development.ini')
    option_parser.add_option('--version',
        help='version tag for the assets',
        type='str', default=None)
    option_parser.add_option('--exclude-file',
        help='list of files to exclude', dest="exclude",
        type='str', default=None)
    options, args = option_parser.parse_args()

    # Initialize the Pylons app
    #conf = appconfig('config:' + options.ini, relative_to='.')
    #load_environment(conf.global_conf, conf.local_conf)
    config = SafeConfigParser()
    config.read(options.ini)

    # Now code can be run, the SQLalchemy Session can be used, etc.

    excludes = []
    if options.exclude:
        excludes = [n.strip() for n in file(options.exclude).readlines()]

    files = []
    for root, dirnames, filenames in os.walk(args[0]):
        for filename in filenames:
            fullpath = os.path.join(root, filename)
            relpath = fullpath[len(args[0])+1:]
            included = True
            for file_to_exclude in excludes:
                if fnmatch.fnmatch(relpath, file_to_exclude):
                    included = False
                    break
            if included:
                upload(config, fullpath, os.path.join("public", options.version, relpath))
