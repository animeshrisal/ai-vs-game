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

for x in parent1.getNodeGenes():
    print(parent1.getNodeGenes()[x].id, 
        parent1.getNodeGenes()[x].nodeType, 
        parent1.getNodeGenes()[x].inputGenes, 
        parent1.getNodeGenes()[x].outputGenes)

conn1 = ConnectionGene(innovation_value.getInnovation(), parent1.getNodeGenes()[1], parent1.getNodeGenes()[4], 1, True)

parent1.addConnectionGenes(conn1)

for x in parent1.getNodeGenes():
    print(parent1.getNodeGenes()[x].id, 
        parent1.getNodeGenes()[x].nodeType, 
        parent1.getNodeGenes()[x].inputGenes, 
        parent1.getNodeGenes()[x].outputGenes)

for x in parent1.getConnectionGenes():
    print(parent1.getConnectionGenes()[x].output_neuron.id)