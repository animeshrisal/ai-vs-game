from connectionGene import ConnectionGene
from nodeGene import NodeGene
import random
import math

class Genome:

    def __init__(self, topology):
        self.nodeList = nodeList
        self.connectionList = connectionList

    def getNodeGenes(self):
        return self.nodeList

    def getConnectionGenes(self):
        return self.connectionList

    def addNodeGenes(self, node):
        self.nodeList.update({node.id: node.clone()})

    def addConnectionGenes(self, conn):
        self.connectionList.update({conn.innovation_number: conn.clone()})

    def addConnectionMutation(self, innovation_number):
        node1 = self.nodeList[random.randint(1, len(self.nodeList))]
        node2 = self.nodeList[random.randint(1, len(self.nodeList))]
        weight = random.uniform(-1, 1)

        reverse = False

        if(node1.nodeType == 'hidden' and node2.nodeType == 'input'):
            reverse = True 

        if(node1.nodeType == 'output' and node2.nodeType == 'hidden'):
            reverse = True

        if(node1.nodeType == 'output' and node2.nodeType == 'input'):
            reverse = True

        connectionImpossible = False

        if(node1.nodeType == 'input' and node2.nodeType == 'input'):
            connectionImpossible = True        

        if(node1.nodeType == 'output' and node2.nodeType == 'output'):
            connectionImpossible = True 

        if(node1.id == node2.id):
            connectionImpossible = True

        connectionExists = False

        for connection in self.connectionList.values():
            if(connection.input_neuron.id == node1.id and connection.output_neuron.id == node2.id):
                connectionExists = True
                break
            
            elif(connection.input_neuron.id == node2.id and connection.output_neuron.id == node1.id):
                connectionExists = True
                break

        if(connectionExists or connectionImpossible):
            return


        newConnection = ConnectionGene(innovation_number.getInnovation(), node2 if reverse else node1, node1 if reverse else node2, weight, True)
        self.connectionList.update({newConnection.innovation_number : newConnection})

    def addNodeMutation(self, innovation_number):
        randomValue = random.randint(1, len(self.connectionList) -1)
        connection = self.connectionList[randomValue]

        connection.disable()

        inNode = self.nodeList[connection.input_neuron.id]
        outNode = self.nodeList[connection.output_neuron.id]

        newNode = NodeGene(len(self.nodeList) + 1, 'hidden')

        inToNew = ConnectionGene(innovation_number.getInnovation(), inNode, newNode, 1, True)
        newToOut = ConnectionGene(innovation_number.getInnovation(), newNode, outNode, connection.weight, True)

        self.nodeList.update({newNode.id : newNode})
        self.connectionList.update({inToNew.innovation_number : inToNew})
        self.connectionList.update({newToOut.innovation_number : newToOut})

    def clone(self):
        return Genome(nodeList = self.nodeList, connectionList = self.connectionList)


    def calculateOutput(self):
        complete = False
        while not complete:
            complete = True
            for x in self.nodeList.values():
                print(x.id , ' ',len(x.inputGenes), ' ', x.recieved_inputs)
                if x.ready():
                    x.fire()

                if not x.has_fired():
                    complete = False

                print(x.id, x.has_fired(), x.inputValue)

    def get_excess_genes(self, comparison_genome):
        excess_genes = []
        largest_innovation_id = max(self.connectionList.keys)

        for g_id, genome in comparison_genome.connectionList.items():
            if g_id > largest_innovation_id:
                excess_genes.append(genome)

        return excess_genes


    def get_disjoint_genes(self, comparison_genome):
        disjoint_genes = []
        largest_innovation_id = max(self.connectionList.keys)

        for g_id, genome in comparison_genome.connectionList.items():
            if not g_id in self.connectionList and g_id < largest_innovation_id:
                disjoint_genes.append(genome)

        for g_id, genome in self.connectionList.items():
            if not g_id in comparison_genome:
                disjoint_genes.append(genome)

        return disjoint_genes      

    def get_avg_weight_difference(self, comparison_genome):
        avg_weight_self = sum(c_gene.weight for c_gene in self.connectionList.values() / len(self.connectionList))
        avg_weight_comp = sum(c_gene.weight for c_gene in comparison_genome.connectionList.values() / len(comparison_genome.connectionList))
        return abs(avg_weight_self - avg_weight_comp)