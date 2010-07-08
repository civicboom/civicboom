
import os
import shutil
import hashlib


def copy_to_local_warehouse(src, warehouse, hash):
    """
    copy a local file (eg /tmp/pylons-upload-245145.dat) to the warehouse
    (eg ./civicboom/public/warehouse/media/ca/de/cade1361)
    """
    dest = "./civicboom/public/warehouse/%s/%s/%s/%s" % (warehouse, hash[0:2], hash[2:4], hash)
    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
    shutil.copy(src, dest)


def copy_to_remote_warehouse(warehouse, hash):
    """
    copy a locally warehoused file to a remote mirror
    """
    src = "./civicboom/public/warehouse/%s/%s/%s/%s" % (warehouse, hash[0:2], hash[2:4], hash)

    # copy to mirror via SCP
    #scp = SCPClient(SSHTransport("static.civicboom.com"))
    #scp.put(self.name, "~/staticdata/%s/%s/%s" % (hash[0:1], hash[2:3], hash))

    # copy to amazon s3
    # ...


def hash_file(name, method="sha1"):
    """
    hash a file in a way that the warehouse likes (reading small chunks
    and applying sha1 to them)
    """
    fp = open(name)
    hash = hashlib.new(method)
    data = "x"
    while data:
        data = fp.read(8192)
        hash.update(data)
    fp.close()
    return hash.hexdigest()
