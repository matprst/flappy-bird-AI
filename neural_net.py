__author__= "Mathias Parisot"
__email__= "parisot.mathias.31@gmail.com"

import numpy, math
# import game
from numpy import *

def sigmoid(x):
    return 1 / (1 + exp(-x))

def dsigmoid(x):
    return x * (1 - x)

vdsigmoid = vectorize(dsigmoid)

class Neural_Network:
    first_weights_matrix = 0
    second_weights_matrix = 0
    first_bias = 0
    second_bias = 0

    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.first_weights_matrix = random.rand(hidden_nodes, input_nodes)
        self.second_weights_matrix = random.rand(output_nodes, hidden_nodes)
        self.first_bias = random.rand(hidden_nodes, 1)
        self.second_bias = random.rand(output_nodes, 1)
        self.learning_rate = 0.1

        print(input_nodes, hidden_nodes, output_nodes)
        print(self.first_weights_matrix)
        print(self.second_weights_matrix)


    def feedforward(self, input):
        hidden_output = self.first_weights_matrix * input
        hidden_output = add(hidden_output, self.first_bias)
        activ_hidden_output = sigmoid(hidden_output)

        output = self.second_weights_matrix * activ_hidden_output
        output = add(output, self.second_bias)
        activ_output = sigmoid(output)

        return activ_output

    def backpropagation(self, input, target):

        #feedforward
        hidden_output = self.first_weights_matrix * input
        hidden_output = add(hidden_output, self.first_bias)
        activ_hidden_output = sigmoid(hidden_output)

        output = self.second_weights_matrix * activ_hidden_output
        output = add(output, self.second_bias)
        activ_output = sigmoid(output)

        #output error
        output_errors = target - activ_output
        print("backpropagation")
        print(target)
        print(output_errors)

        # output gradient
        output_gradient = vdsigmoid(activ_output)
        print("gradient")
        print(output_gradient)
        #hadamard products
        output_gradient = multiply(self.learning_rate, multiply(output_gradient, output_errors))
        print(output_gradient)

        # output delta
        activ_hidden_output_T = activ_hidden_output.transpose()
        delta_weights_second = output_gradient * activ_hidden_output_T

        # output adjust weights
        self.second_weights_matrix = add(self.second_weights_matrix, delta_weights_second)
        # output adjust bias
        self.second_bias = add(self.second_bias, output_gradient)

        #hidden errors
        hidden_errors = self.second_weights_matrix.transpose() * output_errors
        print(hidden_errors)

        #hidden gradient
        hidden_gradient = vdsigmoid(activ_hidden_output)
        hidden_gradient = multiply(self.learning_rate, multiply(hidden_gradient, hidden_errors))

        #hidden delta
        input_T = input.transpose()
        delta_weights_first = hidden_gradient * input_T

        # hidden adjust weights
        self.first_weights_matrix = add(self.first_weights_matrix, delta_weights_first)
        # hidden adjust bias
        self.first_bias = add(self.first_bias, hidden_gradient)

        return 6


inputs = matrix('1; 2; 3; 4')
weights = matrix('1 2 3 -1; -1 6 -4 8; 9 10 11 12')

inputs = matrix('1; 1')
target = matrix('1')
n = Neural_Network(2, 2, 1)
print(n.feedforward(inputs))
print(n.backpropagation(inputs, target))

# print(matrix('1 2; 3 4'))
# print(multiply(matrix('1 2; 3 4'), matrix('1 2; 3 4')))
# print(matrix('1 2; 3 4') * matrix('1 2; 3 4'))
# print(multiply(matrix('1 2; 3 4'), 2))
