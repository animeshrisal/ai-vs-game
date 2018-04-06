import math

class NodeGene:
    def __init__(self, id, nodeType, inputValue = 0.0, inputGenes = {}, outputGenes = {}):
        self.id = id
        self.nodeType = nodeType
        self.inputValue = inputValue
        self.inputGenes = inputGenes
        self.outputGenes = outputGenes

    def activation(self):
        return self.sigmoid(self.input)

    def addInputGene(self, inputGene):
        inputGenes.update({inputGene.innovation_number: inputGene})

    def addOutputGene(self, outputGene):
        outputGenes.update({outputGene.innovation_number: outputGene})

    def sigmoid(self, input):
        return 1 / (1 + math.exp(-self.input)) 

    def addInput(self, inputValue):
        self.inputValue += inputValue

    def fire(self):
        for connectionGene in outputGenes.values():
            connectionGene.output_neuron.addInput((self.activation() * connectionGene.weight) if connectionGene.enabled else 0)

    '''
    def copy(self):
        return NodeGene(id = self.id, 
                        nodeType = self.nodeType, 
                        inputValue = self.inputValue, 
                        inputGenes = self.inputGenes, 
                        outputGenes = self.outputGenes)
    '''





