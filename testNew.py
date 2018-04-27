from connectionGene import ConnectionGene
from nodeGene import NodeGene
from genome import Genome
from innovation import Innovation

parent1 = Genome()

innovation_value = Innovation()

for x in range(1,4):
    node = NodeGene(x, 'input')
    node.addInput(1)
    parent1.addNodeGenes(node)

    
parent1.addNodeGenes(NodeGene(4, 'output'))


conn1 = ConnectionGene(innovation_value.getInnovation(), parent1.getNodeGenes()[1], parent1.getNodeGenes()[4], 0.5, True)
conn2 = ConnectionGene(innovation_value.getInnovation(), parent1.getNodeGenes()[2], parent1.getNodeGenes()[4], 0.5, True)
conn3 = ConnectionGene(innovation_value.getInnovation(), parent1.getNodeGenes()[3], parent1.getNodeGenes()[4], 0.5, True)