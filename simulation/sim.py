#!/usr/bin/python

# python 2.7.6
# pygame 1.9.2

import pygame
import sys
import time
import math

pygame.init()
pygame.key.set_repeat(10,10)

size = width, height = 640, 480

colors = {
        'black': (0,0,0),
        'white': (255,255,255),
        'red': (255,0,0),
        'green': (0,255,0),
        'blue': (0,0,255)
        }

screen = pygame.display.set_mode(size)

velocity = velocityX, velocityY = 1, 1

# TODO: move robot class out of sim.py into its own module
# TODO: see how to make the code more elegant, it's getting rowdy
class Robot():

    def __init__(self, pos, velx, avel, size=(10, 10), color=colors['green']):
        self.pos = pos
        self.size = size
        self.color = color
        self.vel = velx
        self.avel = avel
        self.rect = pygame.draw.rect(screen, 
                self.color, (self.pos, self.size))

        self.hangulation = math.pi/2
        self.direction = pygame.draw.line(screen,
                colors['white'],self.rect.center, (
                    self.rect.center[0] + 20*math.cos(self.hangulation), 
                    self.rect.center[1] - 20*math.sin(self.hangulation)), 2)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        #pygame.draw.rect(screen, colors['white'], self.direction)
        self.direction = pygame.draw.line(screen,
                colors['white'],self.rect.center, (
                    self.rect.center[0] + 20*math.cos(self.hangulation), 
                    self.rect.center[1] - 20*math.sin(self.hangulation)), 2)

    def rotate_ccw(self):
        self.hangulation = self.hangulation + self.avel

    def rotate_cw(self):
        self.hangulation = self.hangulation - self.avel

    def move_backward(self):
        self.rect.move_ip(-self.vel*math.cos(self.hangulation),
                self.vel*math.sin(self.hangulation))
        self.direction.move_ip(-self.vel*math.cos(self.hangulation),
                self.vel*math.sin(self.hangulation))
    def move_forward(self):
        self.rect.move_ip(self.vel*math.cos(self.hangulation),
                -self.vel*math.sin(self.hangulation))
        self.direction.move_ip(self.vel*math.cos(self.hangulation),
                -self.vel*math.sin(self.hangulation))
        
robot1 = Robot((50, 50), 5, math.pi/24)
robot2 = Robot((10, 10), 5, math.pi/24)

robots = [robot1, robot2]

# TODO: controls need to be handled in update()
def update():
    # close out if quit button is pressed on window
    if (pygame.event.peek(pygame.QUIT)):
        pygame.display.quit()
        sys.exit()
    # control input
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                for robot in robots:
                    robot.rotate_ccw() 
            if event.key == pygame.K_RIGHT:
                for robot in robots:
                    robot.rotate_cw() 
            if event.key == pygame.K_DOWN:
                for robot in robots:
                    robot.move_backward() 
            if event.key == pygame.K_UP:
                for robot in robots:
                    robot.move_forward() 

def render():
    screen.fill(colors['black'])
    for robot in robots:
        robot.draw()
    pygame.display.flip()
    pygame.time.delay(10)

# TODO: maybe make a Game object that gets instantiated in __main__
while 1:

    # controls
    # up, down, rotate left, rotate right
    #for event in pygame.event.get():
    #    if event.type == pygame.KEYDOWN:
    #        if event.key == pygame.K_UP:
    #           robot.move_forward() 
    #        if event.key == pygame.K_DOWN:
    #            robot.move_backward()
    #        if event.key == pygame.K_LEFT:
    #           robot.rotate_ccw() 
    #        if event.key == pygame.K_RIGHT:
    #            robot.rotate_cw()

    # update portion
    update()
        
    # render portion
    render()

