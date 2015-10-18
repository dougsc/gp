
class FunctionSet:
  NODE_TYPE = 'function'

  def __init__(self):
    self.function_set = []

  def add_function(self, name, func_ref, arity):
    self.function_set.append({'node_type': self.NODE_TYPE, 'name': name, 'function': func_ref, 'arity': arity})

  def get(self):
    return self.function_set
