
class TerminalSet:
  NODE_TYPE = 'terminal'
  @classmethod
  def is_terminal_value(cls, node):
    return node['node_type'] == cls.NODE_TYPE and node.has_key('value') and (node['type'] in ['int', 'float'])

  @classmethod
  def terminal_value(cls, value):
    return {'node_type': cls.NODE_TYPE, 'name': str(value), 'value': value, 'type': type(value).__name__}

  def __init__(self):
    self.terminal_set = []

  def add_terminal_value(self, name, value):
    self.terminal_set.append({'node_type': self.NODE_TYPE, 'name': name, 'value': value, 'type': type(value).__name__})

  def add_terminal_function(self, name, func_ref, value_type, args=[]):
    self.terminal_set.append({'node_type': self.NODE_TYPE, 'name': name, 'function': func_ref, 'type': value_type, 'args': args})

  def add_terminal_function_to_value(self, func_ref, args=[]):
    self.terminal_set.append({'node_type': self.NODE_TYPE, 'function': func_ref, 'args': args})

  def get(self):
    return self.terminal_set
