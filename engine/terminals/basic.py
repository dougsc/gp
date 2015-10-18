from terminal_set import TerminalSet
from random import randint

def t_basic_terminals():
  ts = TerminalSet(__name__)
  ts.add_terminal_function(name='rand_int', func_ref=t_basic_rand_int, value_type='int', args=[0,9])
  return ts

def t_basic_rand_int(lower_bound, upper_bound):
  return randint(lower_bound, upper_bound) 
