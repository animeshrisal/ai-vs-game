from innovation import Innovation
import config
from genome import Genome
from species import Species

class NEAT(object):

    def __init__(self):

        self.population = 50
        self.initial_topology = (64, 2) 

        self.species_number = 0
        self.species = {}

        self.population_fitness = 0

        self.innovation = Innovation()

        initial_genome = Genome(self.initial_topology, self.innovation)
        self.create_new_species(initial_genome, self.population)


    
    def start_evolution(self):
        while True:

            avg_fitness_scores = {}

            for individual_species_id, individual_species in self.species.items():
                avg_fitness = individual_species.run_generation()

                if avg_fitness != None:
                    avg_fitness_scores[individual_species_id] = avg_fitness

            for individual_species_id, individual_species in self.species.items():
                individual_species.evolve()

            if config.SPECIATION:
                self.perform_speciation() 


    def create_new_species(self, initial_genome, population):
        self.species[self.species_number] = Species(self.species_number, population, initial_genome)
        self.species_number += 1

    def perform_speciation(self):
        for species_id, individual_species in self.species.items():
            if individual_species.active:
                for genome_index, genome in individual_species.genomes.items():
                    if not genome.is_compatible(individual_species.representative):
                        self.assign_genome(genome, species_id)
                        individual_species.delete_genome(genome_index)

    def assign_genome(self, genome, species_id):
        for individual_species_id, individual_species in self.species.items():
            if genome.is_compatible(individual_species.representative):
                species.add_genome(genome)
                return

        self.create_new_species(genome, self.population)