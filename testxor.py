from NEAT import NEAT

neats = NEAT()

for x in range(200):
    for i_id in neats.species:
        neats.species[i_id].generate_fitness()

    neats.start_evolution()