
from pylons import config

import os
import shutil
import hashlib
import magic
import logging

from boto.s3.connection import S3Connection
from boto.s3.key import Key

log = logging.getLogger(__name__)


def copy_to_local_warehouse(src, warehouse, hash):
    """
    copy a local file (eg /tmp/pylons-upload-245145.dat) to the warehouse
    (eg ./civicboom/public/warehouse/media/ca/de/cade1361)
    """
    dest = "./civicboom/public/warehouse/%s/%s/%s/%s" % (warehouse, hash[0:2], hash[2:4], hash)
    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
    shutil.copy(src, dest)


def copy_to_remote_warehouse(warehouse, hash, filename=None):
    """
    copy a locally warehoused file to a remote mirror
    """
    src = "./civicboom/public/warehouse/%s/%s/%s/%s" % (warehouse, hash[0:2], hash[2:4], hash)

    if config["warehouse"] == None:
        log.info("Copying %s/%s (%s) to Null warehouse" % (warehouse, hash, filename))

    if config["warehouse"] == "s3":
        log.info("Copying %s/%s (%s) to S3 warehouse" % (warehouse, hash, filename))
        connection = S3Connection(config["aws_access_key"], config["aws_secret_key"])
        bucket = connection.get_bucket(config["s3_bucket_name"])
        key = Key(bucket)
        key.key = warehouse+"/"+hash
        key.set_metadata('Content-Type', magic.from_file(src, mime=True))
        if filename:
            key.set_metadata('Content-Disposition', 'inline; filename='+__http_escape(filename))
        key.set_contents_from_filename(src)
        key.set_acl('public-read')

    # copy to mirror via SCP
    #scp = SCPClient(SSHTransport("static.civicboom.com"))
    #scp.put(self.name, "~/staticdata/%s/%s/%s" % (hash[0:1], hash[2:3], hash))


def hash_file(name, method="sha1"):
    """
    hash a file in a way that the warehouse likes (reading small chunks
    and applying sha1 to them)
    """
    fp = open(name)
    hash = hashlib.new(method)
    data = "x"
    while data:
        data = fp.read(1024 * 64)
        hash.update(data)
    fp.close()
    return hash.hexdigest()


def __http_escape(text):
    """
    escape the data in a way that makes it safe to include in an HTTP header
    """
    return re.sub("[^a-zA-Z0-9\.-]", "_", text)


