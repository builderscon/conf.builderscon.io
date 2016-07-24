"""abstracts caching layer"""

import pickle
import redis

class Redis(object):
    def __init__(self, host, port, db):
        self.redis = redis.Redis(host=host, port=port, db=db)

    def set(self, key, val, expires=0):
        self.redis.setex(key, pickle.dumps(val), expires)

    def get(self, key):
        thing = self.redis.get(key)
        if not thing:
            return None

        return pickle.loads(thing)
