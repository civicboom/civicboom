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
_local_queue       = []
_worker_functions = {}

config = {}
setup = None
teardown = None

def _default_teardown(task, success, exception):
    if not success:
        log.exception('Error in worker thread:')
        sleep(3)

teardown = _default_teardown


##############################################################################
# Shared API

def add_worker_function(name, f):
    _worker_functions[name] = f

def init_queue(q):
    global _worker_queue
    _worker_queue = q


##############################################################################
# Client API

def add_job(job, autoflush=False):
    """
    Queue a job to be run; autoflush is false so that eg jobs involving
    database objects can be added to the queue, the request finishes,
    the database connection is committed, and *then* the jobs are started.
    """
    global _local_queue
    _local_queue.append(job)
    if autoflush:
        flush()


def flush():
    """
    Adds locally queued jobs to the central job list
    """
    while _local_queue:
        try:
            job = _local_queue.pop(0)
            if _worker_queue:
                log.info('Adding job to worker queue: %s' % job["task"])
                _worker_queue.put(job)
            else:
                log.info('Running job in foreground: %s' % job["task"])
                # in production, jobs are encoded for the queue; in testing, we want
                # un-encodable jobs to fail
                import json; json.dumps(job)
                run_one_job(job)
        except Exception as e:
            log.exception("Exception processing job:")


##############################################################################
# Server API

def run_one_job(job_details):
    live = True
    job_success = None
    next_job = None
    exception = None
    try:
        if setup:
            setup(job_details)
        function_name = job_details.pop("task")
        if "next_job" in job_details:
            next_job = job_details.pop("next_job")
        log.debug('Starting job: %s (%s)' % (function_name, job_details))
        if function_name in _worker_functions:
            job_success = _worker_functions[function_name](**job_details)
        elif function_name == "die":
            live = False
            job_success = True
        else:
            log.error("Unrecognised job type: %s" % function_name)
            job_success = True
    except Exception as e:
        job_success = False
        exception = e
    finally:
        if teardown:
            teardown(job_details, job_success, exception)
        if job_success and next_job:
            run_one_job(next_job)
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

