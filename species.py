from genome import Genome
import random

class Species():

    def __init__(self, id, population_size, genome):
        self.id = id
        self.population_size = population_size
        self.generationNumber = 0
        self.representative = genome 

        self.genomes = {i:genome.clone() for i in range(self.population_size)}

        for i in range(self.population_size):
            pass
        
        self.times_stagnated = 0
        self.active = True
        self.avg_max_fitness_achieved = 0
        self.generation_with_max_fitness = 0

    def generate_fitness(self):
        pass

    def evolve(self):
        if self.active:
            survivor_id = self.select_survivor()
        
        pass

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

    