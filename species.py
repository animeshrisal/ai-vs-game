from genome import Genome
import random

class Species():

    def __init__(self, id, population_size, genome):
        self.id = id
        self.population_size = population_size
        self.generationNumber = 0

        self.genomes = {i:genome.clone() for i in range(self.population_size)}
        self.times_stagnated = 0
        self.active = True
        self.avg_max_fitness_achieved = 0
        self.generation_with_max_fitness = 0

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

    