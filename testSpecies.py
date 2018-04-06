from species import Species
from genome import Genome

parent = Genome()
species1 = Species(1, 200, parent)

for x in species1.genomes.values():
    print(x)