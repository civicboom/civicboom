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


media_queue = Queue()

class MediaThread(Thread):
    def run(self):
        log.info('Media processing thread is running.')

        while True:
            task = media_queue.get()
            try:
                task_type = task.pop("task")
                log.info('Starting task: %s' % (task_type, ))
                if task_type == "process_media":
                    process_media(**task)
            except Exception, e:
                log.exception('Error in media processor thread:')
            media_queue.task_done()
            sleep(3)

def start_worker():
    worker = MediaThread()
    worker.daemon = True
    worker.start()


def _ffmpeg(self, args):
    """
    Convenience function to run ffmpeg and log the output
    """
    ffmpeg = "/usr/bin/ffmpeg" # FIXME: config variable?
    cmd = [ffmpeg, ] + args
    log.info(" ".join(cmd))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.communicate()
    log.debug("stdout: "+output[0])
    log.debug("stderr: "+output[1])
    log.debug("return: "+str(proc.returncode))

def process_media(config, tmp_file, file_hash, file_type, file_name, delete_tmp):
    # Get the thumbnail processed and uploaded ASAP
    if file_type == "image":
        processed = tempfile.NamedTemporaryFile(suffix=".jpg")
        size = 128, 128 # FIXME: config value?
        im = Image.open(tmp_file)
        if im.mode != "RGB":
            im = im.convert("RGB")
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(processed.name, "JPEG")
        wh.copy_to_warehouse(processed.name, "media-thumbnail", file_hash, "thumb.jpg", config)
        processed.close()
    elif file_type == "audio":
        # audio has no thumb; what is displayed to the user is
        # a player plugin
        pass
    elif file_type == "video":
        processed = tempfile.NamedTemporaryFile(suffix=".jpg")
        size = 128, 128 # FIXME: config value?
        _ffmpeg([
            "-y", "-i", tmp_file,
            "-an", "-vframes", "1", "-r", "1",
            "-s", "%dx%d" % (size[0], size[1]),
            "-f", "image2", processed.name
        ])
        wh.copy_to_warehouse(processed.name, "media-thumbnail", file_hash, "thumb.jpg", config)
        processed.close()

    # next most important, the original
    wh.copy_to_warehouse(tmp_file, "media-original", file_hash, file_name, config)

    # FIXME: turn tmp_file into something suitable for web viewing
    if file_type == "image":
        processed = tempfile.NamedTemporaryFile(suffix=".jpg")
        size = 480, 360
        im = Image.open(tmp_file)
        if im.mode != "RGB":
            im = im.convert("RGB")
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(processed.name, "JPEG")
        wh.copy_to_warehouse(processed.name, "media", file_hash, file_name, config)
        processed.close()
    elif file_type == "audio":
        processed = tempfile.NamedTemporaryFile(suffix=".ogg")
        _ffmpeg(["-y", "-i", tmp_file, "-ab", "192k", processed.name])
        wh.copy_to_warehouse(processed.name, "media", file_hash, file_name, config)
        processed.close()
    elif file_type == "video":
        processed = tempfile.NamedTemporaryFile(suffix=".flv")
        size = 480, 360
        _ffmpeg([
            "-y", "-i", tmp_file,
            "-ab", "56k", "-ar", "22050",
            "-qmin", "2", "-qmax", "16",
            "-b", "320k", "-r", "15",
            "-s", "%dx%d" % (size[0], size[1]),
            processed.name
        ])
        wh.copy_to_warehouse(processed.name, "media", file_hash, file_name, config)
        processed.close()

    if delete_tmp:
        os.unlink(tmp_file)


