import math

def sigmoid(input):
    return 1 / (1 + math.exp(-input)) 

print(1 * sigmoid(0.2) + 1 * sigmoid(0.6))