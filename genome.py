from connectionGene import ConnectionGene
from nodeGene import NodeGene
import numpy as np
import random

class Genome:

    def __init__(self):
        self.nodeList = {}
        self.connectionList = {}

    def getNodeGenes(self):
        return self.nodeList

    def getConnectionGenes(self):
        return self.connectionList

    def addNodeGenes(self, node):
        self.nodeList.update({node.id: node.copy()})

    def addConnectionGenes(self, ConnectionGene):
        self.connectionList.update({ConnectionGene.innovation_number: ConnectionGene.copy()})

    def addConnectionMutation(self, innovation_number):
        node1 = self.nodeList[random.randint(1, len(self.nodeList))]
        node2 = self.nodeList[random.randint(1, len(self.nodeList))]
        weight = random.uniform(0, 1)

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
            if(connection.input_neuron == node1.id and connection.output_neuron == node2.id):
                connectionExists = True
                break
            
            elif(connection.input_neuron == node2.id and connection.output_neuron == node1.id):
                connectionExists = True
                break

        if(connectionExists or connectionImpossible):
            return


        newConnection = ConnectionGene(innovation_number.getInnovation(), node2.id if reverse else node1.id, node1.id if reverse else node2.id, weight, True)
        self.connectionList.update({newConnection.innovation_number : newConnection})

    def addNodeMutation(self, innovation_number):
        randomValue = random.randint(1, len(self.connectionList) -1)
        connection = self.connectionList[randomValue]

        inNode = self.nodeList[connection.input_neuron]
        outNode = self.nodeList[connection.output_neuron]

        connection.disable()

        newNode = NodeGene(len(self.connectionList), 'hidden')

        inToNew = ConnectionGene(innovation_number.getInnovation(), inNode.id, newNode.id, 1, True)
        newToOut = ConnectionGene(innovation_number.getInnovation(), newNode.id, outNode.id, connection.weight, True)

        self.nodeList.update({newNode.id : newNode.copy()})
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
