from connectionGene import ConnectionGene
from nodeGene import NodeGene
from genome import Genome
from innovation import Innovation

parent1 = Genome()

innovation_value = Innovation()

for x in range(1,4):
    node = NodeGene(x, 'input')
    parent1.addNodeGenes(node)
    

parent1.addNodeGenes(NodeGene(4, 'output'))
parent1.addNodeGenes(NodeGene(5, 'hidden'))


parent1.addConnectionGenes(ConnectionGene(innovation_value.getInnovation(), 1, 4, 1, True))
parent1.addConnectionGenes(ConnectionGene(innovation_value.getInnovation(), 2, 4, 1, False))
parent1.addConnectionGenes(ConnectionGene(innovation_value.getInnovation(), 3, 4, 1, True))
parent1.addConnectionGenes(ConnectionGene(innovation_value.getInnovation(), 2, 5, 1, True))
parent1.addConnectionGenes(ConnectionGene(innovation_value.getInnovation(), 5, 4, 1, True))
parent1.addConnectionGenes(ConnectionGene(innovation_value.getInnovation(), 1, 5, 1, True))

parent1.addConnectionMutation(innovation_value)

for x in parent1.getConnectionGenes():
    print(x, parent1.getConnectionGenes()[x].input_neuron, parent1.getConnectionGenes()[x].output_neuron, parent1.getConnectionGenes()[x].enabled)

for x in parent1.getNodeGenes():
    print(parent1.getNodeGenes()[x].id, parent1.getNodeGenes()[x].nodeType)

