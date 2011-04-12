"""

http://chrismoos.com/2009/03/04/pylons-worker-threads/
"""

from Queue import Queue
from threading import Thread
from time import sleep


import logging
log = logging.getLogger(__name__)

_workers           = []
_worker_queue      = Queue()
_process_functions = {}


def add_process_function(name, f):
    _process_functions[name] = f

from civicboom.lib.worker_threads.send_message  import send_message
from civicboom.lib.worker_threads.process_media import process_media
add_process_function('process_media', process_media)
add_process_function('send_message' , send_message )



class MediaThread(Thread):
    def run(self):
        log.info('Media processing thread is running.')
        live = True

        while live:
            task = _worker_queue.get()
            try:
                task_type = task.pop("task")
                log.info('Starting task: %s (%s) [approx %d left]' % (task_type, task, _worker_queue.qsize()))
                if task_type in _process_functions:
                    _process_functions[task_type](**task)
                #if task_type == "process_media":
                #    process_media(**task)
                #if task_type == "send_message":
                #    send_message(**task)
                if task_type == "die":
                    live = False
            except Exception as e:
                log.exception('Error in worker thread:')
            _worker_queue.task_done()
            sleep(3)


def start_worker(count=3):
    log.info('Starting worker threads.')
    for n in range(count):
        worker = MediaThread()
        worker.daemon = True
        worker.name = "Worker %d" % (len(_workers)+1)
        worker.start()
        _workers.append(worker)


def stop_worker():
    log.info('Stopping worker threads.')
    if _workers:
        for worker in _workers:
            add_job({"task": "die"})
        for worker in _workers:
            worker.join()
            _workers.remove(worker)


def add_job(job):
    log.info('Adding job to worker queue: %s' % job["task"])
    if not _workers:
        start_worker()
    _worker_queue.put(job)


    


