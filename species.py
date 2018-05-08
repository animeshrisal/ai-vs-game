from genome import Genome
import random
import config

class Species():

    def __init__(self, id, population_size, genome):
        self.id = id
        self.population_size = population_size
        self.generation_number = 0
        self.representative = genome 

        self.genomes = {i:genome.clone() for i in range(self.population_size)}

        for i in range(self.population_size):
            pass
        
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
        pass

    def evolve(self):
        if self.active:
            survivor_ids = self.select_survivor()
            self.create_next_generation(survivor_ids)
            self.generation_number += 1
            for genome in self.genomes.values():
                genome.set_generaton(self.generation_number)


    def get_survivors(self):
        sorted_genomes_id = sorted(self.genomes, key=lambda k: self.genomes[k].fitness, reverse=True)

        alive_genomes_id = sorted_genomes_id[:int(rount(float(self.population_size)/2.0))]
        
        return alive_genomes_id

    def crossover(parent1, parent2):
        child = Genome()

        for parent1Node in parent1.getNodeGenes().values():
            child.addNodeGenes(parent1Node.copy())

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
            pass

    
        
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

                
    