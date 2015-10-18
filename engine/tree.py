import random
from pprint import pformat
from copy import deepcopy
from utils.logger import GP_Logger
from terminal_set import TerminalSet

class Tree:
  @classmethod
  def log(cls):
    return GP_Logger.logger(cls.__name__)

  def __init__(self):
    self.terminal_set=None
    self.function_set=None
    self.function_bias=None
    self.max_depth=None
    self.tree = None

  def clone(self, clone_tree):
    assert clone_tree.tree != None, 'trying to clone from an uninitialized tree'
    self.terminal_set = clone_tree.terminal_set
    self.function_set = clone_tree.function_set
    self.function_bias = clone_tree.function_bias
    self.max_depth = clone_tree.max_depth
    self.tree = deepcopy(clone_tree.tree)

  def mutate(self, clone_tree):
    self.clone(clone_tree)
    mutation_node = random.choice(self.get_node_list())
    self.log().debug('mutating at node %s - current depth: %d' % (mutation_node['node']['name'], mutation_node['depth']))
    self._create_new_node(mutation_node['depth'], mutation_node)
    self.log().debug('node mutated to %s' % (mutation_node['node']['name']))
    self._add_layer(mutation_node)    

  def subtree_crossover(self, clone_tree, other_tree):
    self.clone(clone_tree)
    this_crossover_node = random.choice(self.get_node_list())
    other_crossover_node = random.choice(other_tree.get_node_list())
    self.log().debug('x-over node 1: %s (depth: %d), node 2: %s (depth: %d)' % (this_crossover_node['node']['name'], 
                                                                                this_crossover_node['depth'],
                                                                                other_crossover_node['node']['name'], 
                                                                                other_crossover_node['depth']))
    this_crossover_node['node'] = deepcopy(other_crossover_node['node'])
    this_crossover_node['lower_nodes'] = deepcopy(other_crossover_node['lower_nodes'])
    self.recalculate_depth(this_crossover_node['lower_nodes'], this_crossover_node['depth'] + 1)

  def create(self, terminal_set=[], function_set=[], function_bias=1, max_depth=3):
    self.terminal_set=terminal_set
    self.function_set=function_set
    self.function_bias=function_bias
    self.max_depth=max_depth

    self.tree = {}
    self._create_new_node(1, self.tree)
    self._add_layer(current_node=self.tree)

  def _create_new_node(self, depth, node):
    node_set = []
    if depth == 1:
      node_set = self.function_set
    elif depth >= self.max_depth:
      node_set = self.terminal_set
    else:
      node_set = self.function_set * self.function_bias + self.terminal_set

    chosen_node = random.choice(node_set)
    if not chosen_node.has_key('name'):
      # this needs converting to a named node
      value = chosen_node['function'](*chosen_node['args'])
      chosen_node = TerminalSet.terminal_value(value)

    node['node'] = chosen_node
    node['lower_nodes'] = []
    node['depth'] = depth

  def _add_layer(self, current_node):
    new_node_count = current_node['node'].has_key('arity') and current_node['node']['arity'] or 0
    self.log().debug('adding %d nodes below %s - current depth = %d' % (new_node_count, current_node['node']['name'], current_node['depth']))
    for i in range(new_node_count):
      new_node = {}
      self._create_new_node(current_node['depth'] + 1, new_node)
      current_node['lower_nodes'].append(new_node)

    map(lambda x:self._add_layer(x), current_node['lower_nodes'])

  def dump(self):
    print 'Tree: \n%s' % pformat(self.tree)

  def _dump_structure(self, from_nodes, to_nodes):
    for from_node in from_nodes:
      new_node = {'name': from_node['node']['name'], 'lower_nodes': []}
      to_nodes.append(new_node)
      self._dump_structure(from_node['lower_nodes'], new_node['lower_nodes'])

  def dump_structure(self):
    structure = {'name': self.tree['node']['name'], 'lower_nodes': []}
    self._dump_structure(self.tree['lower_nodes'], structure['lower_nodes'])
    return structure

  def execute_node(self, node, function_lookup, args=None):
    assert node.has_key('value') or node.has_key('function'), 'node does not have a function or value'
    value = None
    if node.has_key('value'):
      value = node['value']
    else:
      if args == None:
        args = node['args']
      if isinstance(node['function'], str):
        value = function_lookup.get_func(node['function'])(*args)
      else:
        value = node['function'](*args)

    return value

  def get_lower_node_value(self, function_lookup, lower_node):
    if lower_node['node']['node_type'] == 'terminal':
      return self.execute_node(lower_node['node'], function_lookup)
    else:
      result_list = map(lambda x:self.get_lower_node_value(function_lookup, x), lower_node['lower_nodes'])
      return self.execute_node(lower_node['node'], function_lookup, result_list)

  def execute(self, function_lookup):
    result_list = map(lambda x:self.get_lower_node_value(function_lookup, x), self.tree['lower_nodes'])
    return self.execute_node(self.tree['node'], function_lookup, result_list)

  def iterate_tree(self, nodes, callback):
    for node in nodes:
      callback(node)
      self.iterate_tree(node['lower_nodes'], callback)

  def recalculate_depth(self, nodes, depth):
    for node in nodes:
      node['depth'] = depth
      self.recalculate_depth(node['lower_nodes'], depth+1)

  def _get_node_list(self, nodes, node_list):
    for node in nodes:
      node_list.append(node)
      self._get_node_list(node['lower_nodes'], node_list)

  def get_node_list(self):
    node_list = []
    self._get_node_list(self.tree['lower_nodes'], node_list)
    return node_list

  def _simplify(self, node, function_lookup):
    if len(node['lower_nodes']) == 0:
      return
    terminal_value_count = filter(lambda x:TerminalSet.is_terminal_value(x['node']), node['lower_nodes'])
    if node['node']['arity'] == terminal_value_count:
      value = self.execute_node(node, function_lookup, args=map(lambda x:x['node']['value'], node['lower_nodes']))
      self.log().debug('Replacing existing node: %s' % pformat(node['node']))
      node['lower_nodes'] = []
      node['node'] = TerminalSet.terminal_value(value)
      self.log().debug(' -- with node: %s' % pformat(node['node']))
      self.is_simplified = False
    else:
      map(lambda x:self._simplify(x, function_lookup), node['lower_nodes'])

  def simplify(self, function_lookup):
    self.is_simplified = False
    simplify_loop_count = 1
    while not self.is_simplified:
      self.log().debug('Simplification %d' % (simplify_loop_count))
      self.is_simplified = True
      self._simplify(self.tree, function_lookup)
      simplify_loop_count += 1
