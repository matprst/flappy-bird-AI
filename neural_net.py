'''
Inspired 
'''
import numpy, math, random
from numpy import *

def sigmoid(x):
    return 1 / (1 + exp(-x))

def dsigmoid(x):
    return x * (1 - x)

def change_weights(x):
    p = random.uniform(0, 1)
    if p < 0.1:
        gaus = random.normal(0, 0.1)
        return x + gaus
    else: return x

vchange_weights = vectorize(change_weights)
vdsigmoid = vectorize(dsigmoid)

class Neural_Network:
    first_weights_matrix = 0
    second_weights_matrix = 0
    first_bias = 0
    second_bias = 0

    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        
        self.first_weights_matrix = 2 * random.rand(hidden_nodes, input_nodes) - 1
        self.second_weights_matrix = 2 * random.rand(output_nodes, hidden_nodes) - 1
        
        self.first_bias = 2 * random.rand(hidden_nodes, 1) - 1
        self.second_bias = 2 * random.rand(output_nodes, 1) - 1
        self.learning_rate = 0.2


    def feedforward(self, input):
        hidden_output = dot(self.first_weights_matrix, input)
        hidden_output = add(hidden_output, self.first_bias)
        activ_hidden_output = sigmoid(hidden_output)

        output = dot(self.second_weights_matrix, activ_hidden_output)
        output = add(output, self.second_bias)
        activ_output = sigmoid(output)

        return activ_output

    def mutate(self):
        self.first_weights_matrix = vchange_weights(self.first_weights_matrix)
        self.second_weights_matrix = vchange_weights(self.second_weights_matrix)
        self.first_bias = vchange_weights(self.first_bias)
        self.second_bias = vchange_weights(self.second_bias)

if __name__ == '__main__':

    n = Neural_Network(4, 4, 1)
    print(n.first_bias)
    print(n.first_bias.reshape(1,4))