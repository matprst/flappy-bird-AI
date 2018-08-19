import pygame, sys, random, os
from pygame.locals import *

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

FPS = 30

BALL_X_INIT = 50
BALL_Y_INIT = int(WINDOW_HEIGHT / 2)
BALL_SIZE_INIT = 8
BALL_VELOCITY_INIT = 5
BALL_GRAVITY_INIT = 1
BALL_COLOR_INIT = RED

PIPE_SPACE_INIT = 100
PIPE_WIDTH_INIT = 10
PIPE_COLOR_INIT = WHITE
PIPE_SPEED_INIT = -2

class Ball:
    def __init__(self):
        self.x = BALL_X_INIT
        self.y = BALL_Y_INIT
        self.size = BALL_SIZE_INIT
        self.velocity = BALL_VELOCITY_INIT
        self.gravity = BALL_GRAVITY_INIT
        self.color = BALL_COLOR_INIT

    def draw(self, display_surf):
        pygame.draw.circle(display_surf, self.color, (self.x, self.y), self.size, 0)

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
        self.width_space = PIPE_SPACE_INIT
        self.y_space = random.randint(int(self.width_space / 2), WINDOW_HEIGHT - int(self.width_space / 2))
        self.color = PIPE_COLOR_INIT
        self.speed = PIPE_SPEED_INIT

        self.top_x = WINDOW_WIDTH
        self.top_y = 0
        self.top_height = self.y_space - int(self.width_space / 2)
        self.top_width = PIPE_WIDTH_INIT

        self.bottom_x = WINDOW_WIDTH
        self.bottom_y = self.y_space + int(self.width_space / 2)
        self.bottom_height = WINDOW_HEIGHT - self.y_space + int(self.width_space / 2)
        self.bottom_width = PIPE_WIDTH_INIT

    def draw(self, display_surf):
        pygame.draw.rect(display_surf, self.color, (self.top_x, self.top_y, self.top_width, self.top_height))
        pygame.draw.rect(display_surf, self.color, (self.bottom_x, self.bottom_y, self.bottom_width, self.bottom_height))

    def update(self):
        self.top_x += self.speed
        self.bottom_x += self.speed

    def x_pos(self):
        return self.top_x

def main():

    global WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK, GRAY, FPS

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 0)
    pygame.display.set_caption('Flapibird')

    fpsClock = pygame.time.Clock()

    jumper = Ball()

    pipes = []
    pipes.append(Pipe())

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif (event.type == KEYDOWN and event.key == K_SPACE):
                jumper.jump()

        DISPLAYSURF.fill(BLACK)

        jumper.update()
        jumper.draw(DISPLAYSURF)

        for pipe in pipes:
            pipe.update()
            pipe.draw(DISPLAYSURF)

            # remove the pipes not anymore in the frame
            if pipe.x_pos() < 0:
                pipes = pipes[1:]

        # create new pipe
        if pipes[-1].x_pos() % 150 == 0:
            pipes.append(Pipe())

        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == '__main__':
    main()
