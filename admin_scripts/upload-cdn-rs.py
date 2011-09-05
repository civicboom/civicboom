#!/usr/bin/env python

import os
import sys
import cloudfiles
import optparse
import fnmatch
from ConfigParser import SafeConfigParser

import logging
logging.basicConfig(
    level   = logging.INFO,
    format  = "%(asctime)s %(levelname)-5.5s %(message)s",
    datefmt = "%H:%M:%S"
)
log = logging.getLogger(__name__)

if __name__ == "__main__":
    option_parser = optparse.OptionParser()
    option_parser.add_option('--ini',
        help='INI file to use for pylons settings',
        type='str', default='development.ini')
    option_parser.add_option('--version',
        help='version tag to use as a prefix',
        type='str', default='test')
    option_parser.add_option('--exclude-file',
        help='list of files to exclude', dest="exclude",
        type='str', default=None)
    options, args = option_parser.parse_args()

    c = SafeConfigParser()
    c.read(options.ini)

    excludes = []
    if options.exclude:
        excludes = [n.strip() for n in file(options.exclude).readlines()]

    log.info("Connecting to cloudfiles")
    conn = cloudfiles.get_connection(
        c.get("app:main", "api_key.rs.username"),
        c.get("app:main", "api_key.rs.api_key"),
        authurl = 'https://lon.auth.api.rackspacecloud.com/v1.0'
    )
    cont = conn.get_container(c.get("app:main", "cdn.rs.container"))
    if cont.is_public == False:
        cont.make_public()

    obj = cont.create_object(options.version)
    obj.content_type = "application/directory"
    obj.write("")

    # walk through all dirs and all files in the specified folder
    log.info("Walking files in %s" % args[0])
    for root, dirnames, filenames in os.walk(args[0]):
        for filename in filenames + dirnames:
            fullpath = os.path.join(root, filename)
            relpath = fullpath[len(args[0]):]
            if relpath[0] == "/":
                relpath = relpath[1:]

            # if the file matches an exclusion pattern, skip it
            included = True
            for file_to_exclude in excludes:
                if fnmatch.fnmatch(relpath, file_to_exclude):
                    included = False
                    break

            # if the file is to be included, add it
            if included:
                if filename in filenames:
                    log.info("Adding file %s" % relpath)
                    obj = cont.create_object(os.path.join(options.version, relpath))
                    obj.load_from_filename(fullpath)
                else:
                    log.info("Adding directory %s" % relpath)
                    obj = cont.create_object(os.path.join(options.version, relpath))
                    obj.content_type = "application/directory"
                    obj.write("")

#    sys.exit(main(sys.argv))
