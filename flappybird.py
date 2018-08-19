import pygame, sys, random, os
from pygame.locals import *


WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)

FPS = 30

CIRCLE_SIZE = 8

GRAVITY = 1

class Ball:
    def __init__(self):
        self.x = 50
        self.y = int(WINDOW_HEIGHT / 2)
        self.velocity = 5
        self.gravity = GRAVITY

    def draw(self, display_surf):
        pygame.draw.circle(display_surf, RED, (self.x, self.y), CIRCLE_SIZE, 0)

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        if self.y >= WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT
            self.velocity = 0
        elif self.y <= 0:
            self.y = 0
            self.velocity = 0

    def jump(self):
        self.velocity += - self.gravity * 12

class Pipe:
    def __init__(self):
        self.width_space = 100
        self.y_space = random.randint(int(self.width_space / 2), WINDOW_HEIGHT - int(self.width_space / 2))

        self.top_x = WINDOW_WIDTH
        self.top_y = 0
        self.top_height = self.y_space - int(self.width_space / 2)
        self.top_width = 10

        self.bottom_x = WINDOW_WIDTH
        self.bottom_y = self.y_space + int(self.width_space / 2)
        self.bottom_height = WINDOW_HEIGHT - self.y_space + int(self.width_space / 2)
        self.bottom_width = 10
        # pygame.Rect(int(WINDOW_WIDTH/2), size_block, 10, size_block))

    def draw(self, display_surf):
        pygame.draw.rect(display_surf, WHITE, (self.top_x, self.top_y, self.top_width, self.top_height))
        pygame.draw.rect(display_surf, WHITE, (self.bottom_x, self.bottom_y, self.bottom_width, self.bottom_height))

    def update(self):
        self.top_x -= 2
        self.bottom_x -= 2

    def x_pos(self):
        return self.top_x

def main():

    global WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK, GRAY, FPS

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 0)
    pygame.display.set_caption('Flapibird')

    fpsClock = pygame.time.Clock()

    circle_x = 200
    circle_y = 200
    jumper = Ball()

    pipes = []
    pipes.append(Pipe())

    while True: # main game loop
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif (event.type == KEYDOWN and event.key == K_SPACE):
                # print("working")
                jumper.jump()

        DISPLAYSURF.fill(BLACK)
        # pygame.draw.circle(DISPLAYSURF, RED, (circle_x, circle_y), CIRCLE_SIZE, 0)
        jumper.update()
        jumper.draw(DISPLAYSURF)

        for pipe in pipes:
            pipe.update()
            pipe.draw(DISPLAYSURF)
            if pipe.x_pos() < 0:
                pipes = pipes[1:]

        if pipes[-1].x_pos() % 150 == 0:
            pipes.append(Pipe())

        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == '__main__':
    main()
