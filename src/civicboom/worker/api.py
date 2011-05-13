"""
A genericish worker API

for single-node, single-threaded:
    call add_job() whenever you want a job done

for single-node, multi-threaded:
    call start_worker() to spawn some background threads
    call add_job() whenever you want a job done

for multi-node:
    master node:
        call init_queue() with a Queue-like object
        call add_job() whenever you want a job done
    worker nodes:
        call init_queue() with a Queue-like object
        call run_worker() to run all jobs in the queue and wait for more
"""

from Queue import Queue
from threading import Thread
from time import sleep


import logging
log = logging.getLogger(__name__)

_workers           = []
_worker_queue      = None
_worker_functions = {}

config = {}
setup = None
teardown = None


##############################################################################
# Shared API

def add_worker_function(name, f):
    _worker_functions[name] = f

def init_queue(q):
    global _worker_queue
    _worker_queue = q


##############################################################################
# Client API

def add_job(job):
    """
    Adds a job to the worker's queue if there is one; if no queues have
    been initialised, runs the job directly
    """
    if _worker_queue and job["task"] not in ["send_notification", "profanity_check"]:
        log.info('Adding job to worker queue: %s' % job["task"])
        _worker_queue.put(job)
    else:
        log.info('Running job in foreground: %s' % job["task"])
        # in production, jobs are encoded for the queue; in testing, we want
        # un-encodable jobs to fail
        import json; json.dumps(job)
        run_one_job(job)


##############################################################################
# Server API

def run_one_job(task):
    live = True
    try:
        if setup:
            setup(task)
        task_type = task.pop("task")
        log.info('Starting task: %s (%s)' % (task_type, task))
        if task_type in _worker_functions:
            _worker_functions[task_type](**task)
        elif task_type == "die":
            live = False
        else:
            log.error("Unrecognised task type: %s" % task_type)
    except Exception as e:
        log.exception('Error in worker thread:')
        sleep(3)
    finally:
        if teardown:
            teardown(task)
    return live


def run_worker():
    live = True
    while live:
        try:
            task = _worker_queue.get()
            live = run_one_job(task)
            _worker_queue.task_done()
        except Exception:
            log.exception("Error talking to queue; sleeping before reconnect")
            sleep(3)


class WorkerThread(Thread):
    def run(self):
        log.info('Media processing thread is running.')
        run_worker()


def start_worker(count=3):
    stop_worker()
    init_queue(Queue())
    log.info('Starting worker threads.')
    for n in range(count):
        worker = WorkerThread()
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

