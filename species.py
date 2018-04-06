

class Species():

    def __init__(self, id, populationSize, genome):
        self.id = id
        self.populationSize = populationSize
        self.generationNumber = 0

        self.genomes = {i:genome.clone() for i in range(self.populationSize)}

    