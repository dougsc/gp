import importlib
from engine.individual import Individual
from engine.runner import Runner
import argparse

def run(cls_path, cls_args, tree_depth, pop_size, max_gen, tourny_size, error_threshold):
  print "debug with: run('%s', '%s', %d, %d, %d, %d, %f)" % (cls_path, cls_args, tree_depth, pop_size, max_gen, tourny_size, error_threshold)
  exp_lib = importlib.import_module('.'.join(cls_path.split('.')[:-1]))
  exp_cls = getattr(exp_lib, cls_path.split('.')[-1])
  exp_args = cls_args and cls_args.split(',') or []

  print 'Using class: %s, args: %s' % (exp_cls.__name__, exp_args)
  pop_size = pop_size - (pop_size % 24)
  print 'Using population size: %d, tree depth: %d, max generations: %d' % (pop_size, tree_depth, max_gen)
  population = map(lambda x:Individual(exp_cls, exp_args), range(pop_size))
  map(lambda x:x.generate(tree_depth=tree_depth), population)

  r = Runner(population, termination_error_threshold=error_threshold, max_generations=max_gen, tournament_size=tourny_size)
  r.run()
  return r

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Run GP experiments.')
  parser.add_argument('--class-path', help='class path for experiment', required=True, dest='cls_path')
  parser.add_argument('--class-args', help='constructor args for experiment', dest='cls_args')
  parser.add_argument('--tree-depth', help='Max tree depth', dest='tree_depth', default=4, type=int)
  parser.add_argument('--pop-size', help='Population Size (rounded down to mod 24)', dest='pop_size', default=100, type=int)
  parser.add_argument('--max-gens', help='Maximum number of generations', dest='max_gen', default=500, type=int)
  parser.add_argument('--tourney-size', help='Tournament Size (factor of 24)', dest='tourny_size', default=2, type=int)
  parser.add_argument('--threshold', help='Error threshold', dest='error_threshold', default=0, type=float)
  args = parser.parse_args()
  run(**vars(args))
