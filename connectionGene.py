import random as rand

import config

class ConnectionGene(object):
    
    def __init__(self, innovation_number, input_neuron, output_neuron, weight=None, enabled = True):
        self.innovation_number = innovation_number
        
        self.input_neuron = input_neuron
        input_neuron.addOutputGene(self)
        
        self.output_neuron = output_neuron
        output_neuron.addInputGene(self)
        
        self.enabled = enabled
        self.weight = weight

        if self.weight is None:
            self.randomize_weight()

    def disable(self):
        self.enabled = False

    def mutate_weight(self):
        if rand.uniform(0, 1) < config.WEIGHT_MUTATION_RATE:
            if rand.uniform(0, 1) < config.UNIFORM_WEIGHT_MUTATION_RATE:
                self.weight += rand.uniform(-0.1, 0.1)

            else:
                self.randomize_weight()
                
    def randomize_weight(self):
        self.weight = rand.uniform(-2, 2)

    def copy(self):
        return ConnectionGene(innovation_number = self.innovation_number, 
        input_neuron = self.input_neuron, 
        output_neuron = self.output_neuron, 
        weight= self.weight,
        enabled = self.enabled)


