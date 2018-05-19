from NEAT import NEAT

neats = NEAT()

network = neats.species[0].genomes[0]

for x in range(10):
    network.mutate()

network.calculateOutput()

