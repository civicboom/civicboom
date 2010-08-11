
import os
import shutil
import hashlib
import magic
import logging
import re

from boto.s3.connection import S3Connection
from boto.s3.key import Key

log = logging.getLogger(__name__)


def copy_cgi_file(cgi_fileobj, dest_filename):
    """
    Relocate a file from temp upload (a cgi.FieldStorage object) to local file
    Reference: Definative Guide to Pylons - pg99
    """
    dest_fileobj = open(dest_filename,'wb')
    shutil.copyfileobj(cgi_fileobj.file, dest_fileobj)
    cgi_fileobj.file.close()
    dest_fileobj.close()
    return dest_fileobj.name


def copy_to_warehouse(config, src, warehouse, hash, filename=None):
    """
    copy a local file (eg /tmp/pylons-upload-245145.dat) to the warehouse
    (eg S3:cb-wh:media/cade1361, ./civicboom/public/warehouse/media/ca/de/cade1361)
    """

    # If src is a cgi.FieldStorage object with an open filestream
    temp_file = None
    if hasattr(src,'file'):
        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        copy_cgi_file(src, temp_file.name)
        src = temp_file.name

    if config["warehouse"] == "local":
        dest = "./civicboom/public/warehouse/%s/%s/%s/%s" % (warehouse, hash[0:2], hash[2:4], hash)
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
        shutil.copy(src, dest)

    elif config["warehouse"] == "s3":
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

    elif config["warehouse"] == "ssh":
        log.info("Copying %s/%s (%s) to SSH warehouse" % (warehouse, hash, filename))
        scp = SCPClient(SSHTransport("static.civicboom.com"))
        scp.put(self.name, "~/staticdata/%s/%s/%s/%s" % (warehouse, hash[0:1], hash[2:3], hash))

    else:
        log.warning("Unknown warehouse type: "+config["warehouse"])
        log.info("Copying %s/%s (%s) to Null warehouse" % (warehouse, hash, filename))

    if temp_file:
        temp_file.close()


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


