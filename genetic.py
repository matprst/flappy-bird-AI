__author__= "Mathias Parisot"
__email__= "parisot.mathias.31@gmail.com"

import game

class Population:
    population = []

    def __init__(self, size):
        for i in range(size):
            self.population.append(game.Ball())

Pop = Population(2)
print(Pop.population)
