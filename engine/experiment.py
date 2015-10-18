
class Experiment:
  function_set = None
  terminal_set = None

  @classmethod
  def get_terminal_set(cls):
    return cls.terminal_set.get()

  @classmethod
  def get_function_set(cls):
    return cls.function_set.get()

  def function_lookup(self, name):
    return getattr(self, name)

  def index(self):
    return None

  def target_data(self):
    self.initialize()
    samples = []
    loop = True
    while loop:
      sample = {'value': self.error(0)}
      if self.index() != None:
        sample['index'] = self.index()
      samples.append(sample)
      loop = self.next()
    return samples
