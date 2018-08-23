__author__= "Mathias Parisot"
__email__= "parisot.mathias.31@gmail.com"

import game, neural_net, random, numpy
from numpy import *

class Population:
    population = []
    size = 0
    best = 0

    def __init__(self, size):
        for i in range(size):
            self.population.append(game.Ball())
        self.size = size
        self.best = self.population[0]

    # def update(self):
    #     for i,elem in enumerate(self.population):
    #         if elem.dead:
    #             self.population[i] = -1
    #
    #     self.population = [elem for elem in self.population if elem != -1]

    def fitness(self):
        sumScore = sum(elem.score for elem in self.population)
        print("sumScore=", sumScore)

        for elem in self.population:
            elem.fitness = elem.score / sumScore

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
        # sort by fitness descending
        self.population.sort(key=lambda x: x.fitness, reverse=True)

        # copy best jumper
        best = game.Ball(self.population[0].brain)
        if self.population[0].score > self.best.score:
            self.best = best

        self.best.color = game.GREEN

        new_population = []

        for i in range(self.size - 1):
            new_population.append(self.crossing(self.pick_parent(), self.pick_parent()))

        new_population.append(self.best)
        self.population = new_population
        print(self.population[0].color)

    def crossing(self, elem1, elem2):
        w11 = elem1.brain.first_weights_matrix.reshape(1, 16)
        w21 = elem1.brain.second_weights_matrix.reshape(1, 4)
        b11 = elem1.brain.first_bias.reshape(1, 4)
        b21 = elem1.brain.second_bias.reshape(1, 1)

        w12 = elem2.brain.first_weights_matrix.reshape(1, 16)
        w22 = elem2.brain.second_weights_matrix.reshape(1, 4)
        b12 = elem2.brain.first_bias.reshape(1, 4)
        b22 = elem2.brain.second_bias.reshape(1, 1)

        # create new matrices for the child's Neural Network
        nw1 = []
        nw2 = []
        nb1 = []
        nb2 = []

        for i in range(16):
            p = random.randint(0,1)
            if p == 0:
                nw1.append(w11.item(i))
            else:
                nw1.append(w12.item(i))

        for i in range(4):
            p = random.randint(0,1)
            if p == 0:
                nw2.append(w21.item(i))
            else:
                nw2.append(w22.item(i))

        for i in range(4):
            p = random.randint(0,1)
            if p == 0:
                nb1.append(b11.item(i))
            else:
                nb1.append(b12.item(i))

        for i in range(1):
            p = random.randint(0,1)
            if p == 0:
                nb2.append(b21.item(i))
            else:
                nb2.append(b22.item(i))

        nw1 = asarray(nw1).reshape(4,4)
        nw2 = asarray(nw2).reshape(1,4)
        nb1 = asarray(nb1).reshape(4,1)
        nb2 = asarray(nb2).reshape(1,1)

        child = game.Ball(neural_net.Neural_Network(4, 4, 1))
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
