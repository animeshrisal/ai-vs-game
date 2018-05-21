import math
from copy import deepcopy
import numpy as np

class NodeGene(object):

    #Initializing neurons
    def __init__(self, id, nodeType, layer):
        self.id = id
        self.nodeType = nodeType
        self.inputValue = 0.0
        self.inputGenes = {}
        self.outputGenes = {}
        self.recieved_inputs = 0
        self.sent_output = False
        self.layer = layer

    def expected_inputs(self):
        if self.nodeType == 'input':
            return 1
        else:
            return len(self.inputGenes)

    def has_fired(self):
        return self.sent_output

    def ready(self):
        recieved_all_inputs = (self.recieved_inputs == self.expected_inputs())
        return (not self.sent_output and recieved_all_inputs)

    def activation(self):
        return self.sigmoid(self.inputValue)        

    def addInputGene(self, inputGene):
        self.inputGenes[inputGene.innovation_number] = inputGene

    def addOutputGene(self, outputGene):
        self.outputGenes[outputGene.innovation_number] = outputGene

    #Activation function
    def sigmoid(self, input):
        return (2.0 / (1.0 + math.exp(-4.9 * input)) - 1.0)

    def addInput(self, value):
        self.inputValue += value
        self.recieved_inputs += 1   
        
    def set_id(self, id):
        self.id = id
    
    #The method where the passing of data from one neuron to next happens
    def fire(self):
        self.sent_output = True
        for connectionGene in self.outputGenes.values():
            if connectionGene.enabled:
                #connectionGene.output_neuron.addInput(self.inputValue * connectionGene.weight)
                connectionGene.output_neuron.addInput(self.activation() * connectionGene.weight)
            else:
                connectionGene.output_neuron.addInput(0)

    def reset_neuron(self):
        self.inputValue = 0.0
        self.recieved_inputs = 0
        self.sent_output = False




