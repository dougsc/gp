
def add_functions(function_set):
  function_set.add_function(name='add', func_ref=f_math_add, arity=2) 
  function_set.add_function(name='subtract', func_ref=f_math_sub, arity=2) 
  function_set.add_function(name='multiply', func_ref=f_math_times, arity=2) 
  function_set.add_function(name='divide', func_ref=f_math_divide, arity=2) 

def f_math_add(a, b):
  return a+b

def f_math_sub(a, b):
  return a-b

def f_math_times(a, b):
  return a*b

def f_math_divide(a, b):
  return b == 0 and 1 or float(a)/b

