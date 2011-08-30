import logging
import json
from beaker.exceptions import InvalidCacheBackendError
from beaker.container import NamespaceManager, Container
from beaker.synchronization import file_synchronizer
from beaker.util import verify_directory
from beaker.exceptions import MissingCacheParameter

try:
    from redis import Redis
except ImportError:
    raise InvalidCacheBackendError("Redis cache backend requires the 'redis' library")

try:
    import cPickle as pickle
except:
    import pickle

log = logging.getLogger(__name__)


def redis_from_url(url):
    conn_params = {}
    parts = url.split('?', 1)
    url = parts[0]
    if len(parts) > 1:
        conn_params = dict(p.split('=', 1) for p in parts[1].split('&'))

    if ":" in url:
        host, port = url.split(':', 1)
        port = int(port)
    else:
        host = url
        port = 6379

    return Redis(host, port, **conn_params)


class RedisQueue(object):
    """An abstract FIFO queue"""
    def __init__(self, redis, queue_id=None):
        self.r = redis
        self.queue_id = "queue:%s" % (queue_id or self.r.incr("queue_space"))

    def put(self, element):
        """Push an element to the tail of the queue"""
        self.r.rpush(self.queue_id, json.dumps(element))

    def get(self):
        """Pop an element from the head of the queue"""
        return json.loads(self.r.blpop(self.queue_id)[1])

    def qsize(self):
        return self.r.llen(self.queue_id)

    def task_done(self):
        pass


class NoSqlManager(NamespaceManager):
    def __init__(self, namespace, url=None, data_dir=None, lock_dir=None, **params):
        NamespaceManager.__init__(self, namespace)

        if not url:
            raise MissingCacheParameter("url is required")

        if lock_dir:
            self.lock_dir = lock_dir
        elif data_dir:
            self.lock_dir = data_dir + "/container_tcd_lock"
        else:
            self.lock_dir = None

        if self.lock_dir:
            verify_directory(self.lock_dir)

        conn_params = {}
        parts = url.split('?', 1)
        url = parts[0]
        if len(parts) > 1:
            conn_params = dict(p.split('=', 1) for p in parts[1].split('&'))

        if ":" in url:
            host, port = url.split(':', 1)
            port = int(port)
        else:
            host = url
            port = None

        self.open_connection(host, port, **conn_params)

    def open_connection(self, host, port):
        self.db_conn = None

    def get_creation_lock(self, key):
        return file_synchronizer(
            identifier ="tccontainer/funclock/%s" % self.namespace,
            lock_dir = self.lock_dir)

    def _format_key(self, key):
        return self.namespace + '_'

    def __getitem__(self, key):
        return pickle.loads(self.db_conn.get(self._format_key(key)))

    def __contains__(self, key):
        return self.db_conn.has_key(self._format_key(key))

    def has_key(self, key):
        return key in self

    def set_value(self, key, value):
        self.db_conn[self._format_key(key)] =  pickle.dumps(value)

    def __setitem__(self, key, value):
        self.set_value(key, value)

    def __delitem__(self, key):
        del self.db_conn[self._format_key(key)]

    def do_remove(self):
        self.db_conn.clear()

    def keys(self):
        return self.db_conn.keys()


class RedisManager(NoSqlManager):
    def __init__(self, namespace, url=None, data_dir=None, lock_dir=None, **params):
        NoSqlManager.__init__(self, namespace, url=url, data_dir=data_dir, lock_dir=lock_dir, **params)

    def open_connection(self, host, port, **params):
        if not port:
            port = 6379
        self.db_conn = Redis(host=host, port=port, db=1, **params)

    def __contains__(self, key):
        #log.debug('%s contained in redis cache (as %s) : %s'%(key, self._format_key(key), self.db_conn.exists(self._format_key(key))))
        return self.db_conn.exists(self._format_key(key))

    def set_value(self, key, value):
        key = self._format_key(key)
        self.db_conn.set(key, pickle.dumps(value))

    def __delitem__(self, key):
        key = self._format_key(key)
        self.db_conn.delete(self._format_key(key))

    def _format_key(self, key):
        return 'beaker:%s:%s' % (self.namespace, key.replace(' ', '\302\267'))

    def do_remove(self):
        for key in self.db_conn.keys('beaker:%s:*' % self.namespace):
            self.db_conn.delete(key)
        #self.db_conn.flush()

    def keys(self):
        raise self.db_conn.keys('beaker:%s:*' % self.namespace)


class RedisContainer(Container):
    namespace_manager = RedisManager
