from genome import Genome
import random
import config
import os
os.chdir(os.getcwd())
import csv

import pickle
from run_game import run_game

class Species(object):

    def __init__(self, id, population_size, genome):
        self.id = id
        self.population_size = population_size
        self.generation_number = 0
        self.representative = genome 

        genome.set_species(self.id)
        genome.set_generation(self.generation_number)

        self.genomes = {i:genome.clone() for i in range(self.population_size)}

        for i in range(1, self.population_size):
            self.genomes[i].reinitialize()
        self.times_stagnated = 0
        self.active = True
        self.avg_max_fitness_achieved = 0
        self.generation_with_max_fitness = 0
        
    def run_generation(self):
        if self.active:
            species_fitness = self.generate_fitness()
            avg_species_fitness = float(species_fitness)/float(self.population_size)
            self.culling(avg_species_fitness)
            return avg_species_fitness if self.active else None

        else:
            return None 

    def generate_fitness(self):
        species_score = 0

        self.pretty_print_s_id(self.id)
        self.pretty_print_gen_id(self.generation_number)

        neural_networks = self.genomes.values()

        for x in self.genomes.values():
            x.fitness = 0

        run_game(neural_networks, self.generation_number, self.id)

        for x in self.genomes.values():
            species_score += x.fitness

        print(species_score)
        return species_score

    def evolve(self):
        if self.active:
            survivor_ids = self.get_survivors()
            self.create_next_generation(survivor_ids)
            self.generation_number += 1
            for genome in self.genomes.values():
                genome.set_generation(self.generation_number)


    def get_survivors(self):
        sorted_genomes_id = sorted(self.genomes, key=lambda k: self.genomes[k].fitness, reverse=True)
        alive_genomes_id = sorted_genomes_id[:int(round(float(self.population_size)/2.0))]
        most_fit_genome = self.genomes[alive_genomes_id[0]]
        pickle.dump(most_fit_genome, open("aiagent.p", "wb"))
        return alive_genomes_id

    
    def crossover(self, random_genome, random_genome_mate):
        if random_genome.fitness > random_genome_mate.fitness:
            fit_genome, unfit_genome = random_genome, random_genome_mate
        else:
            fit_genome, unfit_genome = random_genome_mate, random_genome

        for g_id, gene in fit_genome.connectionList.items():
            if g_id in unfit_genome.connectionList:

                # Randomly inherit from unfit genome
                if random.uniform(-1, 1) < 0:
                    gene.weight = unfit_genome.connectionList[g_id].weight

                # Have chance of disabling if either parent is disabled
                if not gene.enabled or not unfit_genome.connectionList[g_id].enabled:
                    if random.uniform(-1, 1) < config.INHERIT_DISABLED_GENE_RATE:
                        gene.disable()

        return fit_genome

    def create_next_generation(self, ids):
        genomes = {}

        genomes[0] = self.genomes[ids[0]].clone()
        genome_id = 1
    
        while(genome_id < self.population_size):
            #crossover happens here
            random_genome = self.genomes[0].clone()
            random_genome_mate = self.genomes[random.randint(0, len(ids))].clone()

            if random.uniform(0, 1) > config.CROSSOVER_CHANCE:
                genomes[genome_id] = random_genome
                
            else:
                genomes[genome_id] = self.crossover(random_genome, random_genome_mate)

            genomes[genome_id].mutate()

            genome_id += 1

        self.genomes = genomes

    
        
    def culling(self, new_average_fitness):
        if new_average_fitness > self.avg_max_fitness_achieved:
            self.avg_max_fitness_achieved = new_average_fitness
            self.generation_with_max_fitness = self.generation_number

        if(self.generation_number - self.generation_with_max_fitness) > config.STAGNATED_SPECIES_THRESHOLD:
            self.times_stagnated += 1
            print(self.times_stagnated)

            if self.times_stagnated > config.STAGNATIONS_ALLOWED:
                self.active = False #Dead Species

            else:
                self.generation_with_max_fitness = self.generation_number
                self.avg_max_fitness_achieved = 0

                genome = self.genomes[0]

                self.genomes = {i:genome.clone() for i in range(self.population_size)}

                for genome in self.genomes.values():
                    genome.reinitialize()

        if (self.population_size < config.WEAK_SPECIES_THRESHOLD):
            self.active = False #Too weak to live

    
    def add_genome(self, genome):
        genome.set_species(self.id)
        genome.set_generation(self.generation_number)
        self.genomes[self.population_size] = genome.clone()
        self.population_size += 1

    def delete_genome(self, genome_id):
        self.genomes[genome_id] = self.genomes[self.population_size-1].clone()
        del self.genomes[self.population_size-1]
        self.population_size -= 1

    def pretty_print_s_id(self, s_id):
        print("\n")
        print("====================")
        print("===  Species:", s_id, " ===")
        print("====================")
        print("\n")


    def pretty_print_gen_id(self, gen_id):
        print("-----------------------")
        print("---  Generation:", gen_id, " ---")
        print("-----------------------")
        print("\n")