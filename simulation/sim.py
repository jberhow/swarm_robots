#!/usr/bin/python

# python 2.7.6
# pygame 1.9.2

import pygame
import sys
import time
import math
import operator


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
automaticMode = False

class Camera():

    def __init__(self):
        self.mini_screen = pygame.Surface((160, 50))
        self.min = 9999 # for returning closest blob
         
    def draw(self, angle, distance, n):
        #self.mini_screen.fill(colors['black'])
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
                colors['blue'], self.rect.center, (
                    self.rect.center[0] + 20*math.cos(self.hangulation), 
                    self.rect.center[1] - 20*math.sin(self.hangulation)), 2)

        self.sensors = []
        self.sensors.append(IR_Sensor(tuple(map(operator.add, self.rect.center,
                                                (self.rect.height/2*math.cos(self.hangulation),
                                                 -self.rect.height/2*math.sin(self.hangulation)))),
                                      -(60 * (math.pi / 180))))

        self.sensors.append(IR_Sensor(tuple(map(operator.add, self.rect.center,
                                                (self.rect.height / 2 * math.cos(self.hangulation),
                                                 -self.rect.height / 2 * math.sin(self.hangulation)))),
                                      0))

        self.sensors.append(IR_Sensor(tuple(map(operator.add, self.rect.center,
                                                (self.rect.height / 2 * math.cos(self.hangulation),
                                                 -self.rect.height / 2 * math.sin(self.hangulation)))),
                                      (60 * (math.pi / 180))))

        self.currTimeX = time.time()
        self.currTimeY = time.time()
        self.currTimeA = time.time()
        self.forcedRotationalDifference = 0
        self.forcedTranslationalDifference = 0

        self.camera = Camera()
                

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

        for sensor in self.sensors:
            sensor.draw()

        self.direction = pygame.draw.line(screen,

                colors['blue'],self.rect.center, (
                self.rect.center[0] + 20*math.cos(self.hangulation), 
                self.rect.center[1] - 20*math.sin(self.hangulation)),
                2)
        
        screen.blit(cam_screen, (640, 0))
        # camera rendering
        # cam_screen.fill(colors['black'])
        self.camera.mini_screen.fill(colors['black'])
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
        print("Forced Rotational " + str(self.forcedRotationalDifference))
        print("Forced Translational " + str(self.forcedTranslationalDifference))
        if (self.hangulation >= math.pi):
            self.hangulation = -math.pi
        if (self.hangulation < -math.pi):
            self.hangulation = math.pi

        if (not self.sensors[0].obstacleDetected and not self.sensors[1].obstacleDetected
                and not self.sensors[2].obstacleDetected):
            if(self.forcedRotationalDifference == 0):
                rotationalDifference = self.hangulation - controller.hangulation
            else:
                rotationalDifference = self.forcedRotationalDifference
        else:
            if(self.sensors[0].obstacleDetected and self.sensors[1].obstacleDetected):
                self.forcedRotationalDifference = -25 * (math.pi / 180)
                self.forcedTranslationalDifference = 50
            elif (self.sensors[1].obstacleDetected):
                self.forcedRotationalDifference = 25 * (math.pi / 180)
                self.forcedTranslationalDifference = 50
            elif (self.sensors[2].obstacleDetected and self.sensors[1].obstacleDetected):
                self.forcedRotationalDifference = 25 * (math.pi / 180)
                self.forcedTranslationalDifference = 50
            elif(self.sensors[0].obstacleDetected or self.sensors[2].obstacleDetected):
                rotationalDifference = 0

            rotationalDifference = self.forcedRotationalDifference

         #   return
        if(abs(rotationalDifference) < math.pi/360 or (self.forcedTranslationalDifference > 0 and self.forcedRotationalDifference == 0)):
            self.forcedRotationalDifference = 0
            self.currTimeA = time.time()
            if (pygame.key.get_pressed()[pygame.K_UP] or automaticMode):
                self.move_forward()
            elif (pygame.key.get_pressed()[pygame.K_DOWN]):
                self.move_backward()
            else:
                self.currTimeX = time.time()
                self.currTimeY = time.time()
        else:
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
        # end: update wrt controller


        for sensor in self.sensors:
            sensor.update(tuple(map(operator.add, self.rect.center, (self.rect.height/2*math.cos(self.hangulation),
                -self.rect.height/2*math.sin(self.hangulation)))), self.hangulation)


    def rotate_ccw(self):
        self.hangulation = self.hangulation + (self.avel * (time.time() - self.currTimeA))
        if(self.forcedRotationalDifference < 0):
            self.forcedRotationalDifference += (self.avel * (time.time() - self.currTimeA))
            if(self.forcedRotationalDifference > 0):
                self.forcedRotationalDifference = 0
        self.currTimeA = time.time()

    def rotate_cw(self):
        self.hangulation = self.hangulation - (self.avel * (time.time() - self.currTimeA))
        if (self.forcedRotationalDifference > 0):
            self.forcedRotationalDifference -= (self.avel * (time.time() - self.currTimeA))
            if (self.forcedRotationalDifference < 0):
                self.forcedRotationalDifference = 0
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

        if (abs(self.vel * (time.time() - self.currTimeY) * math.sin(self.hangulation)) > 1):
            self.rect.move_ip(0, -self.vel * (time.time() - self.currTimeY) * math.sin(self.hangulation))
            self.direction.move_ip(0, -self.vel * (time.time() - self.currTimeY) * math.sin(self.hangulation))
            if (self.forcedTranslationalDifference > 0):
                self.forcedTranslationalDifference -= abs(self.vel * (time.time() - self.currTimeY) * math.sin(self.hangulation))
                if (self.forcedTranslationalDifference < 0):
                    self.forcedTranslationalDifference = 0
            self.currTimeY = time.time()

class IR_Sensor():

    def __init__(self, position, initialDirection, topLeft=(-4,-20), topRight=(4,-20), bottom=(0, 0), color=colors['white']):
        self.color = color
        self.position = position
        self.initialDirection = initialDirection
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
        self.rect = pygame.draw.polygon(screen, color, (self.points[0], self.points[1], self.points[2]))
        self.obstacleDetected = False

    def update(self, position, direction):
        self.position = position
        self.direction = direction
        outerPosition = tuple(map(operator.add, position, (20*math.cos(direction+self.initialDirection),
            -20*math.sin(direction+self.initialDirection))))
        points = []
        points.append(tuple(map(operator.add, (-4*math.sin(direction+self.initialDirection), 
            -4*math.cos(direction+self.initialDirection)), outerPosition)))
        points.append(tuple(map(operator.add, (4*math.sin(direction+self.initialDirection), 
            4*math.cos(direction+self.initialDirection)), outerPosition)))
        points.append(tuple(map(operator.add, self.originalPoints[2], position)))
        self.points = points

        for obstacle in obstacles:
            if(self.rect.colliderect(obstacle.rect)):
                self.color = colors['red']
                self.obstacleDetected = True
            else:
                self.color = colors['white']
                self.obstacleDetected = False
                    
    def draw(self):
        self.rect = pygame.draw.polygon(screen, self.color, (self.points[0], self.points[1], self.points[2]))

class Obstacle():

    def __init__(self, size, pos, color):
        self.size = size
        self.pos = pos
        self.color = color
        self.rect = pygame.draw.rect(screen,
                                     self.color, (self.pos, self.size))

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        
controller = Controller()
robots = []
obstacles = []
obstacles.append(Obstacle((10, 100), (250, 200), colors['green']))
#obstacles.append(Obstacle((10, 50), (250, 100), colors['red']))



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
                pygame.mouse.get_pos()[1]),45,math.pi/2,
                controller, counter))
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

