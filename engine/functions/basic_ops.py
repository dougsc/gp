from numpy import product, average

def add_functions(function_set, arity):
  function_set.add_function(name='max<%d>' % arity, func_ref=f_max, arity=arity) 
  function_set.add_function(name='min<%d>' % arity, func_ref=f_min, arity=arity) 
  function_set.add_function(name='sum<%d>' % arity, func_ref=f_sum, arity=arity) 
  function_set.add_function(name='prod<%d>' % arity, func_ref=f_prod, arity=arity) 
  function_set.add_function(name='ave<%d>' % arity, func_ref=f_ave, arity=arity) 
  function_set.add_function(name='median<%d>' % arity, func_ref=f_median, arity=arity) 

def f_max(*args):
  return max(args)

def f_min(*args):
  return min(args)

def f_sum(*args):
  return sum(args)

def f_prod(*args):
  return product(*args)

def f_ave(*args):
  return average(*args)

def f_median(*args):
  return median(*args)
