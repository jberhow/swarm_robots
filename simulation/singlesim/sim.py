#!/usr/bin/python

# python 2.7.6
# pygame 1.9.2

import pygame
import sys
import time
import math
import operator
import random
import numpy

from constants import *
from irsensor import IR_Sensor
from robot import Robot
from camera import Camera
from controller import Controller
from obstacle import Obstacle


pygame.init()
pygame.key.set_repeat(20,20)


counter = 0

screen = pygame.display.set_mode(size)
controller = Controller(screen)

cam_screen = pygame.Surface((160, 480))

velocity = velocityX, velocityY = 1, 1



robots = []

obstacles = []
obstacles.append(Obstacle((10, 100), (200, 30), colors['green'], screen))
obstacles.append(Obstacle((10, 100), (200, 200), colors['green'], screen))
obstacles.append(Obstacle((100, 10), (200, 200), colors['green'], screen))
obstacleRects = []

for obstacle in obstacles:
    obstacleRects.append(obstacle.rect)

# TODO: controls need to be handled in update()
def update():
    global automaticMode
    global counter

    # close out if quit button is pressed on window
    if (pygame.event.peek(pygame.QUIT)):
        pygame.display.quit()
        sys.exit()

    # control input
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            robots.append(Robot((pygame.mouse.get_pos()[0],
                pygame.mouse.get_pos()[1]),45,math.pi/2, controller, counter,
                screen, cam_screen, obstacleRects))
            counter = counter + 1

        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                controller.rotate_ccw()

            if event.key == pygame.K_RIGHT:
                controller.rotate_cw()

            if event.key == pygame.K_DOWN:
                controller.move_backward() 

            if event.key == pygame.K_UP:
                controller.move_forward() 

            if event.key == pygame.K_a:
                automaticMode = True
            if event.key == pygame.K_m:
                automaticMode = False

        if event.type == pygame.KEYUP:
            controller.color = colors['white']
            controller.is_moving = False

    controller.update()
    for robot in robots:
        robot.update()

def render():
    screen.fill(colors['black'])
    controller.draw()
    for robot in robots:
        robot.draw()
    for obstacle in obstacles:
        obstacle.draw()
    pygame.display.flip()

# TODO: maybe make a Game object that gets instantiated in __main__
while 1:
    # update portion
    update()
        
    # render portion
    render()

