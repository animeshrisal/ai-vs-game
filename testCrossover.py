from connectionGene import ConnectionGene
from nodeGene import NodeGene
from genome import Genome
from species import Species

parent1 = Genome()
parent2 = Genome()

for x in range(1,4):
    node = NodeGene(x, 'input')
    parent1.addNodeGenes(node)
    

parent1.addNodeGenes(NodeGene(4, 'output'))
parent1.addNodeGenes(NodeGene(5, 'hidden'))

for x in range(1,4):
    node = NodeGene(x, 'input')
    parent2.addNodeGenes(node)


parent2.addNodeGenes(NodeGene(4, 'output'))
parent2.addNodeGenes(NodeGene(5, 'hidden'))
parent2.addNodeGenes(NodeGene(6, 'hidden'))

child = Species.crossover(parent1, parent2)

for x in child.getConnectionGenes():
    print(x, child.getConnectionGenes()[x].input_neuron, child.getConnectionGenes()[x].output_neuron)

for x in child.getNodeGenes():
    print(x, child.getNodeGenes()[x].id, child.getNodeGenes()[x].nodeType)