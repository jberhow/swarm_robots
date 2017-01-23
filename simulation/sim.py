#!/usr/bin/python

# python 2.7.6
# pygame 1.9.2

import pygame
import sys
import time
import math

pygame.init()
pygame.key.set_repeat(20,20)

size = width, height = 800, 480

colors = {
        'black': (0,0,0),
        'white': (255,255,255),
        'red': (255,0,0),
        'green': (0,255,0),
        'blue': (0,0,255)
        }

robots = []
counter = 0

screen = pygame.display.set_mode(size)
cam_screen = pygame.Surface((160, 480))

velocity = velocityX, velocityY = 1, 1

class Camera():

    def __init__(self):
        self.mini_screen = pygame.Surface((160, 50))
        self.min = 9999 # for returning closest blob
         
    def draw(self, angle, distance, n):
        # y = mx + b convering angles to x-axis
        start_point = 80*angle/math.pi+80
        # height will be 50 pixels tall
        end_point = -distance / 8. + 50
        pygame.draw.rect(self.mini_screen, colors['green'],
                ( (0, 0),(160, 50) ), 2)
        if (distance <= self.min):
            self.min = distance
            pygame.draw.line(self.mini_screen, colors['red'],
                    (int(start_point), 50),
                    (int(start_point), 50 - int(end_point)))
        else:
            pygame.draw.line(self.mini_screen, colors['white'],
                    (int(start_point), 50),
                    (int(start_point), 50 - int(end_point)))


class Controller():

    def __init__(self, avel=math.pi/24, pos=(int(0.9*640), 
            int(0.9*height)), 
            radius=int(0.09*height)):
        self.avel = avel
        self.pos = pos
        self.radius = radius
        self.color = colors['white']
        self.rect = pygame.draw.circle(screen, colors['white'], 
                self.pos, self.radius, 2)

        self.hangulation = math.pi/2
        self.is_moving = False

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
        self.is_moving = True

    def move_backward(self):
        self.color = colors['red']
        self.is_moving = True


# TODO: move robot class out of sim.py into its own module
# TODO: see how to make the code more elegant, it's getting rowdy
class Robot():

    def __init__(self, pos, vel, avel, controller, n, size=(10, 10), 
            color=colors['green']):
        self.pos = pos
        self.size = size
        self.color = color
        self.vel = vel
        self.avel = avel
        self.controller = controller
        self.n = n
        self.rect = pygame.draw.rect(screen, 
                self.color, (self.pos, self.size))

        self.hangulation = math.pi/2
        self.direction = pygame.draw.line(screen,
                colors['white'],self.rect.center, (
                    self.rect.center[0] + 
                    20*math.cos(self.hangulation), 
                    self.rect.center[1] - 
                    20*math.sin(self.hangulation)), 2)
        self.camera = Camera()
                
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        #pygame.draw.rect(screen, colors['white'], self.direction)
        self.direction = pygame.draw.line(screen,
                colors['white'],self.rect.center, (
                self.rect.center[0] + 20*math.cos(self.hangulation), 
                self.rect.center[1] - 20*math.sin(self.hangulation)), 
                2)
        
        screen.blit(cam_screen, (640, 0))
        # camera rendering
        # cam_screen.fill(colors['black'])
        for robot in robots:
            if (robot == self):
                pass
            else:
                angle = math.atan2((self.rect.center[1] - 
                    robot.rect.center[1]),(self.rect.center[0] -
                        robot.rect.center[0]))
                distance = math.fabs(math.sqrt((self.rect.center[0] -
                    robot.rect.center[0])**2 + (self.rect.center[1] -
                        robot.rect.center[1])**2))
                self.camera.draw(angle, distance, self.n)
        
        cam_screen.blit(self.camera.mini_screen, (0, self.n*50))

    def update(self):

        # update wrt controller
        if (self.hangulation >= math.pi):
            self.hangulation = -math.pi
        if (self.hangulation < -math.pi):
            self.hangulation = math.pi

        rotationalDifference = ( self.hangulation - 
                controller.hangulation )

        if ( controller.is_moving ):
            if(rotationalDifference == 0):
                return
            if(rotationalDifference > 0 and 
                    rotationalDifference < math.pi):
                self.rotate_cw()
            elif(rotationalDifference > 0 and 
                    rotationalDifference >= math.pi):
                self.rotate_ccw()
            elif(rotationalDifference < 0 and 
                    rotationalDifference > -math.pi):
                self.rotate_ccw()
            elif(rotationalDifference < 0 and 
                   rotationalDifference <= -math.pi):
                self.rotate_cw()
        # end: update wrt controller



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

# TODO: controls need to be handled in update()
def update():
    global counter
    # close out if quit button is pressed on window
    if (pygame.event.peek(pygame.QUIT)):
        pygame.display.quit()
        sys.exit()

    # control input
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            robots.append(Robot((pygame.mouse.get_pos()[0],
                pygame.mouse.get_pos()[1]),5,math.pi/180, 
                controller, counter))
            counter = counter + 1
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
            controller.is_moving = False

    controller.update()
    for robot in robots:
        robot.update()

def render():
    screen.fill(colors['black'])
    font = pygame.font.SysFont("monospace", 15)
    label = font.render(str(controller.hangulation), 1, 
            colors['white'])
    screen.blit(label, (100, 100))
    controller.draw()
    for robot in robots:
        robot.draw()
    pygame.display.flip()
    pygame.time.delay(20)

# TODO: maybe make a Game object that gets instantiated in __main__
while 1:

    # update portion
    update()
        
    # render portion
    render()

