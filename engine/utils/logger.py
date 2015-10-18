
import logging
import os

class GP_Logger:
  LOG_DIR = '/Users/dclark/code/logs'
  @classmethod
  def logger(cls, name):
    logger = logging.getLogger(name)
    if len(logger.handlers) == 0:
      # initialize the logger
      print 'creating new logger for: %s' % (name)
      logger.setLevel(logging.DEBUG)

      fileLogger = logging.FileHandler(os.path.join(cls.LOG_DIR, 'gp-%s.log' % (name)))
      formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
      fileLogger.setFormatter(formatter)

      logger.addHandler(fileLogger)
    return logger
