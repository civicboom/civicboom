#!/usr/bin/python

import optparse
import os

import zipfile
import fnmatch
import gzip

import logging
logging.basicConfig(
    level   = logging.INFO,
    format  = "%(asctime)s %(levelname)-5.5s %(message)s",
    datefmt = "%H:%M:%S"
)
log = logging.getLogger(__name__)


if __name__ == '__main__':
    option_parser = optparse.OptionParser()
    option_parser.add_option('--output',
        help='zip file to write to',
        type='str', default=None)
    option_parser.add_option('--exclude-file',
        help='list of files to exclude', dest="exclude",
        type='str', default=None)
    options, args = option_parser.parse_args()

    excludes = []
    if options.exclude:
        excludes = [n.strip() for n in file(options.exclude).readlines()]

    arch = zipfile.ZipFile(options.output, "w")
    for root, dirnames, filenames in os.walk(args[0]):
        for filename in filenames:
            fullpath = os.path.join(root, filename)
            relpath = fullpath[len(args[0]):]
            included = True
            for file_to_exclude in excludes:
                if fnmatch.fnmatch(relpath, file_to_exclude):
                    included = False
                    break
            if included:
                logging.info("Adding %s" % relpath)
                arch.write(fullpath, relpath)
                if relpath.endswith(".css") or relpath.endswith(".js"):
                    logging.info("Adding %s.gz" % relpath)
                    f = gzip.open('/tmp/cb-static-foo.gz', 'wb', 9)
                    f.write(file(fullpath).read())
                    f.close()
                    arch.write('/tmp/cb-static-foo.gz', relpath+".gz")
    arch.close()
