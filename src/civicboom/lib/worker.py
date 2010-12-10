"""

http://chrismoos.com/2009/03/04/pylons-worker-threads/
"""

from Queue import Queue
from threading import Thread
from time import sleep

import tempfile
import Image
import os
import subprocess
import civicboom.lib.services.warehouse as wh

from pylons import config

import logging
log = logging.getLogger(__name__)

_worker = None
_media_queue = Queue()


class MediaThread(Thread):
    def run(self):
        log.info('Media processing thread is running.')
        live = True

        while live:
            task = _media_queue.get()
            try:
                task_type = task.pop("task")
                log.info('Starting task: %s (%s)' % (task_type, str(task)))
                if task_type == "process_media":
                    process_media(**task)
                if task_type == "die":
                    live = False
            except Exception as e:
                log.exception('Error in media processor thread:')
            _media_queue.task_done()
            sleep(3)

def start_worker():
    log.info('Starting worker thread.')
    global _worker
    _worker = MediaThread()
    _worker.daemon = True
    _worker.name = "Worker"
    _worker.start()

def stop_worker():
    log.info('Stopping worker thread.')
    global _worker
    if _worker:
        add_job({"task": "die"})
        _worker.join()
        _worker = None

def add_job(job):
    log.info('Adding job to worker queue: %s' % job["task"])
    if not _worker:
        start_worker()
    _media_queue.put(job)


def _ffmpeg(args):
    """
    Convenience function to run ffmpeg and log the output
    """
    ffmpeg = config["media.ffmpeg"]
    cmd = [ffmpeg, ] + args
    log.info(" ".join(cmd))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.communicate()
    log.debug("stdout: "+output[0])
    log.debug("stderr: "+output[1])
    log.debug("return: "+str(proc.returncode))


def _update_media_length(hash, length):
    """
    Placeholder to update media file length in DB
    """
    #import database actions
    # update the record in db

def process_media(tmp_file, file_hash, file_type, file_name, delete_tmp):
    import memcache
    m               = memcache.Client(config['service.memcache.server'].split(), debug=0)
    memcache_key    = str("media_processing_"+file_hash)
    memcache_expire = int(config['media.processing.expire_memcache_time'])
    
    # AllanC - in time the memcache could be used to update the user with percentage information about the status of the processing
    #          This is returned to the user with a call to the media controller

    m.set(memcache_key, "encoding media", memcache_expire)
    if file_type == "image":
        processed = tempfile.NamedTemporaryFile(suffix=".jpg")
        size = (int(config["media.media.width"]), int(config["media.media.height"]))
        im = Image.open(tmp_file)
        if im.mode != "RGB":
            im = im.convert("RGB")
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(processed.name, "JPEG")
        m.set(memcache_key, "copying image", memcache_expire)
        wh.copy_to_warehouse(processed.name, "media", file_hash, file_name)
        processed.close()
    elif file_type == "audio":
        processed = tempfile.NamedTemporaryFile(suffix=".ogg")
        _ffmpeg(["-y", "-i", tmp_file, "-ab", "192k", processed.name])
        m.set(memcache_key, "copying audio", memcache_expire)
        wh.copy_to_warehouse(processed.name, "media", file_hash, file_name)
        processed.close()
    elif file_type == "video":
        log.debug("encoding video to flv")
        processed = tempfile.NamedTemporaryFile(suffix=".flv")
        size = (int(config["media.media.width"]), int(config["media.media.height"]))
        _ffmpeg([
            "-y", "-i", tmp_file,
            "-ab", "56k", "-ar", "22050",
            "-qmin", "2", "-qmax", "16",
            "-b", "320k", "-r", "15",
            "-s", "%dx%d" % (size[0], size[1]),
            processed.name
        ])
        m.set(memcache_key, "copying video", memcache_expire)
        log.debug("START copying processed video to warehouse %s:%s (%dKB)" % (file_name, processed.name, os.path.getsize(processed.name)/1024))
        wh.copy_to_warehouse(processed.name, "media", file_hash, file_name)
        log.debug("END   copying processed video to warehouse %s:%s" % (file_name, processed.name))
        # TODO:
        # for RSS 2.0 'enclosure' we need to know the length of the processed file in bytes
        # We should include here a call to database to update the length field
        #_update_media_length(file_hash, os.path.getsize(processed.name))
        processed.close()

    # Get the thumbnail processed and uploaded ASAP
    m.set(memcache_key, "thumbnail", memcache_expire)
    if file_type == "image":
        processed = tempfile.NamedTemporaryFile(suffix=".jpg")
        size = (int(config["media.thumb.width"]), int(config["media.thumb.height"]))
        #log.info('Opening image.') # FIXME: image.open() blocks while running setup-app from nosetests, but not from paster. wtf. See bug #45
        im = Image.open(tmp_file)
        #log.info('Checking mode.')
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


    # leist important, the original
    log.debug("START copying original media to warehouse %s:%s (%dKB)" % (file_name, tmp_file, os.path.getsize(tmp_file)/1024) )
    m.set(memcache_key, "copying original video", memcache_expire)
    wh.copy_to_warehouse(tmp_file, "media-original", file_hash, file_name)
    log.debug("END   copying original media to warehouse %s:%s" % (file_name, tmp_file) )


    if delete_tmp:
        os.unlink(tmp_file)

    m.delete(memcache_key)
    log.debug("deleting memcache %s" % memcache_key)


