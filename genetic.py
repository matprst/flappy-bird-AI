__author__= "Mathias Parisot"
__email__= "parisot.mathias.31@gmail.com"

import game, neural_net

class Population:
    population = []

    def __init__(self, size):
        for i in range(size):
            self.population.append(game.Ball())

    # def update(self):
    #     for i,elem in enumerate(self.population):
    #         if elem.dead:
    #             self.population[i] = -1
    #
    #     self.population = [elem for elem in self.population if elem != -1]

    def fitness(self):
        sumFitness = sum(elem.score for elem in self.population)

        for elem in self.population:
            elem.fitness = elem.score / sumFitness


# Pop = Population(2)
# print(Pop.population)
