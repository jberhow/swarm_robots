#!/usr/bin/python

#IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!
#IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!
#IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!
#IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!
#IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!
#IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!
#IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!
#WAIT UNTIL THE PITCH & ROLL STABILIZE TO 0 BEFORE MOVING THE BOARD
#WAIT UNTIL THE PITCH & ROLL STABILIZE TO 0 BEFORE MOVING THE BOARD
#WAIT UNTIL THE PITCH & ROLL STABILIZE TO 0 BEFORE MOVING THE BOARD
#WAIT UNTIL THE PITCH & ROLL STABILIZE TO 0 BEFORE MOVING THE BOARD
#WAIT UNTIL THE PITCH & ROLL STABILIZE TO 0 BEFORE MOVING THE BOARD
#IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!
#IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!
#IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!
#IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!

import smbus
import time
import math
import socket
import sys


  
HOST = '172.24.1.1'   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
#s.listen(10)
#print 'Socket now listening'
 
#wait to accept a connection - blocking call
#conn, addr = s.accept()
#print 'Connected with ' + addr[0] + ':' + str(addr[1]) 

bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

XG_DEVICE_ADDRESS = 0x68      #7 bit address (will be left shifted to add the read write bit)
M_DEVICE_ADDRESS = 0x0C
NUM_SAMPLES = 1

#print format(bus.read_byte_data(XM_DEVICE_ADDRESS, 0x0F), '#04x')

bus.write_byte_data(XG_DEVICE_ADDRESS, 0x1B, 0x00)
time.sleep(0.1)
bus.write_byte_data(XG_DEVICE_ADDRESS, 0x1C, 0x00)
time.sleep(0.1)
bus.write_byte_data(XG_DEVICE_ADDRESS, 0x37, 0x22)
time.sleep(0.1)
bus.write_byte_data(M_DEVICE_ADDRESS, 0x0A, 0x06)
time.sleep(0.1)

heading_mag = 0
heading = 0
pitch = 0
roll = 0
prev_time = 0
prev_gz = 0
first_time = True
average_gx = 0
average_gy = 0
average_gz = 0
average_counter = 0
gx_offset = 0
gy_offset = 0
gz_offset = 0
continuous = False

final_gx_offset = 0
final_gy_offset = 0
final_gz_offset = 0


pitch_acc = 0

#Write a single register
while True:
  m_x1 = 0
  m_x2 = 0
  m_y1 = 0
  m_y2 = 0
  m_z1 = 0
  m_z2 = 0
  
  for i in range(NUM_SAMPLES):
    m_x1 += bus.read_byte_data(M_DEVICE_ADDRESS, 0x03)
    bus.read_byte_data(M_DEVICE_ADDRESS, 0x09)
    m_x2 += bus.read_byte_data(M_DEVICE_ADDRESS, 0x04)
    bus.read_byte_data(M_DEVICE_ADDRESS, 0x09)
    m_y1 += bus.read_byte_data(M_DEVICE_ADDRESS, 0x05)
    bus.read_byte_data(M_DEVICE_ADDRESS, 0x09)
    m_y2 += bus.read_byte_data(M_DEVICE_ADDRESS, 0x06)
    bus.read_byte_data(M_DEVICE_ADDRESS, 0x09)
    m_z1 += bus.read_byte_data(M_DEVICE_ADDRESS, 0x07)
    bus.read_byte_data(M_DEVICE_ADDRESS, 0x09)
    m_z2 += bus.read_byte_data(M_DEVICE_ADDRESS, 0x08)
    bus.read_byte_data(M_DEVICE_ADDRESS, 0x09)

    print('{:08b}'.format(m_x1))
    print('{:08b}'.format(m_x2))
    m_x = (m_x2<<8) | m_x1
    print('{:016b}'.format(m_x))
    m_y = (m_y2<<8) | m_y1
    print('{:016b}'.format(m_y))    



  
  #print("M Current: {0:+.3f}, {1:+.3f}, {2:+.3f}".format(m_x, m_x1, m_x2))
  
  a_x1 = 0
  a_x2 = 0
  a_y1 = 0
  a_y2 = 0
  a_z1 = 0
  a_z2 = 0
  
  for i in range(NUM_SAMPLES):
    a_x1 += bus.read_byte_data(XG_DEVICE_ADDRESS, 0x3C) 
    a_x2 += bus.read_byte_data(XG_DEVICE_ADDRESS, 0x3B)
    a_y1 += bus.read_byte_data(XG_DEVICE_ADDRESS, 0x3E)
    a_y2 += bus.read_byte_data(XG_DEVICE_ADDRESS, 0x3D)
    a_z1 += bus.read_byte_data(XG_DEVICE_ADDRESS, 0x40)
    a_z2 += bus.read_byte_data(XG_DEVICE_ADDRESS, 0x3F)
    
    a_x = (a_x2<<8) | a_x1
    print('{:016b}'.format(a_x))
    a_y = (a_y2<<8) | a_y1
    print('{:016b}'.format(a_y))
  
  #print("{0:+.3f}, {1:+.3f}, {2:+.3f}".format(a_x, a_y, a_z))
  

  
  #print("X Current: {0:.3f}, {1:.3f}, {2:.3f}".format(a_x,a_y,a_z))
  
  g_x1 = 0
  g_x2 = 0
  g_y1 = 0
  g_y2 = 0
  g_z1 = 0
  g_z2 = 0
  
  #for i in range(NUM_SAMPLES):
  g_x1 += bus.read_byte_data(XG_DEVICE_ADDRESS, 0x44)
  g_x2 += bus.read_byte_data(XG_DEVICE_ADDRESS, 0x43)
  g_y1 += bus.read_byte_data(XG_DEVICE_ADDRESS, 0x46)
  g_y2 += bus.read_byte_data(XG_DEVICE_ADDRESS, 0x45)
  g_z1 += bus.read_byte_data(XG_DEVICE_ADDRESS, 0x48)
  g_z2 += bus.read_byte_data(XG_DEVICE_ADDRESS, 0x47)
  
  
  enc = (m_x<<48) | (m_y<<32) | (a_x<<16) | a_y
  print('{:064b}'.format(enc))
