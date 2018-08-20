__author__= "Mathias Parisot"
__email__= "parisot.mathias.31@gmail.com"

import numpy, math
# import game
from numpy import *

def sigmoid(x):
    return 1 / (1 + exp(-x))

class Neural_Network:
    first_weights_matrix = 0
    second_weights_matrix = 0

    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.first_weights_matrix = random.rand(hidden_nodes, input_nodes)
        self.second_weights_matrix = random.rand(output_nodes, hidden_nodes)
        print(input_nodes, hidden_nodes, output_nodes)
        print(self.first_weights_matrix)
        print(self.second_weights_matrix)

    def feedforward(self, input):
        hidden_output = self.first_weights_matrix * input
        activ_hidden_output = sigmoid(hidden_output)

        output = self.second_weights_matrix * activ_hidden_output
        activ_output = sigmoid(output)

        return activ_output

    def backpropagation(self, input, target):
        output = self.feedforward(input)

        #error
        error = target - output

        print(input, output, target, error)
        return error


inputs = matrix('1; 2; 3; 4')
weights = matrix('1 2 3 -1; -1 6 -4 8; 9 10 11 12')

print(inputs)
print(weights)
print(weights*inputs)
print(type(squeeze(asarray(weights))))
print(type(weights))

inputs = matrix('1; 1')
target = matrix('1')
n = Neural_Network(2, 2, 1)
print(n.feedforward(inputs))
print(n.backpropagation(inputs, target))
