from innovation import Innovation
import config
from genome import Genome
from species import Species

class NEAT(object):

    def __init__(self):

        self.population = 50
        self.initial_topology = (21, 2) #20 from the game data + 1 is bias weight 

        self.species_number = 0
        self.species = {}

        self.population_fitness = 0

        self.innovation = Innovation()

        initial_genome = Genome(self.initial_topology, self.innovation)
        self.create_new_speces(initial_genome, self.population)

    def create_new_species(self, initial_genome, population):
        self.species[self.species_number] = Species(self.species_number, population, initial_genome)
        self.species_number += 1

    def get_active_population(self):
        active_population = 0
        for species in self.species.values():
            if species.active:
                active_population += species.species_population 

        return active_population