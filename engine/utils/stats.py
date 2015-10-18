from redis import Redis

class RedisWrap:
  def __init__(self):
    try:
      self.redis_cli = Redis()
      self.redis_cli.info()
    except Exception, e:
      print 'failed to connect to redis: %s' % (str(e))
      self.redis_cli = None

  def append(self, key, value, timestamp=False):
    if self.redis_cli:
      if timestamp:
        value['ts'] = self.redis_cli.time()
      res = self.redis_cli.rpush(key, value)

  def delete(self, key):
    if self.redis_cli:
      self.redis_cli.delete(key)

class Stats:
  def __init__(self, key_root):
    self.stats_cli = RedisWrap()
    self.key_root = key_root

  def _get_full_key(self, key):
    return '%s:%s' % (self.key_root, key)

  def init_series(self, key):
    key_list = isinstance(key, list) and key or [key]
    map(lambda x:self.stats_cli.delete(self._get_full_key(x)), key_list)

  def add_to_series(self, key, value, timestamp=False):
    self.stats_cli.append(self._get_full_key(key), value, timestamp)
