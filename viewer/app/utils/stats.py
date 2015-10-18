from datetime import datetime as dt
from redis import Redis

def convert_sample(raw_sample):
  sample = eval(raw_sample)
  if sample.has_key('ts'):
    sample['ts'] = dt.fromtimestamp(float('%d.%d' % (sample['ts'])))
  return sample

def get_data(key):
  r = Redis()
  return map(lambda x:convert_sample(x), r.lrange(key, 0, -1))
