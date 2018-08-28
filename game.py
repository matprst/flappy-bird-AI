#!/usr/bin/env python

__author__= "Mathias Parisot"
__email__= "parisot.mathias.31@gmail.com"

import pygame, sys, random, os, neural_net, numpy, genetic
from pygame.locals import *

WINDOW_WIDTH = 170
WINDOW_HEIGHT = 300

WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

FPS = 800

BALL_X_INIT = 50
BALL_Y_INIT = int(WINDOW_HEIGHT / 2)
BALL_SIZE_INIT = 8
BALL_VELOCITY_INIT = 5
BALL_GRAVITY_INIT = 1
BALL_LIFT_INIT = -12
BALL_COLOR_INIT = RED
BALL_SCORE_INIT = 0

PIPE_SPACE_INIT = 80
PIPE_WIDTH_INIT = 30
PIPE_COLOR_INIT = WHITE
PIPE_SPEED_INIT = -2
PIPES_DISTANCE = 120

#population
SIZE_POPULATION = 200

class Ball:
    def __init__(self, brain = None):
        self.x = BALL_X_INIT
        self.y = BALL_Y_INIT
        self.size = BALL_SIZE_INIT
        self.velocity = BALL_VELOCITY_INIT
        self.gravity = BALL_GRAVITY_INIT
        self.lift = BALL_LIFT_INIT
        self.color = BALL_COLOR_INIT
        self.score = BALL_SCORE_INIT
        self.fitness = 0
        self.dead = False

        if brain is not None:
            self.brain = brain
        else:
            self.brain = neural_net.Neural_Network(5, 1, 1)

    def draw(self, display_surf):
        if not self.dead:
            pygame.draw.circle(display_surf, self.color, (self.x, self.y), self.size, 0)

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        self.score += 1

    def jump(self):
        self.velocity += self.lift

    def increase_score(self, amount):
        self.score += amount

    def dies(self):
        self.dead = True

    def think(self, pipe):
        input = numpy.matrix([[self.y / WINDOW_HEIGHT], [pipe.x / WINDOW_WIDTH], [pipe.top_height / WINDOW_HEIGHT], [pipe.bottom_y / WINDOW_HEIGHT], [self.velocity / 10]])
        # input = numpy.matrix([[(self.y - pipe.y_space) / WINDOW_HEIGHT], [pipe.x / WINDOW_WIDTH]])
        output = self.brain.feedforward(input)

        return output[0, 0] > 0.5

    def copy(self):
        return Ball(self.brain)

class Pipe:
    def __init__(self):
        # half-pipes settings
        self.x = WINDOW_WIDTH
        self.width_space = PIPE_SPACE_INIT
        self.y_space = random.randint(int(self.width_space / 2) + 20, WINDOW_HEIGHT - int(self.width_space / 2) - 20)
        self.width = PIPE_WIDTH_INIT
        self.color = PIPE_COLOR_INIT
        self.speed = PIPE_SPEED_INIT

        # top half-pipe settings
        self.top_y = 0
        self.top_height = self.y_space - int(self.width_space / 2)

        # bottom half-pipe settings
        self.bottom_y = self.y_space + int(self.width_space / 2)
        self.bottom_height = WINDOW_HEIGHT - self.y_space + int(self.width_space / 2)

    def draw(self, display_surf):
        # draw top half-pipe
        pygame.draw.rect(display_surf, self.color, (self.x, self.top_y, self.width, self.top_height))
        # draw bottom half-pipe
        pygame.draw.rect(display_surf, self.color, (self.x, self.bottom_y, self.width, self.bottom_height))

    def update(self):
        self.x += self.speed

def main():

    global WINDOW_WIDTH, WINDOW_HEIGHT, FPS, PIPES_DISTANCE

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 0)
    pygame.display.set_caption('Flapibird')

    fpsClock = pygame.time.Clock()

    jumpers = genetic.Population(SIZE_POPULATION)

    while True:

        # initialize pipe array
        pipes = []
        pipes.append(Pipe())

        # game loop - until all jumpers are dead
        while not all(jumper.dead for jumper in jumpers.population):

            # events loop
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    jumpers.info()

                    pygame.quit()
                    sys.exit()

            closest_pipe = 0
            distance_closest_pipe = WINDOW_WIDTH

            for pipe in pipes:
                pipe.update()

                # remove the pipes not anymore in the frame
                if pipe.x < 0:
                    pipes = pipes[1:]

                # find the closest pipe from the jumpers
                if -pipe.width < pipe.x - BALL_X_INIT < distance_closest_pipe:
                    closest_pipe = pipe
                    distance_closest_pipe = pipe.x - BALL_X_INIT

            for jumper in jumpers.population:
                if not jumper.dead:

                    think = jumper.think(closest_pipe)
                    if think:
                        jumper.jump()

                    jumper.update()

                    # colisions detection
                    if jumper.y <= 0 or jumper.y >= WINDOW_HEIGHT:
                        jumper.dies()

                    if not (closest_pipe.x < jumper.x < closest_pipe.x + closest_pipe.width \
                    and not (closest_pipe.y_space - int(closest_pipe.width_space / 2) < jumper.y < closest_pipe.y_space + int(closest_pipe.width_space / 2))):
                        pass
                    else:
                        jumper.dies()

            # create new pipe
            if (WINDOW_WIDTH - pipes[-1].x) == PIPES_DISTANCE:
                pipes.append(Pipe())

            # draw game objects
            DISPLAYSURF.fill(BLACK)

            for pipe in pipes:
                pipe.draw(DISPLAYSURF)

            for jumper in jumpers.population:
                jumper.draw(DISPLAYSURF)

            pygame.display.update()
            fpsClock.tick(FPS)

        jumpers.info()
        jumpers.next_generation2()


if __name__ == '__main__':
    main()
