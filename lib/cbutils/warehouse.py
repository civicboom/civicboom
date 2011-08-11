"""
Warehouse module

Dependencies:
  Python 2.6
  Boto 1.9b

Use:
  import warehouse as wh
  wh.configure({
      "warehouse.type": "s3",
      "warehouse.s3.bucket": "my-bucket",
      "api_key.aws.access": "q456w5ysh54dgrtg",
      "api_key.aws.secret": "1345etywertywr65",
  })
  key = wh.copy_to_warehouse("/home/shish/demo.avi", "movies")
  print "Uploaded to my-bucket.s3.amazonaws.com/movies/%s" % key
"""

import os
import shutil
import hashlib
import magic
import logging
import re

from boto.s3.connection import S3Connection
from boto.s3.key import Key


log = logging.getLogger(__name__)
config = None


def configure(c):
    global config
    config = c


def copy_cgi_file(cgi_fileobj, dest_filename):
    """
    Relocate a file from temp upload (a cgi.FieldStorage object) to local file
    Reference: Definative Guide to Pylons - pg99
    """
    if hasattr(cgi_fileobj,'file'):
        dest_fileobj = open(dest_filename,'wb')
        shutil.copyfileobj(cgi_fileobj.file, dest_fileobj)
        cgi_fileobj.file.close()
        dest_fileobj.close()
    else:
        shutil.copyfile(cgi_fileobj, dest_filename)


def copy_to_warehouse(src, warehouse, hash=None, filename=None, placeholder=False):
    """
    copy a local file (eg /tmp/pylons-upload-245145.dat) to the warehouse
    (eg S3:cb-wh:media/cade1361, ./civicboom/public/warehouse/media/ca/de/cade1361)
    """

    if not hash:
        hash = hash_file(src)

    log.info("Copying %s/%s (%s) to %s warehouse" % (warehouse, hash, filename, config["warehouse.type"]))

    if config["warehouse.type"] == "local":  #  or not config.get('online', True):  # hrm, tests with s3 access are nice, sometimes...
        dest = "/tmp/warehouse/%s/%s" % (warehouse, hash)
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
        shutil.copy(src, dest)

    elif config["warehouse.type"] == "s3":  # pragma: no cover - online services aren't active in test mode
        connection = S3Connection(config["api_key.aws.access"], config["api_key.aws.secret"])
        bucket = connection.get_bucket(config["warehouse.s3.bucket"])

        key = Key(bucket)
        key.key = warehouse+"/"+hash
        metadata = {
            'Content-Type': magic.from_file(src, mime=True),
            'Cache-Control': 'no-cache' if placeholder else 'public, max-age=31536000',
            #'Expires': 'Sun, 17 Mar 2023 17:48:53 GMT', # FIXME: now() + 1 year
            'Content-Disposition': 'inline; filename='+__http_escape(filename) if filename else 'inline',
        }

        if key.exists():
            log.warning("%s/%s already exists; updating metadata only" % (warehouse, hash))
            key.copy(bucket.name, key.key, metadata=metadata)
            key.set_acl('public-read')
        else:
            key.set_contents_from_filename(src, headers=metadata)
            key.set_acl('public-read')

    elif config["warehouse.type"] == "ssh":  # pragma: no cover - online services aren't active in test mode
        log.error("SSH warehouse not implemented")
        #scp = SCPClient(SSHTransport("static.civicboom.com"))
        #scp.put(src, "~/staticdata/%s/%s/%s/%s" % (warehouse, hash[0:1], hash[2:3], hash))

    elif config["warehouse.type"] == "null":  # pragma: no cover - online services aren't active in test mode
        pass

    else:  # pragma: no cover - online services aren't active in test mode
        log.warning("Unknown warehouse type: "+config["warehouse.type"])

    return hash


def hash_file(file, method="sha1"):
    """
    Hash a file in a way that the warehouse likes (reading small chunks
    and applying sha1 to them)

    Can accept a file object stream or a string filename

    If a stream is present it will return the stream to it's original position
    """

    # Check to see if file is a cgi.FieldStore object and extract the open file obj
    if hasattr(file,"file"):
        file = file.file

    # If file if an open stream already, get the files current position to return to at the end
    file_pos = None
    if hasattr(file,"read") and hasattr(file,"seek") and hasattr(file,"tell"):
        file_pos = file.tell()
        file.seek(0)
    # If not an existing open stream then open a new stream
    else:
        file = open(file)

    # calculate the hash, 64KB at a time
    hash = hashlib.new(method)
    data = "x"
    while data:
        data = file.read(1024 * 64)
        hash.update(data)

    # move the file pos back to where it started (if it was already open)
    if file_pos != None:
        file.seek(file_pos)
    else:
        file.close()
    return hash.hexdigest()


def __http_escape(text):
    """
    escape the data in a way that makes it safe to include in an HTTP header
    """
    return re.sub("[^a-zA-Z0-9\.-]", "_", text)
