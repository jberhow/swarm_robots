#!/usr/bin/python

# python 2.7.6
# pygame 1.9.2

import math
import pygame
#from robot import Robot

from constants import *

class Camera():

    def __init__(self, myrobot, cam_screen):
        self.mini_screen = pygame.Surface((160, 50))
        self.hanglitude_list = []
        self.myrobot = myrobot
        self.hanglitude_list = []
        self.cam_screen = cam_screen
        
    def update(self):
        self.hanglitude_list = robots[:]
        for robot in robots:
            if (robot == self.myrobot):
                pass
            else:
                angle = math.atan2((self.myrobot.rect.center[1] - 
                    robot.rect.center[1]),(self.myrobot.rect.center[0] -
                        robot.rect.center[0]))
                distance = math.fabs(math.sqrt((self.myrobot.rect.center[0] -
                    robot.rect.center[0])**2 + (self.myrobot.rect.center[1] -
                        robot.rect.center[1])**2))
                self.hanglitude_list[robot.n] = (angle +
                        self.myrobot.hangulation, distance)

    def draw(self):
        self.mini_screen.fill(colors['black'])

        if self.hanglitude_list:
            if not isinstance(self.hanglitude_list[0], Robot):
                closest = self.hanglitude_list[0]
            else:
                closest = (9999, 9999)
            for hanglitude in self.hanglitude_list:
                if not isinstance(hanglitude, Robot):
                    if (hanglitude[1] < closest[1]):
                        closest = hanglitude
                    # y = mx + b converting angles to x-axis
                    start_point = 80*hanglitude[0]/math.pi+80
                    # height will be 50 pixels tall
                    end_point = -hanglitude[1] / 8. + 50
                    pygame.draw.rect(self.mini_screen, colors['green'],
                            ( (0, 0),(160, 50) ), 2)
                    pygame.draw.line(self.mini_screen, colors['white'],
                            (int(start_point), 50),
                            (int(start_point), 50 - int(end_point)))

            start_point = 80*closest[0]/math.pi+80
            end_point = -closest[1] / 8. + 50
            pygame.draw.line(self.mini_screen, colors['red'],
                    (int(start_point), 50),
                    (int(start_point), 50 - int(end_point)))
            
            self.cam_screen.blit(self.mini_screen, (0, self.myrobot.n*50))

