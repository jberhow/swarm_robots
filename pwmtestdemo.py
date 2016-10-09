#!/usr/bin/python

import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

def right_reverse(pwm):
  GPIO.output(13, GPIO.LOW)
  right_r.ChangeDutyCycle(abs(pwm))
  return

def right_forward(pwm):
  right_f.ChangeDutyCycle(abs(pwm))
  GPIO.output(11, GPIO.LOW)
  return
  
def left_reverse(pwm):
  left_r.ChangeDutyCycle(abs(pwm))
  GPIO.output(16, GPIO.LOW)
  return
  
def left_forward(pwm):
  left_f.ChangeDutyCycle(abs(pwm))
  GPIO.output(18, GPIO.LOW) 
  return 
  
def stop():
  right_f.ChangeDutyCycle(0)
  right_r.ChangeDutyCycle(0)
  left_f.ChangeDutyCycle(0)
  left_r.ChangeDutyCycle(0)
  return
  
def forward(pwm):
    right_forward(pwm)
    left_forward(pwm)
    return

def reverse(pwm):
    right_reverse(pwm)
    left_reverse(pwm)
    return

def rotate_left(pwm):
  left_forward(pwm)
  right_reverse(pwm)
  return
  
def rotate_right(pwm):
  left_reverse(pwm)
  right_forward(pwm)
  return
 
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

left_f = GPIO.PWM(17, 50)
left_r = GPIO.PWM(18, 50)
right_f = GPIO.PWM(27, 50)
right_r = GPIO.PWM(28, 50)

right_f.start(0)
right_r.start(0)
left_f.start(0)
left_r.start(0)

forward(100)
stop()
reverse(100)
stop()
rotate_right(100)
stop()
rotate_left(100)
stop()
