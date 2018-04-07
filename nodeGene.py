import math
from copy import deepcopy

class NodeGene:
    def __init__(self, id, nodeType, inputValue = 0.0, inputGenes = {}, outputGenes = {}):
        self.id = id
        self.nodeType = nodeType
        self.inputValue = inputValue
        self.inputGenes = inputGenes
        self.outputGenes = outputGenes
        self.sentOutput = 0.0

    def activation(self):
        return self.sigmoid(self.input)

    def addInputGene(self, inputGene):
        self.inputGenes[inputGene.innovation_number] = inputGene

    def addOutputGene(self, outputGene):
        self.outputGenes[outputGene.innovation_number] = outputGene

    def sigmoid(self, input):
        return 1 / (1 + math.exp(-self.input)) 

    def addInput(self, inputValue):
        self.inputValue += inputValue

    def fire(self):
        for connectionGene in self.outputGenes.values():
            connectionGene.output_neuron.addInput((self.inputValue * connectionGene.weight) if connectionGene.enabled else 0)

    def sendOutput():
        return sigmoid(inputValue)

    def clone(self):
        return deepcopy(self)





