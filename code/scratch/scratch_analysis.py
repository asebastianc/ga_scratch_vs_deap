from scratch import GeneticAlgorithm
from scratch import spaces, prices, names
from scratch import export_results

population_size = 200
limit = 6.5
ga = GeneticAlgorithm(population_size)
ga.initialize_population(spaces, prices, limit)

for individual in ga.population:
  individual.fitness()

ga.order_population()
export_results(ga)