import config

def calculate(genome, X):
    for i, input_value in enumerate(X):
        genome.input_neurons[i].addInput(input_value)
        

    output = [False, False]
    complete = False
    while not complete:

        complete = True

        for x in genome.nodeList.values():
            if x.ready():
                x.fire()

            if not x.has_fired():
                complete = False

    output_neuron_1 = genome.output_neurons[0]
    output_neuron_2 = genome.output_neurons[1]
    value_1 = output_neuron_1.activation()
    value_2 = output_neuron_2.activation()
    genome.reset_nodes()
        
    if value_1 >= config.ACTIVATION_THRESHOLD and value_1 > value_2:
        output[0] = True
        
    if value_2 >= config.ACTIVATION_THRESHOLD and value_2 > value_1:
        output[1] = True

    return output