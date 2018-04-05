from connectionGene import ConnectionGene
from nodeGene import NodeGene
from genome import Genome

parent1 = Genome()
parent2 = Genome()

for x in range(1,4):
    node = NodeGene(x, 'input')
    parent1.addNodeGenes(node)
    

parent1.addNodeGenes(NodeGene(4, 'output'))
parent1.addNodeGenes(NodeGene(5, 'hidden'))


parent1.addConnectionGenes(ConnectionGene(1, 1, 4, 1, True))
parent1.addConnectionGenes(ConnectionGene(2, 2, 4, 1, False))
parent1.addConnectionGenes(ConnectionGene(3, 3, 4, 1, True))
parent1.addConnectionGenes(ConnectionGene(4, 2, 5, 1, True))
parent1.addConnectionGenes(ConnectionGene(5, 5, 4, 1, True))
parent1.addConnectionGenes(ConnectionGene(8, 1, 5, 1, True))

for x in range(1,4):
    node = NodeGene(x, 'input')
    parent2.addNodeGenes(node)


parent2.addNodeGenes(NodeGene(4, 'output'))
parent2.addNodeGenes(NodeGene(5, 'hidden'))
parent2.addNodeGenes(NodeGene(6, 'hidden'))


parent1.addConnectionGenes(ConnectionGene(1, 1, 4, 1, True))
parent1.addConnectionGenes(ConnectionGene(2, 2, 4, 1, False))
parent1.addConnectionGenes(ConnectionGene(3, 3, 4, 1, True))
parent1.addConnectionGenes(ConnectionGene(4, 2, 5, 1, True))
parent1.addConnectionGenes(ConnectionGene(5, 5, 4, 1, False))
parent1.addConnectionGenes(ConnectionGene(6, 5, 6, 1, True))
parent1.addConnectionGenes(ConnectionGene(7, 6, 4, 1, True))
parent1.addConnectionGenes(ConnectionGene(9, 3, 5, 1, True))
parent1.addConnectionGenes(ConnectionGene(10, 1, 6, 1, True))

child = Genome.crossover(parent1, parent2)

for x in child.getConnectionGenes():
    print(x, child.getConnectionGenes()[x].input_neuron, child.getConnectionGenes()[x].output_neuron)