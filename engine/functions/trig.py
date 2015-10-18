
from math import tan,sin,cos

def add_functions(function_set):
  function_set.add_function(name='tan', func_ref=f_trig_tan, arity=1) 
  function_set.add_function(name='sin', func_ref=f_trig_sin, arity=1) 
  function_set.add_function(name='cos', func_ref=f_trig_cos, arity=1) 

def f_trig_tan(a):
  return tan(a)

def f_trig_sin(a):
  return sin(a)

def f_trig_cos(a):
  return cos(a)
