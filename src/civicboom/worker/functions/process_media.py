import tempfile
import Image
import os
import os.path
import subprocess

import cbutils.warehouse as wh
from cbutils.worker import config
from civicboom.model.meta import Session
from civicboom.model import Media

import logging
log = logging.getLogger(__name__)


def _ffmpeg(args):
    """
    Convenience function to run ffmpeg and log the output
    """
    ffmpeg = config["media.ffmpeg"]
    cmd = [ffmpeg, ] + args
    log.info(" ".join(cmd))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.communicate()
    log.debug("stdout: %s", output[0])
    log.debug("stderr: %s", output[1])
    log.debug("return: %d", proc.returncode)


def _reformed(name, ext):
    return os.path.splitext(name)[0] + "." + ext


def process_media(tmp_file, file_hash, file_type, file_name, delete_tmp):
    db_object = Session.query(Media).filter(Media.hash==file_hash).first()

    from cbutils.redis_ import redis_from_url
    m               = redis_from_url(config['worker.queue.url'])
    status_key    = str("media_processing_"+file_hash)
    status_expire = int(config['media.processing.status_expire_time'])
    
    # temp hack while bulk importing
    if config['warehouse.type'] == 's3':
        from boto.s3.connection import S3Connection
        from boto.s3.key import Key
        connection = S3Connection(config["api_key.aws.access"], config["api_key.aws.secret"])
        bucket = connection.get_bucket(config["warehouse.s3.bucket"])
        key = Key(bucket)
        key.key = "media-original/"+file_hash
        if key.exists():
            log.info("media %s (%s) already processed, skipping" % (file_hash, file_name))
            return

    # AllanC - in time the memcache could be used to update the user with percentage information about the status of the processing
    #          This is returned to the user with a call to the media controller

    m.setex(status_key, "encoding media", status_expire)
    if file_type == "image":
        try:
            import pexif
            (lat, lon) = pexif.JpegFile.fromFile(tmp_file).get_geo()
            db_object.location = "SRID=4326;POINT(%f %f)" % (lon, lat)
        except Exception as e:
            pass
        processed = tempfile.NamedTemporaryFile(suffix=".jpg")
        size = (int(config["media.media.width"]), int(config["media.media.height"]))
        im = Image.open(tmp_file)
        if im.mode != "RGB":
            im = im.convert("RGB")
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(processed.name, "JPEG")
        m.setex(status_key, "copying image", status_expire)
        wh.copy_to_warehouse(processed.name, "media", file_hash, _reformed(file_name, "jpg"))
        processed.close()
    elif file_type == "audio":
        processed = tempfile.NamedTemporaryFile(suffix=".flv")
        _ffmpeg(["-y", "-i", tmp_file, "-ar", "44100", processed.name])
        m.setex(status_key, "copying audio", status_expire)
        wh.copy_to_warehouse(processed.name, "media", file_hash, _reformed(file_name, "flv"))
        processed.close()
    elif file_type == "video":
        log.debug("encoding video to flv")
        processed = tempfile.NamedTemporaryFile(suffix=".flv")
        size = (int(config["media.media.width"]), int(config["media.media.height"]))
        _ffmpeg([
            "-y", "-i", tmp_file, "-ar", "22050",
            "-s", "%dx%d" % (size[0], size[1]),
            #"-b", "%s" % (int(config["media.video.bitrate"]) * 1024), # AllanC - had to rem this out because the flash player dies with other bitrates. Investigate later properly
            processed.name
        ])
        m.setex(status_key, "copying video", status_expire)
        #log.debug("START copying processed video to warehouse %s:%s (%dKB)" % (file_name, processed.name, os.path.getsize(processed.name)/1024))
        wh.copy_to_warehouse(processed.name, "media", file_hash, _reformed(file_name, "flv"))
        #log.debug("END   copying processed video to warehouse %s:%s" % (file_name, processed.name))
        # TODO:
        # for RSS 2.0 'enclosure' we need to know the length of the processed file in bytes
        # We should include here a call to database to update the length field
        db_object.filesize = os.path.getsize(processed.name)
        processed.close()

    # Get the thumbnail processed and uploaded ASAP
    m.setex(status_key, "thumbnail", status_expire)
    if file_type == "image":
        processed = tempfile.NamedTemporaryFile(suffix=".jpg")
        size = (int(config["media.thumb.width"]), int(config["media.thumb.height"]))
        im = Image.open(tmp_file)
        if im.mode != "RGB":
            im = im.convert("RGB")
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(processed.name, "JPEG")
        wh.copy_to_warehouse(processed.name, "media-thumbnail", file_hash, "thumb.jpg")
        processed.close()
    elif file_type == "audio":
        # audio has no thumb; what is displayed to the user is
        # a player plugin
        pass
    elif file_type == "video":
        processed = tempfile.NamedTemporaryFile(suffix=".jpg")
        size = (int(config["media.thumb.width"]), int(config["media.thumb.height"]))
        _ffmpeg([
            "-y", "-i", tmp_file,
            "-an", "-vframes", "1", "-r", "1",
            "-s", "%dx%d" % (size[0], size[1]),
            "-f", "image2", processed.name
        ])
        wh.copy_to_warehouse(processed.name, "media-thumbnail", file_hash, "thumb.jpg")
        processed.close()


    # least important, the original
    #log.debug("START copying original media to warehouse %s:%s (%dKB)" % (file_name, tmp_file, os.path.getsize(tmp_file)/1024) )
    m.setex(status_key, "copying original video", status_expire)
    wh.copy_to_warehouse(tmp_file, "media-original", file_hash, file_name)
    #log.debug("END   copying original media to warehouse %s:%s" % (file_name, tmp_file) )


    if delete_tmp:
        os.unlink(tmp_file)

    m.delete(status_key)
    log.debug("deleting status_key %s" % status_key)

    Session.commit()

    return True
