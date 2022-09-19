import pandas as pd
from random import random
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

class Individual():
	def __init__(self, spaces, prices, space_limit, generation = 0):
		self.spaces = spaces
		self.prices = prices
		self.space_limit = space_limit
		self.score_evaluation = 0
		self.used_space = 0
		self.generation = generation
		self.chromosome = []

		for i in range(len(spaces)):
			if random() < 0.9: ######### 0.5
				self.chromosome.append('0')
			else:
				self.chromosome.append('1')

	def fitness(self):
		score = 0
		sum_spaces = 0
		for i in range(len(self.chromosome)):
			if self.chromosome[i] == '1':
				score += self.prices[i]
				sum_spaces += self.spaces[i]
		if sum_spaces > self.space_limit: # penalization if spaced is violated
			score = 1
		self.score_evaluation = score
		self.used_space = sum_spaces

	def crossover(self, other_individual):
		# create children
		cutoff = round(random () * len(self.chromosome))
		child1 = other_individual.chromosome[0:cutoff] + self.chromosome[cutoff::]
		child2 = self.chromosome[0:cutoff] + other_individual.chromosome[cutoff::]

		# create new individuals
		children = [Individual(self.prices, self.prices, self.space_limit, self.generation + 1),
								Individual(self.prices, self.prices, self.space_limit, self.generation + 1)]
		# define new chromosomes
		children[0].chromosome = child1
		children[1].chromosome = child2
		return children

	def mutation(self, rate):
		for i in range(len(self.chromosome)):
			if random() < rate:
				if self.chromosome[i] == "1":
					self.chromosome[i] = "0"
				else:
					self.chromosome[i] = "1"
		return self

class GeneticAlgorithm():
	def __init__(self, population_size):
		self.population_size = population_size
		self.population = [] # store each individual
		self.generation = 0 # generation atribute of individual
		self.best_solution = None # best solution considering all gen
		self.list_of_solutions = []

	def initialize_population(self, spaces, prices, space_limit):
		for i in range(self.population_size):
			self.population.append(Individual(spaces, prices, space_limit))
		self.best_solution = self.population[0]

	def order_population(self):
		self.population = sorted(self.population, key = lambda population:  population.score_evaluation, reverse = True)

	def best_individual(self, individual): # update the best solution in index 0
		if individual.score_evaluation > self.best_solution.score_evaluation:
			self.best_solution = individual

	def sum_evaluations(self):
		sum = 0
		for individual in self.population:
			sum += individual.score_evaluation
		return sum

	def select_parent(self, sum_evaluation):
		parent = -1
		# select one of the individuals to apply crossover
		random_value = random() * sum_evaluation # simmulation of roulette
		sum = 0
		i = 0 # control the loop
		while i < len(self.population) and sum < random_value:
			sum += self.population[i].score_evaluation
			parent += 1 # index of self.population
			i += 1
		return parent
		
	def solve(self, mutation_probability, number_of_generations, spaces, prices, limit):
		self.initialize_population(spaces, prices, limit)
		
		for individual in self.population:
			individual.fitness()
		self.order_population()
		self.best_solution = self.population[0]
		self.list_of_solutions.append(self.best_solution.score_evaluation)
		
		for generation in range(number_of_generations):
			sum = self.sum_evaluations()
			new_population = []
			for new_individuals in range(0, self.population_size, 2):
				parent1 = self.select_parent(sum)
				parent2 = self.select_parent(sum)
				children = self.population[parent1].crossover(self.population[parent2])
				new_population.append(children[0].mutation(mutation_probability))
				new_population.append(children[1].mutation(mutation_probability))
			
			self.population = list(new_population)

			for individual in self.population:
				individual.fitness()
			self.visualize_generation()
			best = self.population[0]
			self.list_of_solutions.append(best.score_evaluation)
			self.best_individual(best)

		print('**** Best solution - Generation: ', self.best_solution.generation,
					'Total price: ', self.best_solution.score_evaluation, 'Space: ', self.best_solution.used_space,
					'Chromosome: ', self.best_solution.chromosome)
		
		return self.best_solution.chromosome

def export_results(ga):
	used_space = []
	score = []

	for n in range(5000):
		for i in range(ga.population_size):
			if ga.population[i].score_evaluation > 1.0:
				used_space.append(round(ga.population[i].used_space, 2))
				score.append(round(ga.population[i].score_evaluation, 2))

		used_space.append("-")
		score.append("-")

	df = pd.DataFrame({"Space": used_space, "Score": score})

	df.to_csv("../../results/scratch/scratch_results.csv", index = False)

	with open("../../results/scratch/scratch_results.txt", "a") as f:
		for index, row in df.iterrows():
			if row["Space"] == "-":
				f.write("\n")
			else:
				f.write("{:.2f} {:.2f}\n".format(row["Space"], row["Score"]))

	lzc = lzma.LZMACompressor()
	with open("../../results/scratch/scratch_results.txt", "r") as fin, open("../../results/scratch/scratch_results.xz", "wb") as fout:
		for chunk in fin:
			compressed_chunk = lzc.compress(chunk.encode("ascii"))
			fout.write(compressed_chunk)
		fout.write(lzc.flush())