#!/usr/bin/python

# python 2.7.6
# pygame 1.9.2

import pygame
import sys
import time

pygame.init()

size = width, height = 640, 480

colors = {
        'black': (0,0,0),
        'red': (255,0,0),
        'green': (0,255,0),
        'blue': (0,0,255)
        }

screen = pygame.display.set_mode(size)

velocity = velocityX, velocityY = 1, 1

# TODO: create a robot class
robotPos = robotX, robotY = 50, 50
robotSize = robotW, robotH = 50, 50
robotColor = colors['green']

running = True

robot = pygame.draw.rect(screen, robotColor, (robotPos, robotSize))

# TODO: make separate functions for rendering and updating
while running:

    # close out if quit button is pressed on window
    if (pygame.event.peek(pygame.QUIT)):
        pygame.display.quit()
        running = False
        
    # update portion
    if (robot.x + robot.w > width or robot.x < 0):
        velocityX = -velocityX
    if (robot.y + robot.h > height or robot.y < 0):
        velocityY = -velocityY
    robot.move_ip(velocityX, velocityY)
        
    # render portion
    screen.fill(colors['black'], robot)
    pygame.draw.rect(screen, robotColor, robot)
    pygame.display.flip()
    pygame.time.delay(10)

sys.exit()
