from connectionGene import ConnectionGene
from nodeGene import NodeGene
from genome import Genome
from innovation import Innovation

calc = Genome()

innovation_value = Innovation()

node1 = NodeGene(1, 'input', 1)
node2 = NodeGene(2, 'input', 2)
node3 = NodeGene(3, 'output', 0)

calc.addNodeGenes(node1)
calc.addNodeGenes(node2)
calc.addNodeGenes(node3)

calc.addConnectionGenes(ConnectionGene(innovation_value.getInnovation(), calc.getNodeGenes()[1], calc.getNodeGenes()[3], 0.2, True))
calc.addConnectionGenes(ConnectionGene(innovation_value.getInnovation(), calc.getNodeGenes()[2], calc.getNodeGenes()[3], 0.3, True))

calc.calculateOutput()