#!/usr/bin/python

# python 2.7.6
# pygame 1.9.2

import pygame
import math

from constants import *

class Controller():

    def __init__(self, screen, avel=math.pi/24, pos=(int(0.9*640), 
            int(0.9*height)), 
            radius=int(0.09*height)):
        self.screen = screen
        self.avel = avel
        self.pos = pos
        self.radius = radius
        self.color = colors['white']
        self.rect = pygame.draw.circle(self.screen, colors['white'], 
                self.pos, self.radius, 2)

        self.hangulation = math.pi/2
        self.is_moving = False

    def draw(self):
        self.rect = pygame.draw.circle(self.screen, self.color, 
                self.pos, self.radius, 2)
        self.direction = pygame.draw.line(self.screen,
                self.color ,self.rect.center, (
                    self.rect.center[0] + 
                    self.radius*math.cos(self.hangulation), 
                    self.rect.center[1] - 
                    self.radius*math.sin(self.hangulation)), 2)

    def update(self):
        if (self.hangulation > math.pi):
            self.hangulation = -math.pi
        if (self.hangulation < -math.pi):
            self.hangulation = math.pi

    def rotate_ccw(self):
        self.hangulation = self.hangulation + self.avel

    def rotate_cw(self):
        self.hangulation = self.hangulation - self.avel

    def move_forward(self):
        self.color = colors['green']
        self.is_moving = True

    def move_backward(self):
        self.color = colors['red']
        self.is_moving = True

