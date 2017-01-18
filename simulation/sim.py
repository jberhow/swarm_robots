#!/usr/bin/python

# python 2.7.6
# pygame 1.9.2

import pygame
import sys
import time
import math

pygame.init()
pygame.key.set_repeat(20,20)

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

class Controller():

    def __init__(self, avel=math.pi/24, pos=(int(0.9*width), 
            int(0.9*height)), 
            radius=int(0.09*height)):
        self.avel = avel
        self.pos = pos
        self.radius = radius
        self.color = colors['white']
        self.rect = pygame.draw.circle(screen, colors['white'], 
                self.pos, self.radius, 2)

        self.hangulation = math.pi/2

    def draw(self):
        self.rect = pygame.draw.circle(screen, self.color, 
                self.pos, self.radius, 2)
        self.direction = pygame.draw.line(screen,
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

    def move_backward(self):
        self.color = colors['red']


# TODO: move robot class out of sim.py into its own module
# TODO: see how to make the code more elegant, it's getting rowdy
class Robot():

    def __init__(self, pos, velx, avel, controller, size=(10, 10), 
            color=colors['green']):
        self.pos = pos
        self.size = size
        self.color = color
        self.vel = velx
        self.avel = avel
        self.controller = controller
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
                    self.rect.center[1] - 20*math.sin(self.hangulation)), 
                2)

    def update(self):
        if (self.hangulation >= math.pi):
            self.hangulation = -math.pi
        if (self.hangulation < -math.pi):
            self.hangulation = math.pi

        rotationalDifference = self.hangulation - controller.hangulation

        if(rotationalDifference == 0):
            return
        if(rotationalDifference > 0 and rotationalDifference < math.pi):
            self.rotate_cw()
        elif(rotationalDifference > 0 and rotationalDifference >= math.pi):
            self.rotate_ccw()
        elif(rotationalDifference < 0 and rotationalDifference > -math.pi):
            self.rotate_ccw()
        elif(rotationalDifference < 0 and rotationalDifference <= -math.pi):
            self.rotate_cw()


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
        
controller = Controller()
robots = []

# TODO: controls need to be handled in update()
def update():
    # close out if quit button is pressed on window
    if (pygame.event.peek(pygame.QUIT)):
        pygame.display.quit()
        sys.exit()

    # control input
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            robots.append(Robot((pygame.mouse.get_pos()[0],
                pygame.mouse.get_pos()[1]),5,math.pi/180, controller))
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                controller.rotate_ccw() 
                for robot in robots:
                    robot.rotate_ccw() 
            if event.key == pygame.K_RIGHT:
                controller.rotate_cw() 
                for robot in robots:
                    robot.rotate_cw() 
            if event.key == pygame.K_DOWN:
                controller.move_backward() 
                for robot in robots:
                    robot.move_backward() 
            if event.key == pygame.K_UP:
                controller.move_forward() 
                for robot in robots:
                    robot.move_forward()
        if event.type == pygame.KEYUP:
            controller.color = colors['white']

    controller.update()
    for robot in robots:
        robot.update()

def render():
    screen.fill(colors['black'])
    font = pygame.font.SysFont("monospace", 15)
    label = font.render(str(controller.hangulation), 1, (255, 255, 255))
    screen.blit(label, (100, 100))
    controller.draw()
    for robot in robots:
        robot.draw()
    pygame.display.flip()
    pygame.time.delay(20)


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

