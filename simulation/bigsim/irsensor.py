#!/usr/bin/python

# python 2.7.6
# pygame 1.9.2

import pygame
import operator
import math

from constants import *

class IR_Sensor():

    def __init__(self, position, initialDirection, robot, screen, obstacles, topLeft=(-4,-20), topRight=(4,-20), bottom=(0, 0), color=colors['white']):
        self.color = color
        self.position = position
        self.initialDirection = initialDirection
        self.screen = screen
        self.obstacles = obstacles
        self.direction = initialDirection
        self.originalPoints = []
        self.originalPoints.append(topLeft)
        self.originalPoints.append(topRight)
        self.originalPoints.append(bottom)
        outerPosition = tuple(map(operator.add, position, (20 * math.cos(initialDirection), -20 * math.sin(initialDirection))))
        self.points = []
        self.points.append(tuple(map(operator.add, (-4*math.sin(initialDirection), -4*math.cos(initialDirection)), outerPosition)))
        self.points.append(tuple(map(operator.add, (4*math.sin(initialDirection), 4*math.cos(initialDirection)), outerPosition)))
        self.points.append(tuple(map(operator.add, bottom, position)))
        self.rect = pygame.draw.polygon(self.screen, color, (self.points[0], self.points[1], self.points[2]))
        self.obstacleDetected = False
        self.robot = robot

    def update(self, position, direction):
        self.position = position
        self.direction = direction
        #Find the coordinates of the outer point of the triangle pointing radially away from the robot
        outerPosition = tuple(map(operator.add, position, (20*math.cos(direction+self.initialDirection),
            -20*math.sin(direction+self.initialDirection))))
        points = []
        #Update the 3 points for the ir sensor's triangle
        points.append(tuple(map(operator.add, (-4*math.sin(direction+self.initialDirection), 
            -4*math.cos(direction+self.initialDirection)), outerPosition)))
        points.append(tuple(map(operator.add, (4*math.sin(direction+self.initialDirection), 
            4*math.cos(direction+self.initialDirection)), outerPosition)))
        points.append(tuple(map(operator.add, self.originalPoints[2], position)))
        self.points = points
        #Check if the ir sensor is colliding with obstacles or other robots
        if(self.rect.collidelist(self.obstacles) != -1):
            self.color = colors['red']
            self.obstacleDetected = True
        else:
            self.color = colors['white']
            self.obstacleDetected = False
            #Check robots separately so to avoid detected robot that ir sensor is attached to
            for robot in robots:
                if(self.robot != robot and self.rect.colliderect(robot.rect)):
                    self.color = colors['red']
                    self.obstacleDetected = True
                    break

                    
    def draw(self):
        self.rect = pygame.draw.polygon(self.screen, self.color, (self.points[0], self.points[1], self.points[2]))

