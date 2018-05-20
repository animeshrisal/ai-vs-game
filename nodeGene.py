import math
from copy import deepcopy

class NodeGene(object):

    #Initializing neurons
    def __init__(self, id, nodeType, layer):
        self.id = id
        self.nodeType = nodeType
        self.inputValue = 1
        self.inputGenes = {}
        self.outputGenes = {}
        self.recieved_inputs = 0
        self.sent_output = False
        self.recieved_all_inputs = False
        self.layer = layer

    def expected_inputs(self):
        if self.nodeType == 'input':
            return 0
        else:
            return len(self.inputGenes)

    def has_fired(self):
        return self.sent_output

    def check_if_recieved(self):
         self.recieved_all_inputs = (self.recieved_inputs == self.expected_inputs())
         return self.recieved_all_inputs

    def ready(self):
        self.check_if_recieved()
        return (not self.sent_output and self.recieved_all_inputs)

    def activation(self):
        self.inputValue = self.sigmoid(self.inputValue)        

    def addInputGene(self, inputGene):
        self.inputGenes[inputGene.innovation_number] = inputGene

    def addOutputGene(self, outputGene):
        self.outputGenes[outputGene.innovation_number] = outputGene

    #Activation function
    def sigmoid(self, input):
        return 1 / (1 + math.exp(-input))

    def addInput(self, inputValue):
        self.inputValue += inputValue
        self.recieved_inputs += 1

        if(self.nodeType != 'input'):
            if self.check_if_recieved():
                self.activation()
        
    def set_id(self, id):
        self.id = id
    
    #The method where the passing of data from one neuron to next happens
    def fire(self):
        self.sent_output = True
        for connectionGene in self.outputGenes.values():
            if connectionGene.enabled:
                #connectionGene.output_neuron.addInput(self.inputValue * connectionGene.weight)
                connectionGene.output_neuron.addInput(self.inputValue * connectionGene.weight)
            else:
                connectionGene.output_neuron.addInput(0)

    def clone(self):
        return deepcopy(self)

    def reset_neuron(self):
        self.outputValue = 0.0
        self.recieved_inputs = 0
        self.sent_output = False




