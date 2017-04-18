import redis
import rediscluster
import flask_session

def build(backend, cfg):
    if backend == 'Redis':
        r = redis.Redis(**cfg.section('REDIS_INFO'))
        return flask_session.RedisSessionInterface(r, key_prefix="session", use_signer=True)
    elif backend == 'RedisCluster':
        r = rediscluster.client.RedisCluster(**cfg.section('REDIS_CLUSTER'))
        return flask_session.RedisSessionInterface(r, key_prefix="session", use_signer=True)
   
    raise Exception('Unknown backend "%s"' % backend)

