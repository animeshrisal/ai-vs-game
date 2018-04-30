from connectionGene import ConnectionGene
from nodeGene import NodeGene
from genome import Genome
from species import Species
from innovation import Innovation
import random

parent1 = Genome()
parent2 = Genome()
innovation_value = Innovation()

for x in range(1,4):
    node = NodeGene(x, 'input')
    parent1.addNodeGenes(node)
    

parent1.addNodeGenes(NodeGene(4, 'output'))
parent1.addNodeGenes(NodeGene(5, 'hidden'))

parent1.addConnectionGenes(ConnectionGene(1, parent1.getNodeGenes()[1], parent1.getNodeGenes()[4], 1, True))
parent1.addConnectionGenes(ConnectionGene(2, parent1.getNodeGenes()[2], parent1.getNodeGenes()[4], 1, False))
parent1.addConnectionGenes(ConnectionGene(3, parent1.getNodeGenes()[3], parent1.getNodeGenes()[4], 1, True))
parent1.addConnectionGenes(ConnectionGene(4, parent1.getNodeGenes()[2], parent1.getNodeGenes()[5], 1, True))
parent1.addConnectionGenes(ConnectionGene(5, parent1.getNodeGenes()[5], parent1.getNodeGenes()[4], 1, True))
parent1.addConnectionGenes(ConnectionGene(8, parent1.getNodeGenes()[1], parent1.getNodeGenes()[5], 1, True))

for x in range(1,4):
    node = NodeGene(x, 'input')
    parent2.addNodeGenes(node)


parent2.addNodeGenes(NodeGene(4, 'output'))
parent2.addNodeGenes(NodeGene(5, 'hidden'))
parent2.addNodeGenes(NodeGene(6, 'hidden'))

parent2.addConnectionGenes(ConnectionGene(1, parent1.getNodeGenes()[1], parent1.getNodeGenes()[4], 1, True))
parent2.addConnectionGenes(ConnectionGene(2, parent1.getNodeGenes()[2], parent1.getNodeGenes()[4], 1, False))
parent2.addConnectionGenes(ConnectionGene(3, parent1.getNodeGenes()[3], parent1.getNodeGenes()[4], 1, True))
parent2.addConnectionGenes(ConnectionGene(4, parent1.getNodeGenes()[2], parent1.getNodeGenes()[5], 1, True))
parent2.addConnectionGenes(ConnectionGene(5, parent1.getNodeGenes()[5], parent1.getNodeGenes()[4], 1, False))
parent2.addConnectionGenes(ConnectionGene(6, parent1.getNodeGenes()[5], parent1.getNodeGenes()[6], 1, True))
parent2.addConnectionGenes(ConnectionGene(7, parent1.getNodeGenes()[6], parent1.getNodeGenes()[4], 1, True))
parent2.addConnectionGenes(ConnectionGene(9, parent1.getNodeGenes()[3], parent1.getNodeGenes()[5], 1, True))
parent2.addConnectionGenes(ConnectionGene(10, parent1.getNodeGenes()[1], parent1.getNodeGenes()[6], 1, True))

child = Species.crossover(parent1, parent2)

for x in child.getConnectionGenes():
    print(x, child.getConnectionGenes()[x].input_neuron.id, child.getConnectionGenes()[x].output_neuron.id, child.getConnectionGenes()[x].enabled)

for x in child.getNodeGenes():
    print(x, child.getNodeGenes()[x].id, child.getNodeGenes()[x].nodeType)