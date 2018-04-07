from nodeGene import NodeGene

class ConnectionGene:
    
    def __init__(self, innovation_number, input_neuron, output_neuron, weight=None, enabled = True):
        self.innovation_number = innovation_number
        
        self.input_neuron = input_neuron
        input_neuron.addOutputGene(self)
        
        self.output_neuron = output_neuron
        output_neuron.addInputGene(self)
        
        self.enabled = enabled
        self.weight = weight

        if self.weight is None:
            self.weight = 0.5



    def disable(self):
        self.enabled = False

    def copy(self):
        return ConnectionGene(innovation_number = self.innovation_number, 
                    input_neuron = self.input_neuron, 
                    output_neuron = self.output_neuron, 
                    weight = self.weight, 
                    enabled = self.enabled)

