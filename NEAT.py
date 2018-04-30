from innovation import Innovation
import config
import genome
from species import Species

class NEAT(object):

    def __init__(self):

        self.population = 50
        self.initial_topology = (20, 2)

        self.species_number = 0
        self.species = {}

        self.population_fitness = 0

        self.innovation = Innovation()

        initial_genome = Genome(self.initial_topology, self.innovation)
        self.create_new_speces(initial_genome, self.population)

    def create_new_speces(self, initial_genome, population):
        self.species[self.species_number] = Species(self.species_number, population, initial_genome)
        self.species += 1

    