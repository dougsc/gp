
#  def get_terminal_set(self):
#  def get_function_set(self):
#  def initialize(self):
#  def next(self):
#  def function_lookup(self):
#  def error(self, value):

from engine import *
from random import randint
from os import path
import csv
from engine.function_set import FunctionSet
import engine.functions.signs as gp_f_signs
import engine.functions.trig as gp_f_trig
from engine.experiment import Experiment

class LineExp(Experiment):
  _target_data = None
  function_set = FunctionSet()
  gp_f_signs.add_functions(function_set)
  gp_f_trig.add_functions(function_set)
  terminal_set = TerminalSet()
  terminal_set.add_terminal_function(name='x_var', func_ref='get_x', value_type=int.__name__)
  terminal_set.add_terminal_function_to_value(func_ref=randint, args=[-9,9])

  def __init__(self, filename):
    self.current_data_index = 0
    self.read_target_data(filename)

  @classmethod
  def set_target_data(cls, data):
    assert cls._target_data == None, 'attempt to reset target data'
    cls._target_data = data

  @classmethod
  def read_target_data(cls, filename):
    if cls._target_data != None:
      return

    fh = open(filename)
    (_, ext) = path.splitext(filename)
    if ext == '.csv':
      csv_data = csv.reader(fh)
      cls.set_target_data(map(lambda raw_data:map(lambda x:float(x), raw_data), csv_data))
    else:
      raise Exception('unknonw data file type: %s' % (ext))

  def get_x(self):
    return self.index()

  def initialize(self):
    self.current_data_index = 0

  def next(self):
    if (self.current_data_index + 1) < len(self._target_data):
      self.current_data_index += 1
      return True
    return False

  def index(self):
    return self._target_data[self.current_data_index][0]

  def norm_error(self, value):
    return abs(self.error(value))

  def error(self, value):
    return (self._target_data[self.current_data_index][1] - value)
