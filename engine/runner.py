
import numpy
import bisect
import random
import sys
from pprint import pformat
from utils.logger import GP_Logger
from utils.stats import Stats

class Runner:
  NEW_GEN_DIST = {'mutate': 0.05, 'reproduce': 0.5}
  # Stats Keys:
  SK_LOWEST_ERROR = 'lowest_error'
  SK_BEST_INDIVIDUAL = 'best_individual'
  SK_TARGET_SAMPLES = 'target_samples'
  SK_ACTUAL_SAMPLES = 'actual_samples'  
  SK_BEST_TREE = 'best_tree'

  @classmethod
  def log(cls):
    return GP_Logger.logger(cls.__name__)

  def __init__(self, population, termination_error_threshold, max_generations, tournament_size=2):
    self.population = population
    self.termination_error_threshold = termination_error_threshold
    self.current_generation = 1
    self.current_best_error = sys.maxint
    self.max_generations = max_generations
    self.tournament_size = tournament_size
    self.stats = Stats(self.__class__.__name__)
    self.stats.init_series([self.SK_LOWEST_ERROR, self.SK_BEST_INDIVIDUAL, self.SK_TARGET_SAMPLES, self.SK_ACTUAL_SAMPLES,
                            self.SK_BEST_TREE])

  def store_target_samples(self):
    experiment = self.population[0].exp_class(*self.population[0].exp_args)
    map(lambda x:self.stats.add_to_series(self.SK_TARGET_SAMPLES, x), experiment.target_data())

  def store_actual_samples(self, individual):
    self.stats.init_series(self.SK_ACTUAL_SAMPLES)
    map(lambda x:self.stats.add_to_series(self.SK_ACTUAL_SAMPLES, x), individual.evaluate_data())

  def findIndexOfBest(self):
    return numpy.argmin(map(lambda x:x.error, self.population))

  def evaluate(self):
    self.log().debug('evaluating generation %d' % (self.current_generation))
    for individual in self.population:
      individual.evaluate()

    best = self.findIndexOfBest()
    self.log().debug('population member %d was best with %d error (target: %d)' % (best, self.population[best].error, self.termination_error_threshold))
    self.stats.add_to_series(self.SK_LOWEST_ERROR, {'error': self.population[best].error, 'index': self.current_generation}, timestamp=True)
    self.stats.add_to_series(self.SK_BEST_INDIVIDUAL, {'best_ix': best, 'index': self.current_generation}, timestamp=True)
    return self.population[best]

  def update_standings(self):
    for i in xrange(0, len(self.population), self.tournament_size):
      lowest_error = min(map(lambda x:x.error, self.population[i:i+self.tournament_size]))
      winners = filter(lambda x:x.error == lowest_error, self.population[i:i+self.tournament_size])
      losers = filter(lambda x:x.error > lowest_error, self.population[i:i+self.tournament_size])
      assert len(winners) + len(losers) == self.tournament_size, 'Expected winners (%d) + losers (%d) = tournament size (%d)' % (len(winners), len(losers), self.tournament_size)
      if len(losers) == 0:
        continue

      self.log().debug('best in tournament [%d:%d](error: %d): %d winners' % (i, i+self.tournament_size, lowest_error, len(winners)))
      map(lambda x:x.increment_standing(), winners)
      map(lambda x:x.decrement_standing(), losers)

  def random_select_n_unique(self, number, weight_list):
    selection = []
    assert number < len(weight_list), 'attemt to get %d unique values from a list of %d elements' % (number, len(weight_list))
    weight_max = weight_list[-1]

    while len(selection) < number:
      ix = bisect.bisect_right(weight_list, random.uniform(0, weight_max))
      if not ix in selection:
        selection.append(ix)

    return selection

  def generate_new_population(self):
    new_population = []
    self.update_standings()
    weight_list = list(numpy.cumsum(map(lambda x:x.standing, self.population)))
    pop_size = len(self.population)

    chosen_number = int(pop_size * self.NEW_GEN_DIST['reproduce'])
    chosen_number = chosen_number - (chosen_number % 2)
    individuals_chosen = self.random_select_n_unique(chosen_number, weight_list)
    self.log().debug('%d indiviuals chosen to reproduce - %s' % (len(individuals_chosen), sorted(individuals_chosen)))
    for ix in xrange(0, len(individuals_chosen), 2):
      new_population.append(self.population[individuals_chosen[ix]].reproduce(self.population[individuals_chosen[ix+1]]))

    chosen_number = int(pop_size * self.NEW_GEN_DIST['mutate'])
    individuals_chosen = self.random_select_n_unique(chosen_number, weight_list)
    self.log().debug('%d indiviuals chosen to mutate - %s' % (len(individuals_chosen), sorted(individuals_chosen)))
    for ix in xrange(0, len(individuals_chosen)):
      new_population.append(self.population[individuals_chosen[ix]].mutate())

    chosen_number = len(self.population) - len(new_population)
    individuals_chosen = self.random_select_n_unique(chosen_number, weight_list)
    self.log().debug('%d indiviuals chosen to clone - %s' % (len(individuals_chosen), sorted(individuals_chosen)))
    for ix in xrange(0, len(individuals_chosen)):
      new_population.append(self.population[individuals_chosen[ix]].clone())
    
    assert len(self.population) == len(new_population), 'new population size does not match original'
    self.population = new_population
    self.current_generation += 1

  def check_evaluation(self, best):
    if best.error <= self.current_best_error:
      self.current_best_error = best.error
      self.stats.add_to_series(self.SK_BEST_TREE, {'tree': best.tree.dump_structure()})
      self.store_actual_samples(best)
    return (best.error <= self.termination_error_threshold)

  def run(self):
    self.store_target_samples()
    success = self.check_evaluation(self.evaluate())
    while self.current_generation <= self.max_generations and success == False:
      self.generate_new_population()
      self.log().debug('average standing for generation %d: %f' % (self.current_generation, 
                                       numpy.average(map(lambda x:x.standing, self.population))))
      success = self.check_evaluation(self.evaluate())
    print 'success: %s' % (success)
