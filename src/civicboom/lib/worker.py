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
            except Exception, e:
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

def process_media(tmp_file, file_hash, file_type, file_name, delete_tmp):
    # Get the thumbnail processed and uploaded ASAP
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

    # next most important, the original
    wh.copy_to_warehouse(tmp_file, "media-original", file_hash, file_name)

    if file_type == "image":
        processed = tempfile.NamedTemporaryFile(suffix=".jpg")
        size = (int(config["media.media.width"]), int(config["media.media.height"]))
        im = Image.open(tmp_file)
        if im.mode != "RGB":
            im = im.convert("RGB")
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(processed.name, "JPEG")
        wh.copy_to_warehouse(processed.name, "media", file_hash, file_name)
        processed.close()
    elif file_type == "audio":
        processed = tempfile.NamedTemporaryFile(suffix=".ogg")
        _ffmpeg(["-y", "-i", tmp_file, "-ab", "192k", processed.name])
        wh.copy_to_warehouse(processed.name, "media", file_hash, file_name)
        processed.close()
    elif file_type == "video":
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
        wh.copy_to_warehouse(processed.name, "media", file_hash, file_name)
        processed.close()

    if delete_tmp:
        os.unlink(tmp_file)

    from pylons import config
    import memcache
    m = memcache.Client([config['service.memcache.server']], debug=0)
    m.delete(str("media_processing_"+file_hash))


