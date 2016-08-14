"""abstracts caching layer"""

import pickle
import redis
import os
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/') or os.getenv('SERVER_SOFTWARE', '').startswith('Development/'):
    from google.appengine.api import memcache
else:
    import memcache

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

class Memcached:
    def __init__(self, servers=[], debug=0):
        if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/') or os.getenv('SERVER_SOFTWARE', '').startswith('Development/'):
            self.client = memcache
        else:
            def server_str(server):
                host = server.get('host')
                port = server.get('port')
                if not host:
                    raise Exception("host missing in memcache servers settings" )
                elif not port:
                    raise Exception("port missing in memcache servers settings" )
                else:
                    return str(  host + ':' + port )

            if not servers:
                raise Exception("servers missing in memcache settings")
            else:
                server_settings = map( server_str, servers )
            self.client = memcache.Client(server_settings, debug)

    def set(self, key, val, expires=0):
        self.client .set(key, val, expires)

    def get(self, key):
        return self.client.get(key)

