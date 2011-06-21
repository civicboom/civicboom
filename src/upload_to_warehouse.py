#!/usr/bin/python

import optparse
from paste.deploy import appconfig
from civicboom.config.environment import load_environment
from civicboom.lib.services import warehouse as wh
import os

import logging
logging.basicConfig(
    level   = logging.INFO,
    format  = "%(asctime)s,%(msecs)03d %(levelname)-5.5s [%(name)s] [%(threadName)s] %(message)s",
    datefmt = "%H:%M:%S"
)
log = logging.getLogger(__name__)

def upload(folder, args):
    for arg in args:
        wh.copy_to_warehouse(arg, folder, wh.hash_file(arg), filename=os.path.basename(arg))

if __name__ == '__main__':
    option_parser = optparse.OptionParser()
    option_parser.add_option('--ini',
        help='INI file to use for pylons settings',
        type='str', default='development.ini')
    option_parser.add_option('--folder',
        help='which folder to upload to',
        type='str', default='avatars')
    options, args = option_parser.parse_args()

    # Initialize the Pylons app
    conf = appconfig('config:' + options.ini, relative_to='.')
    load_environment(conf.global_conf, conf.local_conf)

    # Now code can be run, the SQLalchemy Session can be used, etc.
    upload(options.folder, args)
