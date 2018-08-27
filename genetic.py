__author__= "Mathias Parisot"
__email__= "parisot.mathias.31@gmail.com"

import game, neural_net, random, numpy
from numpy import *

class Population:
    population = []
    size = 0
    best = 0
    generation_number = 1

    def __init__(self, size):
        for i in range(size):
            self.population.append(game.Ball())
        self.size = size
        self.best = self.population[0]

    def fitness(self):
        sumScore = sum(elem.score**2 for elem in self.population)
        # print("sumScore=", sumScore)

        for elem in self.population:
            elem.fitness = (elem.score**2) / sumScore

    def pick_parent(self):
        p = random.uniform(0, 1)
        index = 0
        while p > 0:
            p -= self.population[index].fitness
            index += 1
        index -= 1
        random_elem = self.population[index]
        # print('index=', index)
        child = game.Ball(random_elem.brain)
        child.brain.mutate()
        return child

    def next_generation(self):
        self.generation_number += 1
        # sort by fitness descending
        self.population.sort(key=lambda x: x.fitness, reverse=True)

        # copy best jumper
        # best = game.Ball(self.population[0].brain)
        # if self.population[0].score > self.best.score:
        #     self.best = best
        #
        # self.best.color = game.GREEN

        new_population = []

        for i in range(self.size):
            new_population.append(self.crossing(self.pick_parent(), self.pick_parent()))

        # new_population.append(self.best)
        self.population = new_population
        # print(self.population[0].color)

    def next_generation2(self):
        self.generation_number += 1
        # sort by fitness descending
        self.population.sort(key=lambda x: x.fitness, reverse=True)

        new_population = []

        #pick the 5% best jumpers from previous generation
        for i in range(int(self.size * 0.05)):
            new_ball = game.Ball(self.population[i].brain)
            new_population.append(new_ball)

        #choose randomly 75% of the previous generation and cross them
        for i in range(int(self.size * 0.75)):
            new_population.append(self.crossing(self.pick_parent(), self.pick_parent()))

        #choose randomly 15% of the previous generation
        for i in range(int(self.size * 0.15)):
            new_population.append(self.pick_parent())

        for i in range(int(self.size * 0.05)):
            new_ball = game.Ball()
            new_population.append(new_ball)

        self.population = new_population

    def crossing(self, elem1, elem2):
        w11 = elem1.brain.first_weights_matrix.reshape(1, elem1.brain.input_nodes * elem1.brain.hidden_nodes)
        w21 = elem1.brain.second_weights_matrix.reshape(1, elem1.brain.hidden_nodes * elem1.brain.output_nodes)
        b11 = elem1.brain.first_bias.reshape(1, elem1.brain.hidden_nodes)
        b21 = elem1.brain.second_bias.reshape(1, elem1.brain.output_nodes)

        w12 = elem2.brain.first_weights_matrix.reshape(1, elem1.brain.input_nodes * elem1.brain.hidden_nodes)
        w22 = elem2.brain.second_weights_matrix.reshape(1, elem1.brain.hidden_nodes * elem1.brain.output_nodes)
        b12 = elem2.brain.first_bias.reshape(1, elem1.brain.hidden_nodes)
        b22 = elem2.brain.second_bias.reshape(1, elem1.brain.output_nodes)

        # create new matrices for the child's Neural Network
        nw1 = []
        nw2 = []
        nb1 = []
        nb2 = []

        for i in range(elem1.brain.input_nodes * elem1.brain.hidden_nodes):
            p = random.randint(0,1)
            if p == 0:
                nw1.append(w11.item(i))
            else:
                nw1.append(w12.item(i))

        for i in range(elem1.brain.hidden_nodes * elem1.brain.output_nodes):
            p = random.randint(0,1)
            if p == 0:
                nw2.append(w21.item(i))
            else:
                nw2.append(w22.item(i))

        for i in range(elem1.brain.hidden_nodes):
            p = random.randint(0,1)
            if p == 0:
                nb1.append(b11.item(i))
            else:
                nb1.append(b12.item(i))

        for i in range(elem1.brain.output_nodes):
            p = random.randint(0,1)
            if p == 0:
                nb2.append(b21.item(i))
            else:
                nb2.append(b22.item(i))

        nw1 = asarray(nw1).reshape(elem1.brain.hidden_nodes,elem1.brain.input_nodes)
        nw2 = asarray(nw2).reshape(elem1.brain.output_nodes,elem1.brain.hidden_nodes)
        nb1 = asarray(nb1).reshape(elem1.brain.hidden_nodes,1)
        nb2 = asarray(nb2).reshape(elem1.brain.output_nodes,1)

        child = game.Ball(neural_net.Neural_Network(elem1.brain.input_nodes, elem1.brain.hidden_nodes, elem1.brain.output_nodes))
        child.brain.first_weights_matrix = nw1
        child.brain.second_weights_matrix = nw2
        child.brain.first_bias = nb1
        child.brain.second_bias = nb2
        return child

    def max_fitness(self):
        m = 0
        e = 0
        for elem in self.population:
            if elem.fitness > m:
                m = elem.fitness
                e = elem
        return m, e

    def max_score(self):
        m = 0
        e = 0
        for elem in self.population:
            if elem.score > m:
                m = elem.score
                e = elem
        return m, e

    def info(self):
        print("\ngeneration", self.generation_number)
        self.fitness()
        print("max fit=", self.max_fitness()[0])
        mx = self.max_score()
        print("max sco=", mx[0])
        print("matrices=")
        print(mx[1].brain.first_weights_matrix)
        print(mx[1].brain.second_weights_matrix)
        print(mx[1].brain.first_bias)
        print(mx[1].brain.second_bias)
