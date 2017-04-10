#!/usr/bin/python

# python 2.7.6
# pygame 1.9.2

import pygame
import math
import time
import operator
import random

from constants import *
from irsensor import IR_Sensor
from camera import Camera


#from camera import Camera

# TODO: move robot class out of sim.py into its own module
# TODO: see how to make the code more elegant, it's getting rowdy
class Robot():

    def __init__(self, pos, vel, avel, controller, n, screen, cam_screen, obstacles, size=(10, 10), 
            color=colors['green']):
        self.pos = pos
        self.size = size
        self.color = color
        self.vel = vel
        self.avel = avel
        self.controller = controller
        self.n = n
        self.screen = screen
        self.cam_screen = cam_screen
        self.obstacles = obstacles
        self.rect = pygame.draw.rect(self.screen, 
                self.color, (self.pos, self.size))

        self.hangulation = math.pi/2
        self.direction = pygame.draw.line(self.screen,
                colors['blue'], self.rect.center, (
                    self.rect.center[0] + 20*math.cos(self.hangulation), 
                    self.rect.center[1] - 20*math.sin(self.hangulation)), 2)

        self.sensors = []
        self.sensors.append(IR_Sensor(tuple(map(operator.add, self.rect.center,
                                                (self.rect.height/2*math.cos(self.hangulation),
                                                 -self.rect.height/2*math.sin(self.hangulation)))),
                                      -(60 * (math.pi / 180)), self,
                                      self.screen, self.obstacles))

        self.sensors.append(IR_Sensor(tuple(map(operator.add, self.rect.center,
                                                (self.rect.height / 2 * math.cos(self.hangulation),
                                                 -self.rect.height / 2 * math.sin(self.hangulation)))),
                                      0, self, self.screen, self.obstacles))

        self.sensors.append(IR_Sensor(tuple(map(operator.add, self.rect.center,
                                                (self.rect.height / 2 * math.cos(self.hangulation),
                                                 -self.rect.height / 2 * math.sin(self.hangulation)))),
                                      (60 * (math.pi / 180)), self,
                                      self.screen, self.obstacles))

        self.currTimeX = time.time()
        self.currTimeY = time.time()
        self.currTimeA = time.time()

        self.irRotationalDifference = 0         #A forced rotation with highest priority given when ir sensor detects an obstacle
        self.cameraRotationalDifference = 0     #A forced rotation with priority below the ir sensor for the camera
        self.forcedTranslationalDifference = 0  #A forced translational movement set by any sensor

        self.camera = Camera(self, self.cam_screen)
                

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

        for sensor in self.sensors:
            sensor.draw()

        self.direction = pygame.draw.line(self.screen,

                colors['blue'],self.rect.center, (
                self.rect.center[0] + 20*math.cos(self.hangulation), 
                self.rect.center[1] - 20*math.sin(self.hangulation)),
                2)
        
        self.screen.blit(self.cam_screen, (640, 0))
        # camera rendering
        # cam_screen.fill(colors['black'])
        #self.camera.mini_screen.fill(colors['black'])
        self.camera.draw()


    def update(self):
        #Keep robot angle withhin -pi to pi
        if (self.hangulation > math.pi):
            self.hangulation = -math.pi
        if (self.hangulation < -math.pi):
            self.hangulation = math.pi

        #If no IR sensors have detected anything
        #Follow the controller if there is no forced rotational movement
        if (not self.sensors[0].obstacleDetected and not self.sensors[1].obstacleDetected
                and not self.sensors[2].obstacleDetected):

            #TODO: Set camera rotational difference if closest robot has changed (positive = cw,negative = ccw)
            #if():
            #    cameraRotationalDifference =
            #    forcedTranslationalDistance = You can set this if you need it to move after rotating

            if(self.irRotationalDifference != 0):
                rotationalDifference = self.irRotationalDifference
                self.cameraRotationalDifference = 0
            elif(self.cameraRotationalDifference != 0):
                rotationalDifference = self.cameraRotationalDifference
            else:
                rotationalDifference = self.hangulation - self.controller.hangulation

        #If the middle sensor and an outer sensor both detect an obstacle then rotate and move away from obstacle using
        #gaussian distribution so that robots do not continually collide into each other
        else:
            if(self.sensors[0].obstacleDetected and self.sensors[1].obstacleDetected):
                self.irRotationalDifference = -random.gauss(25, 5) * (math.pi / 180)
                self.forcedTranslationalDifference = random.gauss(40, 10)
            elif (self.sensors[1].obstacleDetected):
                self.irRotationalDifference = random.gauss(25, 5) * (math.pi / 180)
                self.forcedTranslationalDifference = random.gauss(40, 10)
            elif (self.sensors[2].obstacleDetected and self.sensors[1].obstacleDetected):
                self.irRotationalDifference = random.gauss(25, 5) * (math.pi / 180)
                self.forcedTranslationalDifference = random.gauss(40, 10)
            #elif(self.sensors[0].obstacleDetected or self.sensors[2].obstacleDetected):
            #    rotationalDifference = 0

            rotationalDifference = self.irRotationalDifference

        #If no more rotation is required or there is force translational movement, move the robot
        if(abs(rotationalDifference) < math.pi/360 or (self.forcedTranslationalDifference > 0 and self.irRotationalDifference == 0 and self.cameraRotationalDifference == 0)):
            self.irRotationalDifference = 0
            self.cameraRotationalDifference = 0
            self.currTimeA = time.time()
            if (pygame.key.get_pressed()[pygame.K_UP] or automaticMode):
                self.move_forward()
            elif (pygame.key.get_pressed()[pygame.K_DOWN]):
                self.move_backward()
            else:
                self.currTimeX = time.time()
                self.currTimeY = time.time()
        else:
            #Rotate depending on the direction needed to rotate
            self.currTimeX = time.time()
            self.currTimeY = time.time()
            if(rotationalDifference > 0 and rotationalDifference < math.pi):
                self.rotate_cw()
            elif(rotationalDifference > 0 and rotationalDifference >= math.pi):
                self.rotate_ccw()
            elif(rotationalDifference < 0 and rotationalDifference > -math.pi):
                self.rotate_ccw()
            elif(rotationalDifference < 0 and rotationalDifference <= -math.pi):
                self.rotate_cw()


        for sensor in self.sensors:
            sensor.update(tuple(map(operator.add, self.rect.center, (self.rect.height/2*math.cos(self.hangulation),
                -self.rect.height/2*math.sin(self.hangulation)))), self.hangulation)

        self.camera.update()


    def rotate_ccw(self):
        self.hangulation = self.hangulation + (self.avel * (time.time() - self.currTimeA))
        if(self.irRotationalDifference < 0):
            self.irRotationalDifference += (self.avel * (time.time() - self.currTimeA))
            if(self.irRotationalDifference > 0):
                self.irRotationalDifference = 0
        if(self.cameraRotationalDifference < 0):
            self.cameraRotationalDifference += (self.avel * (time.time() - self.currTimeA))
            if(self.cameraRotationalDifference > 0):
                self.cameraRotationalDifference = 0
        self.currTimeA = time.time()

    def rotate_cw(self):
        self.hangulation = self.hangulation - (self.avel * (time.time() - self.currTimeA))
        if (self.irRotationalDifference > 0):
            self.irRotationalDifference -= (self.avel * (time.time() - self.currTimeA))
            if (self.irRotationalDifference < 0):
                self.irRotationalDifference = 0
        if (self.cameraRotationalDifference > 0):
            self.cameraRotationalDifference -= (self.avel * (time.time() - self.currTimeA))
            if (self.cameraRotationalDifference < 0):
                self.cameraRotationalDifference = 0
        self.currTimeA = time.time()

    def move_backward(self):
        if (abs(self.vel * (time.time() - self.currTimeX) * math.cos(self.hangulation)) > 1):
            self.rect.move_ip(-self.vel * (time.time() - self.currTimeX) * math.cos(self.hangulation), 0)
            self.direction.move_ip(-self.vel * (time.time() - self.currTimeX) * math.cos(self.hangulation), 0)
            self.currTimeX = time.time()

        if (abs(self.vel * (time.time() - self.currTimeY) * math.sin(self.hangulation)) > 1):
            self.rect.move_ip(0, self.vel * (time.time() - self.currTimeY) * math.sin(self.hangulation))
            self.direction.move_ip(0, self.vel * (time.time() - self.currTimeY) * math.sin(self.hangulation))
            self.currTimeY = time.time()

    def move_forward(self):
        if (abs(self.vel * (time.time() - self.currTimeX) * math.cos(self.hangulation)) > 1):
            self.rect.move_ip(self.vel * (time.time() - self.currTimeX) * math.cos(self.hangulation), 0)
            self.direction.move_ip(self.vel * (time.time() - self.currTimeX) * math.cos(self.hangulation), 0)
            if (self.forcedTranslationalDifference > 0):
                self.forcedTranslationalDifference -= abs(self.vel * (time.time() - self.currTimeX) * math.cos(self.hangulation))
                if (self.forcedTranslationalDifference < 0):
                    self.forcedTranslationalDifference = 0
            self.currTimeX = time.time()

        #
        if (abs(self.vel * (time.time() - self.currTimeY) * math.sin(self.hangulation)) > 1):
            self.rect.move_ip(0, -self.vel * (time.time() - self.currTimeY) * math.sin(self.hangulation))
            self.direction.move_ip(0, -self.vel * (time.time() - self.currTimeY) * math.sin(self.hangulation))
            if (self.forcedTranslationalDifference > 0):
                self.forcedTranslationalDifference -= abs(self.vel * (time.time() - self.currTimeY) * math.sin(self.hangulation))
                if (self.forcedTranslationalDifference < 0):
                    self.forcedTranslationalDifference = 0
            self.currTimeY = time.time()

