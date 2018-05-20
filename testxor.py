from NEAT import NEAT

neats = NEAT()

for x in range(20):
    for i_id in neats.species:
        neats.species[i_id].generate_fitness()

    neats.start_evolution()