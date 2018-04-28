
class Species():

    def __init__(self, id, populationSize, genome):
        self.id = id
        self.populationSize = populationSize
        self.generationNumber = 0

        self.genomes = {i:genome.clone() for i in range(self.populationSize)}

    @staticmethod
    def crossover(parent1, parent2):
        child = Genome()

        for parent1Node in parent1.getNodeGenes().values():
            child.addNodeGenes(parent1Node.copy())

        for parent1Node in parent1.getConnectionGenes().values():
            if parent1Node.innovation_number in parent2.getConnectionGenes(): 
                truthValue = bool(random.getrandbits(1))
                childConGene = parent1Node.copy() if truthValue else parent2.getConnectionGenes().index(parent1Node.innovation).copy()
            else:
                childConGene = parent1Node.copy()
                child.addConnectionGenes(childConGene)

        return child

    