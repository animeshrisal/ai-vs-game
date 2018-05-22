from connectionGene import ConnectionGene
from nodeGene import NodeGene
import random
import config
from copy import deepcopy
import time
from sklearn import preprocessing

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

        self.max_hidden_neurons = 50


        #Creating input neurons
        i = 0
        self.input_neurons = []
        while i < self.num_input_neurons:
            new_neuron_id = self.get_next_neuron_id()

            self.nodeList[new_neuron_id] = NodeGene(new_neuron_id, 'input', 0)
            self.input_neurons.append(self.nodeList[new_neuron_id])
            i += 1
   
        #Creating output neurons
        i = 0
        self.output_neurons = []
        while i < self.num_output_neurons:
            new_neuron_id = self.get_next_neuron_id()
            self.nodeList[new_neuron_id] = NodeGene(new_neuron_id, 'output', 11)
            self.output_neurons.append(self.nodeList[new_neuron_id])
            i += 1

        #Creating new connection genes
        for input_neuron in self.input_neurons:
            for output_neuron in self.output_neurons:
                #random.uniform(0, 1) < config.RANDOM_THRESHOLD: #Dont want every input node to connect to all output nodes.
                innovation_number = self.innovation.getInnovation()
                self.connectionList[innovation_number] = ConnectionGene(innovation_number, input_neuron, output_neuron)
        

    ###Useful for testing
    def getNodeGenes(self):
        return self.nodeList

    def getConnectionGenes(self):
        return self.connectionList

    def addNodeGenes(self, node):
        self.nodeList.update({node.id: node})

    def addConnectionGenes(self, conn):
        self.connectionList.update({conn.innovation_number: conn})

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
                if(node2.layer <= node1.layer):
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
                    
                    newNode = NodeGene(self.get_next_neuron_id(), "hidden", random.randint(inNode.layer, outNode.layer))
                    
                    innovation_number = self.innovation.getInnovation()
                    inToNew = ConnectionGene(innovation_number, inNode, newNode, 1, True)
                    innovation_number = self.innovation.getInnovation()
                    newToOut = ConnectionGene(innovation_number, newNode, outNode, connection.weight, True)

                    
                    self.nodeList[newNode.id] = newNode
                    self.connectionList[inToNew.innovation_number] = inToNew
                    self.connectionList[newToOut.innovation_number] = newToOut
                    
                    self.hiddenneurons.append(newNode)
            
    def clone(self):
        return deepcopy(self)

    def calculateOutput(self, X):

        X = preprocessing.scale(X)
        
        for i, input_value in enumerate(X):
            self.input_neurons[i].addInput(input_value)
        
        complete = False
        while not complete:

            complete = True

            for x in self.nodeList.values():
                if x.ready():
                    x.fire()

                if not x.has_fired():
                    complete = False

        output_neuron = self.output_neurons[0]
        value = output_neuron.activation()
        self.reset_nodes()
        return True if value >= config.ACTIVATION_THRESHOLD else False

    def reset_nodes(self):
        for node_id, node in self.nodeList.items():
            node.reset_neuron()

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