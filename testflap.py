from neat import NEAT
import sys
import pickle
import os.path


# Driver for NEAT solution to FlapPyBird
def evolutionary_driver():
	
	if not os.path.isfile('save.p'):
		solver = NEAT()
	else:
		solver = pickle.load(open("./save.p", "rb"))
	 
	while True:
		solver.start_evolution()
		pickle.dump(solver, open("./save.p", "wb"))

def write_genome_to_file(genome):
    # Write the genome that solves it to a file
    pass


if __name__ == "__main__":
	evolutionary_driver()
