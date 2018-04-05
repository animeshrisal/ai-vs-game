from connectionGene import ConnectionGene
from nodeGene import NodeGene
import numpy as np
from random import *

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

    def addConnectionMutation():
        randomValue = randint(1, len(nodeList))
        node1 = nodeList[randomValue]
        node2 = nodeList[ramdomValue]
        weight = random.uniform(0, 1)

        reversed = False

        if(node1.nodeType == 'hidden' and node2.nodeType == 'input'):
            reverse = True 

        if(node1.nodeType == 'output' and node2.nodeType == 'hidden'):
            reverse = True

        if(node1.nodeType == 'output' and node2.nodeType == 'input'):
            reverse = True

        connectionExists = False

        for connection in connectionList:
            if(connection.input_neuron == node1.id and connection.output_node == node2.id):
                connectionExists = True
                break
            
            elif(connection.input_neuron == node1.id and connection.output_node == node2.id):
                connectionExists = True
                break

        if connectionExists:
            return

        newConnection = connectionGene(0, node2.id if reverse else node1.id, node1.id if reverse else node2.id, weight, True)
        connectionList.append(newConnection)

    def addNodeMutation():
        randomValue = randint(1, len(connectionList))
        connection = connectionList.index(randomValue)

        inNode = nodeList.index(randomValue)
        outNode = nodeList.index(ramdomValue)

        connection.disable()

        newNode = nodeGene('hidden', len(connectionList))

        inToNew = connectionGene(0, inNode.id, newNode.id, 1, true)
        newToOut = connectionGene(0, newNode.id, outNode.id, connection.weight, true)

        nodeList.append(newNode)
        connectionList.append(inToNew)
        connectionList.append(newToOut)

    def crossover(parent1, parent2):
        child = Genome()

        for parent1Node in parent1.getNodeGenes().values():
            child.addNodeGenes(parent1Node.copy())

        for parent1Node in parent1.getConnectionGenes().values():
            if parent1Node.innovation_number in parent2.getConnectionGenes(): 
                truthValue = bool(random.getrandbits(1))
                childConGene = parent1Node.copy if truthValue else parent2.getConnectionGenes().index(parent1Node.innovation).copy()
            else:
                childConGene = parent1Node.copy()
                child.addConnectionGenes(childConGene)

        return child
