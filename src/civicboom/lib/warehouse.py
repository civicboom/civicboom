
from pylons import config

import os
import shutil
import hashlib
import magic
import logging
import re

from boto.s3.connection import S3Connection
from boto.s3.key import Key

log = logging.getLogger(__name__)


def copy_to_local_warehouse(src, warehouse, hash):
    """
    copy a local file (eg /tmp/pylons-upload-245145.dat) to the warehouse
    (eg ./civicboom/public/warehouse/media/ca/de/cade1361)
    """
    
    def copyCGIFile(cgi_fileobj, dest_filename):
        """
        Relocate a file from temp upload (a cgi.FieldStorage object) to local file
        Reference: Definative Guide to Pylons - pg99
        """        
        dest_fileobj = open(dest_filename,'wb')
        shutil.copyfileobj(cgi_fileobj.file, dest_fileobj)
        cgi_fileobj.file.close()
        dest_fileobj.close()
        return dest_fileobj.name
    
    dest = "./civicboom/public/warehouse/%s/%s/%s/%s" % (warehouse, hash[0:2], hash[2:4], hash)
    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))

    if hasattr(src,'file'): copyCGIFile(src, dest) # If src is a cgi.FiledStore object with an open filestream
    else                  : shutil.copy(src, dest)
    return dest


def copy_to_remote_warehouse(warehouse, hash, filename=None):
    """
    copy a locally warehoused file to a remote mirror
    """
    src = "./civicboom/public/warehouse/%s/%s/%s/%s" % (warehouse, hash[0:2], hash[2:4], hash)

    if config["warehouse"] == None or config["warehouse"] == "":
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


def hash_file(file, method="sha1"):
    """
    Hash a file in a way that the warehouse likes (reading small chunks
    and applying sha1 to them)
    
    Can accept a file object stream or a string filename
    
    If a stream is present it will return the stream to it's original position
    """
    file_pos = None
    # Check to see if file is a cgi.FieldStore object and extract the open file obj
    if hasattr(file,"file"): file = file.file
    # If file if an open stream already, get the files current position to return too at the end
    if hasattr(file,"read") and hasattr(file,"seek") and hasattr(file,"tell"): 
        file_pos = file.tell()
    # If not an existing open stream then open a new stream
    else: 
        file = open(file)
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


