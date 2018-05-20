from connectionGene import ConnectionGene
from nodeGene import NodeGene
import random
import config
from copy import deepcopy
import time

class Genome(object):

    def __init__(self, topology, innovation):
        
        self.species_id = None
        self.generation_id = None
        self.fitness = 0

        self.num_input_neurons = topology[0]
        self.num_output_neurons = topology[1]

        self.current_neuron_id = 0
        self.innovation = innovation

        self.nodeList = {}
        self.connectionList = {}
        self.hiddenneurons = []

        self.max_hidden_neurons = 10


        #Creating input neurons
        i = 0
        self.input_neurons = []
        while i < self.num_input_neurons:
            new_neuron_id = self.get_next_neuron_id()
            self.nodeList[new_neuron_id] = NodeGene(new_neuron_id, 'input', 0).clone()
            self.input_neurons.append(self.nodeList[new_neuron_id])
            i += 1
   
        #Creating output neurons
        i = 0
        self.output_neurons = []
        while i < self.num_output_neurons:
            new_neuron_id = self.get_next_neuron_id()
            self.nodeList[new_neuron_id] = NodeGene(new_neuron_id, 'output', 11).clone()
            self.output_neurons.append(self.nodeList[new_neuron_id])
            i += 1

        #Creating new connection genes
        for input_neuron in self.input_neurons:
            for output_neuron in self.output_neurons:
                #random.uniform(0, 1) < config.RANDOM_THRESHOLD: #Dont want every input node to connect to all output nodes.
                innovation_number = self.innovation.getInnovation()
                self.connectionList[innovation_number] = ConnectionGene(innovation_number, input_neuron, output_neuron).clone()
        

    ###Useful for testing
    def getNodeGenes(self):
        return self.nodeList

    def getConnectionGenes(self):
        return self.connectionList

    def addNodeGenes(self, node):
        self.nodeList.update({node.id: node.clone()})

    def addConnectionGenes(self, conn):
        self.connectionList.update({conn.innovation_number: conn.clone()})

    ###
    def mutate(self):
        for connection in self.connectionList.values():
            connection.mutate_weight()
 
        
        if random.uniform(0, 1) < config.ADD_GENE_MUTATION:
            node1 = random.choice(list(set().union(self.hiddenneurons, self.input_neurons)))
            node2 = random.choice(list(set().union(self.hiddenneurons, self.output_neurons)))
            weight = random.uniform(-1, 1)

            connectionImpossible = False
            
            if(node1.id == node2.id):
                connectionImpossible = True

            
            if(node1.nodeType == 'hidden' and node2.nodeType == 'hidden'):
                if(node2.layer < node1.layer):
                    connectionImpossible = True
                

            connectionExists = False

            for connection in self.connectionList.values():
                if(connection.input_neuron.id == node1.id and connection.output_neuron.id == node2.id):
                    connectionExists = True
                    break
                
                elif(connection.input_neuron.id == node2.id and connection.output_neuron.id == node1.id):
                    connectionExists = True
                    break

            if(connectionExists or connectionImpossible):
                return
            else:
                innovation_number = self.innovation.getInnovation()
                newConnection = ConnectionGene(innovation_number, node1, node2, weight, True)
                self.connectionList[newConnection.innovation_number] = newConnection

            
        
        
        if random.uniform(0, 1) < config.ADD_NODE_MUTATION and len(self.nodeList) <= ( self.num_input_neurons + self.num_output_neurons + self.max_hidden_neurons):
            
            if(bool(self.connectionList) == True):

                connection = random.choice(list(self.connectionList.values()))

                if connection.enabled:
                    connection.disable()

                    inNode = self.nodeList[connection.input_neuron.id]
                    outNode = self.nodeList[connection.output_neuron.id]
                    
                    newNode = NodeGene(self.get_next_neuron_id(), "hidden", random.randint(inNode.layer, outNode.layer)).clone()
                    
                    innovation_number = self.innovation.getInnovation()
                    inToNew = ConnectionGene(innovation_number, inNode, newNode, 1, True).clone()
                    innovation_number = self.innovation.getInnovation()
                    newToOut = ConnectionGene(innovation_number, newNode, outNode, connection.weight, True).clone()

                    
                    self.nodeList[newNode.id] = newNode
                    self.connectionList[inToNew.innovation_number] = inToNew
                    self.connectionList[newToOut.innovation_number] = newToOut
                    
                    self.hiddenneurons.append(newNode)
            
    def clone(self):
        return deepcopy(self)

    def calculateOutput(self):
        counter = 0
        complete = False
        while not complete:

            complete = True
        
            for x in self.nodeList.values():
                #print(x.id , ' ',len(x.inputGenes), ' ', len(x.outputGenes), ' ', x.recieved_inputs, ' ', x.nodeType)
                if x.ready():
                    x.fire()

                if not x.has_fired():
                    complete = False

                #print(x.id, x.has_fired(), x.inputValue)

        self.reset_nodes()
        return self.output_neurons[0]


    def predict(self):
        input_values = [[1, 1], [1, 0], [0, 1], [0, 0]]
        expected_output_values = [0,1,1,0]
        actual_value = [0,0,0,0]
        counter = 0
        for x in input_values:
            self.nodeList[0].inputValue = x[0]
            self.nodeList[1].inputValue = x[1]
            value = self.calculateOutput()
            if(expected_output_values[counter] == 0):
                actual_value[counter] = 1 - self.output_neurons[0].inputValue
            else:
                actual_value[counter] = self.output_neurons[0].inputValue
        
            
            print("Input 1: ", x[0], "Input 2: ", x[1], "Expected Output:", expected_output_values[counter] , "Actual Output: ", value.inputValue)
            counter += 1
        
        self.set_fitness(sum(actual_value)/4)

    def reset_nodes(self):
        for x in self.nodeList:
            self.nodeList[x].reset_neuron()

    def get_excess_genes(self, comparison_genome):
        excess_genes = []
        largest_innovation_id = max(self.connectionList.keys())

        for g_id, genome in comparison_genome.connectionList.items():
            if g_id > largest_innovation_id:
                excess_genes.append(genome)

        return excess_genes

    def get_disjoint_genes(self, comparison_genome):
        disjoint_genes = []
        largest_innovation_id = max(self.connectionList.keys())

        for g_id, genome in comparison_genome.connectionList.items():
            if not g_id in self.connectionList and g_id < largest_innovation_id:
                disjoint_genes.append(genome)

        for g_id, genome in self.connectionList.items():
            if not g_id in comparison_genome.connectionList.keys():
                disjoint_genes.append(genome)

        return disjoint_genes      

    def get_avg_weight_difference(self, comparison_genome):
        avg_weight_self = sum(c_gene.weight for c_gene in self.connectionList.values()) / len(self.connectionList)
        avg_weight_comp = sum(c_gene.weight for c_gene in comparison_genome.connectionList.values()) / len(comparison_genome.connectionList)
        return abs(avg_weight_self - avg_weight_comp)

    def is_compatible(self, comparison_genome):
        normalize_const = max(len(self.connectionList), len(comparison_genome.connectionList))
        normalize_const = normalize_const if normalize_const > 20 else 1

        num_excess_genes = len(self.get_excess_genes(comparison_genome))
        num_disjoint_genes = len(self.get_disjoint_genes(comparison_genome))
        avg_weight_difference = self.get_avg_weight_difference(comparison_genome)

        compatibility_score = (( num_excess_genes * config.EXCESS_COMPATIBILITY_CONSTANT) / normalize_const) +\
                            (( num_disjoint_genes * config.DISJOINT_COMPATIBILITY_CONSTANT) / normalize_const) +\
                            (avg_weight_difference * config.WEIGHT_COMPATIBILITY_CONSTANT)


        compatible = compatibility_score < config.COMPATIBILITY_THRESHOLD
        return compatible   
        
    def set_fitness(self, fitness):

        self.fitness = fitness

    def set_generation(self, generation_id):
        self.generation_id = generation_id

    def set_species(self, species_id):
        self.species_id = species_id

    def get_next_neuron_id(self):
        current_id = self.current_neuron_id
        self.current_neuron_id += 1
        return current_id

    def reinitialize(self):
        for connection_gene_id, connection_gene in self.connectionList.items():
            connection_gene.randomize_weight()