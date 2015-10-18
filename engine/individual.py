from tree import Tree
import numpy

class Individual:
  STANDING_LIMITS = {'min': 1, 'max': 10, 'starting': 5}

  def __init__(self, exp_class, exp_args=[]):
    self.exp_class = exp_class
    self.exp_args = exp_args
    self._error = 0
    self._standing = None

  @property
  def error(self):
    return self._error

  @property
  def standing(self):
    return self._standing

  def increment_standing(self):
    self._standing = min(self._standing + 1, self.STANDING_LIMITS['max'])

  def decrement_standing(self):
    self._standing = max(self._standing - 1, self.STANDING_LIMITS['min'])

  def init_experiment(self):
    self._error = 0
    self.experiment = self.exp_class(*self.exp_args)
    self.experiment.initialize()
  
  def generate(self, extra_terminal_set=[], extra_function_set=[], tree_depth=3, tree_function_bias=1):
    self._standing = self.STANDING_LIMITS['starting']
    self.init_experiment()
    self.tree = Tree()
    self.tree.create(self.experiment.get_terminal_set() + extra_terminal_set,
                     self.experiment.get_function_set() + extra_function_set,
                     function_bias=tree_function_bias, max_depth=tree_depth)

  def clone(self):
    clone = self.__class__(self.exp_class, self.exp_args)
    clone._standing = self._standing
    clone.init_experiment()
    clone.tree = Tree()
    clone.tree.clone(self.tree)
    return clone

  def mutate(self):
    mutant = self.__class__(self.exp_class, self.exp_args)
    mutant._standing = self._standing
    mutant.init_experiment()
    mutant.tree = Tree()
    mutant.tree.mutate(self.tree)
    return mutant

  def reproduce(self, other_individual):
    child = self.__class__(self.exp_class, self.exp_args)
    child._standing = int(numpy.average([self._standing, other_individual._standing]))
    child.init_experiment()
    child.tree = Tree()
    child.tree.subtree_crossover(self.tree, other_individual.tree)
    return child

  def get_func(self, function_name):
    return self.experiment.function_lookup(function_name)

  def evaluate(self):
    loop = True
    while loop:
      self._error += self.experiment.norm_error(self.tree.execute(self))
      loop = self.experiment.next()

  def evaluate_data(self):
    samples = []
    loop = True
    self.experiment.initialize()
    while loop:
      actual_value = self.tree.execute(self)
      sample = {'value': actual_value, 'error': self.experiment.norm_error(actual_value)}
      if self.experiment.index() != None:
        sample['index'] = self.experiment.index()
      samples.append(sample)
      loop = self.experiment.next()
    return samples

  def simplify(self):
    self.tree.simplify(self)
