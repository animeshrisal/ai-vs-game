class ConnectionGene:
    
    def __init__(self, innovation_number, input_neuron, output_neuron, weight=None, enabled = True):
        self.innovation_number = innovation_number
        self.input_neuron = input_neuron
        self.output_neuron = output_neuron
        self.enabled = enabled
        self.weight = weight

    def disable(self):
        self.enabled = False

    def copy(self):
        return ConnectionGene(innovation_number = self.innovation_number, 
                    input_neuron = self.input_neuron, 
                    output_neuron = self.output_neuron, 
                    weight = self.weight, 
                    enabled = self.enabled)
