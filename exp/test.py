
#  def get_terminal_set(self):
#  def get_function_set(self):
#  def initialize(self):
#  def next(self):
#  def function_lookup(self):
#  def error(self, value):

from engine import *
from random import randint
from engine.function_set import FunctionSet
import engine.functions.signs as gp_f_signs
from engine.experiment import Experiment

class TestExp(Experiment):
  function_set = FunctionSet()
  gp_f_signs.add_functions(function_set)
  terminal_set = TerminalSet()
  terminal_set.add_terminal_function(name='x_var', func_ref='get_x', value_type=int.__name__)
  terminal_set.add_terminal_function_to_value(func_ref=randint, args=[0,4])
  
  def __init__(self):
    self.x = 0

  def get_x(self):
    return self.x

  def initialize(self):
    self.x = -5

  def next(self):
    if self.x <= 5:
      self.x += 1
      return True
    return False

  def index(self):
    return self.x

  def norm_error(self, value):
    return abs(self.error(value))

  def error(self, value):
#    print 'value: %f, error: %f' % (value, abs(((self.x * self.x) + self.x + 1) - value))
    return (((self.x * self.x * self.x) + self.x + 1) - value)
