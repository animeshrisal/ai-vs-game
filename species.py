from genome import Genome
import random
import config
import numpy as np
from scipy.stats import expon
import FlapPyBird.flappy as flpy
import os
os.chdir(os.getcwd() + '/FlapPyBird/')

class Species(object):

    def __init__(self, id, population_size, genome):
        self.id = id
        self.population_size = population_size
        self.generation_number = 0
        self.representative = genome 

        self.genomes = {i:genome.clone() for i in range(self.population_size)}
     
        self.times_stagnated = 0
        self.active = True
        self.avg_max_fitness_achieved = 0
        self.generation_with_max_fitness = 0
        
    def run_generation(self):
        if self.active:
            species_fitness = self.generate_fitness()
            avg_species_fitness = float(species_fitness)/float(self.population_size+1)
            self.culling(avg_species_fitness)
            return avg_species_fitness if self.active else None

        else:
            return None 

    def generate_fitness(self):
        species_score = 0

        neural_networks = self.genomes.values()

        app = flpy.FlappyBirdApp(neural_networks)
        app.play()
        results = app.crash_info

        for crash_info in results:

            distance_from_pipes = 0
            if (crash_info['y'] < crash_info['upperPipes'][0]['y']):
                distance_from_pipes = abs(crash_info['y'] - crash_info['upperPipes'][0]['y'])       
            elif (crash_info['y'] > crash_info['upperPipes'][0]['y']):      
                distance_from_pipes = abs(crash_info['y'] - crash_info['lowerPipes'][0]['y'])       

            fitness_score = ((crash_info['score'] * 1000)       
                              + (crash_info['distance'])        
                              - (distance_from_pipes * 3)       
                              - (1.5 * crash_info['energy']))

            # Should experiment with this more.
            # fitness_score = ((crash_info['distance'])
            #                  - (1.5 * crash_info['energy']))

            neural_networks[crash_info['network_id']].set_fitness(fitness_score)
            species_score += fitness_score

        print "\nSpecies Score:", species_score

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
        return alive_genomes_id

    
    def crossover(self, genome1, genome2):
        if genome1.fitness > genome2.fitness:
            parent1, parent2 = genome1, genome2
        else:
            parent1, parent2 = genome2, genome1

        child = parent1

        for parent1Connection in parent1.getConnectionGenes().values():
            if parent1Connection.innovation_number in parent2.getConnectionGenes(): 
                truthValue = bool(random.getrandbits(1))
                childConGene = parent1Connection.copy() if truthValue else parent2.getConnectionGenes()[parent1Connection.innovation_number].copy()
            else:
                childConGene = parent1Connection.copy()
                child.addConnectionGenes(childConGene)

        return child

    def create_next_generation(self, ids):
        genomes = {}

        genomes[0] = self.genomes[ids[0]].clone()
        genome_id = 1
    
        while(genome_id < self.population_size):
            #crossover happens here
            random_genome = self.genomes[random.randint(0, len(ids) -1)]
            random_genome_mate = self.genomes[random.randint(0, len(ids) -1)]

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

            if self.times_stagnated > config.STAGNATIONS_ALLOWED:
                self.active = False #Dead Species

            else:
                self.generation_with_max_fitness = self.generation_number
                self.avg_max_fitness_achieved = 0

                genome = self.genomes[0]

                self.genomes = {i:genome.clone() for i in range(self.population_size)}

                for genome in self.genomes.values():
                    pass #reinitialize genome

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

