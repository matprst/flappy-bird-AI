__author__= "Mathias Parisot"
__email__= "parisot.mathias.31@gmail.com"

import numpy, math, random
# import game
from numpy import *

def sigmoid(x):
    return 1 / (1 + exp(-x))

def dsigmoid(x):
    return x * (1 - x)

def change_weights(x):
    p = random.uniform(0, 1)
    if p < 0.02:
        sign = random.choice([-1, 1])
        return x + x * sign * 0.1
    else: return x

vchange_weights = vectorize(change_weights)
vdsigmoid = vectorize(dsigmoid)

class Neural_Network:
    first_weights_matrix = 0
    second_weights_matrix = 0
    first_bias = 0
    second_bias = 0

    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        # print(input_nodes, hidden_nodes, output_nodes)
        self.first_weights_matrix = 2 * random.rand(hidden_nodes, input_nodes) - 1
        self.second_weights_matrix = 2 * random.rand(output_nodes, hidden_nodes) - 1
        # print(self.second_weights_matrix)
        self.first_bias = 2 * random.rand(hidden_nodes, 1) - 1
        self.second_bias = 2 * random.rand(output_nodes, 1) - 1
        self.learning_rate = 0.2

    def feedforward(self, input):
        hidden_output = dot(self.first_weights_matrix, input)
        hidden_output = add(hidden_output, self.first_bias)
        activ_hidden_output = sigmoid(hidden_output)
        # print(activ_hidden_output)

        output = dot(self.second_weights_matrix, activ_hidden_output)
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

        # output gradient
        output_gradient = vdsigmoid(activ_output)
        #hadamard products
        output_gradient = multiply(self.learning_rate, multiply(output_gradient, output_errors))

        # output delta
        activ_hidden_output_T = activ_hidden_output.transpose()
        delta_weights_second = output_gradient * activ_hidden_output_T

        # output adjust weights
        self.second_weights_matrix = add(self.second_weights_matrix, delta_weights_second)
        # output adjust bias
        self.second_bias = add(self.second_bias, output_gradient)

        #hidden errors
        hidden_errors = self.second_weights_matrix.transpose() * output_errors

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

    def mutate(self):
        self.first_weights_matrix = vchange_weights(self.first_weights_matrix)
        self.second_weights_matrix = vchange_weights(self.second_weights_matrix)
        self.first_bias = vchange_weights(self.first_bias)
        self.second_bias = vchange_weights(self.second_bias)


#
# a = matrix('1, 2; 3 4')
# b = matrix('2; 2')
# print(a*b)

if __name__ == '__main__':

    n = Neural_Network(4, 4, 1)
    # print(n.first_weights_matrix)
    # print(n.first_weights_matrix.reshape(1, 16))
    # print(n.second_weights_matrix)
    # print(n.second_weights_matrix.reshape(1, 4))
    print(n.first_bias)
    print(n.first_bias.reshape(1,4))
    # print(n.second_bias)
    # print(n.second_bias.reshape(1, 1))
    # n.mutate()
    # print(n.first_weights_matrix)
    # print(n.second_weights_matrix)
    # print(n.first_bias)
    # print(n.second_bias)
    # training_data = [
    #     {
    #     'inputs': matrix('0; 1'),
    #     'targets': matrix('1')
    #     },
    #     {
    #     'inputs': matrix('1; 0'),
    #     'targets': matrix('1')
    #     },
    #     {
    #     'inputs': matrix('0; 0'),
    #     'targets': matrix('0')
    #     },
    #     {
    #     'inputs': matrix('1; 1'),
    #     'targets': matrix('0')
    #     },
    # ]
    #
    # for j in range(5):
    #     n = Neural_Network(2, 2, 1)
    #     for i in range(50000):
    #         index = random.randint(0, 4)
    #         data = training_data[index]
    #         n.backpropagation(data['inputs'], data['targets'])
    #
    #     print("\nTEST\n")
    #     print(n.first_weights_matrix)
    #     print(n.second_weights_matrix)
    #     print(n.feedforward(matrix('0; 1')))
    #     print(n.feedforward(matrix('1; 0')))
    #     print(n.feedforward(matrix('0; 0')))
    #     print(n.feedforward(matrix('1; 1')))
