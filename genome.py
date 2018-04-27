from connectionGene import ConnectionGene
from nodeGene import NodeGene
import random

class Genome:

    def __init__(self, nodeList = {}, connectionList = {}):
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

        inNode = self.nodeList[connection.input_neuron.id]
        outNode = self.nodeList[connection.output_neuron.id]

        connection.disable()

        newNode = NodeGene(len(self.nodeList) + 1, 'hidden')

        inToNew = ConnectionGene(innovation_number.getInnovation(), inNode, newNode, 1, True)
        newToOut = ConnectionGene(innovation_number.getInnovation(), newNode, outNode, connection.weight, True)

        self.nodeList.update({newNode.id : newNode.clone()})
        self.connectionList.update({inToNew.innovation_number : inToNew})
        self.connectionList.update({newToOut.innovation_number : newToOut})

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
            

       