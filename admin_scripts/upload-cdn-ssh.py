#!/usr/bin/python

import optparse
import os

import zipfile
import fnmatch
import gzip
from ConfigParser import SafeConfigParser

import logging
logging.basicConfig(
    level   = logging.INFO,
    format  = "%(asctime)s %(levelname)-5.5s %(message)s",
    datefmt = "%H:%M:%S"
)
log = logging.getLogger(__name__)


if __name__ == '__main__':
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
    host = c.get("DEFAULT", "ssh_host"),

    excludes = []
    if options.exclude:
        excludes = [n.strip() for n in file(options.exclude).readlines()]

    arch = zipfile.ZipFile("static-%s.zip" % options.version, "w")

    # walk through all dirs and all files in the specified folder
    for root, dirnames, filenames in os.walk(args[0]):
        for filename in filenames:
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
                logging.info("Adding %s" % relpath)
                arch.write(fullpath, relpath)

                # if the file is CSS or JS, also add a precompressed version
                # with the same modification timestamp (for nginx to serve)
                if relpath.endswith(".css") or relpath.endswith(".js"):
                    logging.info("Adding %s.gz" % relpath)
                    f = gzip.open(fullpath+".gz", 'wb', 9)
                    f.write(file(fullpath).read())
                    f.close()
                    s = os.stat(fullpath)
                    os.utime(fullpath+".gz", (s.st_atime, s.st_mtime))
                    arch.write(fullpath+".gz", relpath+".gz")
                    os.unlink(fullpath+".gz")

    arch.close()

    os.system("scp static-%s.zip %s:~/" % (options.version, host))
    os.system("ssh %s unzip -o static-%s.zip -d /opt/cb/var/www/static/%s" % (host, options.version, options.version))
    os.system("ssh %s rm -f static-%s.zip" % (host, options.version))
    os.system("rm -f static-%s.zip" % (options.version, ))
