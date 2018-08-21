__author__= "Mathias Parisot"
__email__= "parisot.mathias.31@gmail.com"

import game, neural_net

class Population:
    population = []

    def __init__(self, size):
        for i in range(size):
            self.population.append(game.Ball())

    def draw(self, display_surf):
        for ball in self.population:
            ball.draw(display_surf)

# Pop = Population(2)
# print(Pop.population)
