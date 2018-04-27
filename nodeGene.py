import math
from copy import deepcopy

class NodeGene:
    def __init__(self, id, nodeType, inputValue = 0.0, inputGenes = {}, outputGenes = {}):
        self.id = id
        self.nodeType = nodeType
        self.inputValue = inputValue
        self.inputGenes = inputGenes
        self.outputGenes = outputGenes
        self.outputValue = 0.0
        self.recieved_inputs = 0
        self.sent_output = False

    def expected_inputs(self):
        return 0 if self.nodeType == 'input' else len(self.inputGenes)

    def has_fired(self):
        return self.sent_output


    def ready(self):
        recieved_all_inputs = (self.recieved_inputs == self.expected_inputs())
        return (not self.sent_output and recieved_all_inputs)

    def activation(self):
        return self.sigmoid(self.input)

    def addInputGene(self, inputGene):
        self.inputGenes[inputGene.innovation_number] = inputGene

    def addOutputGene(self, outputGene):
        self.outputGenes[outputGene.innovation_number] = outputGene

    def sigmoid(self, input):
        return 1 / (1 + math.exp(-self.inputValue)) 

    def addInput(self, inputValue):
        self.inputValue += inputValue
        self.recieved_inputs += 1

    def fire(self):
        self.sent_output = True
        for connectionGene in self.outputGenes.values():
            connectionGene.output_neuron.addInput((self.inputValue * connectionGene.weight) if connectionGene.enabled else 0)

    def calculateOutput(self):
        self.outputValue = self.sigmoid(self.outputValue)

    def getOutput(self):
        return self.outputValue

    def clone(self):
        return deepcopy(self)





