import pandas as pd
import random
import numpy as np
from deap import base, creator, algorithms, tools
import os
import lzma

class Product():
	def __init__(self, name, space, price):
		self.name = name
		self.space = space
		self.price = price

df = pd.read_csv("../../data/furniture_products.csv")

products_list = []
for i in range(df.shape[0]):
	products_list.append(Product(df["Product"].iloc[i], df["Volume"].iloc[i], df["Price"].iloc[i]))

spaces = []
prices = []
names = []

for product in products_list:
	spaces.append(product.space),
	prices.append(product.price),
	names.append(product.name)

population_size = 20
mutation_probability = 0.01
crossover_probability = 1.0

def fitness(solution):
	cost = 0
	sum_space = 0
	for i in range(len(solution)):
		if solution[i] == 1:
			cost += prices[i]
			sum_space += spaces[i]
	# constraint penalization		
	if sum_space > 6.5:
		cost = 1
	return cost,


# initialize the GA
toolbox = base.Toolbox()

# as we have a maximisation problem
creator.create("FitnessMax", base.Fitness, weights = (1.0,))

# create individuals
creator.create("Individual", list, fitness = creator.FitnessMax)

# register individuals with boolean format
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool,	n = 11)

# register a population
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# evaluate population
toolbox.register("evaluate", fitness)

# crossover operator
toolbox.register("mate", tools.cxOnePoint)

# mutation operator
toolbox.register("mutate", tools.mutFlipBit, indpb = 0.1) # indpb: mutataion probability

# roulette method
toolbox.register("select", tools.selRoulette)

# Implementation
population = toolbox.population(n = 200) # n: population size
number_of_generations = 5 # 500 generations are performed within line 84 for loop

statistics = tools.Statistics(key = lambda individual: individual.fitness.values)
statistics.register("max", np.max)

score = []
chromosomes = []

for z in range(5000):
	population, generation = algorithms.eaSimple(population, toolbox,	crossover_probability, mutation_probability, number_of_generations, statistics)

	score_ = []
	for z in range(len(generation)):
		score_.append("{:.2f}".format(generation[z]["max"]))
	score_.append("-")
	score.append(score_)

	chromosomes_ = []
	for y in range(len(generation)):
		chromosome = population[y]
		chromosomes_.append(chromosome)
	chromosomes_.append("-")
	chromosomes.append(chromosomes_)

used_space = []
for i in range(len(chromosomes)):
	pop = chromosomes[i]
	for u in range(len(pop)):
		space_usage = 0
		indiv = pop[u]
		if indiv == "-":
			pass
		else:
			for t in range(len(spaces)):
				if indiv[t] == 1:
					space_usage += spaces[t]
		used_space.append(space_usage)

for f in range(len(used_space)):
	if used_space[f] == 0:
		used_space[f] = "-"

ind_score_list = []
for i in range(len(score)):
	generation_score = score[i]
	for u in range(len(generation_score)):
		ind_score = generation_score[u]
		ind_score_list.append(ind_score)

results = pd.DataFrame({"Space": used_space, "Score":ind_score_list})

with open("../../results/distributed/distributed_results.txt", "a") as f:
	for index, row in results.iterrows():
		if row["Space"] == "-":
			f.write("\n")
		else:
			f.write("{:.2f} {}\n".format(row["Space"], row["Score"]))

lzc = lzma.LZMACompressor()
with open("../../results/distributed/distributed_results.txt", "r") as fin, open("../../results/distributed/distributed_results.xz", "wb") as fout:
	for chunk in fin:
		compressed_chunk = lzc.compress(chunk.encode("ascii"))
		fout.write(compressed_chunk)
	fout.write(lzc.flush())


results = results[(results["Space"] != "-") & (results["Score"] != "-")]

results["Space"] = results["Space"].astype(float)
results["Score"] = results["Score"].astype(float)

results = results[results["Space"] <= 6.5]

results.to_csv("../../results/distributed/distributed_results.csv", index = False)