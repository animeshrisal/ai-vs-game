from NEAT import NEAT

neats = NEAT()

neats.start_evolution()

for i_id in neats.species:
    neats.species[i_id].generate_fitness()

neats.start_evolution()

for i_id in neats.species:
    neats.species[i_id].generate_fitness()

neats.start_evolution()

for i_id in neats.species:
    neats.species[i_id].generate_fitness()

neats.start_evolution()

for i_id in neats.species:
    neats.species[i_id].generate_fitness()

neats.start_evolution()

for i_id in neats.species:
    neats.species[i_id].generate_fitness()

    

for i_id in neats.species:
    print(neats.species[i_id].avg_max_fitness_achieved)



