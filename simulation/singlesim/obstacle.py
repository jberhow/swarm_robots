#!/usr/bin/python

# python 2.7.6
# pygame 1.9.2

import pygame

class Obstacle():

    def __init__(self, size, pos, color, screen):
        self.size = size
        self.pos = pos
        self.color = color
        self.screen = screen
        self.rect = pygame.draw.rect(self.screen,
                                     self.color, (self.pos, self.size))

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        
