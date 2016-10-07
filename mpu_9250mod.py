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

def twos_comp(val, bits):
  """compute the 2's compliment of int value val"""
  if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
      val = val - (1 << bits)        # compute negative value
  return val                         # return positive value as is s
  
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
#bus.write_byte_data(XG_DEVICE_ADDRESS, 0x37, 0x02)
bus.write_byte_data(XG_DEVICE_ADDRESS, 0x37, 0x22)
time.sleep(0.1)
#bus.write_byte_data(M_DEVICE_ADDRESS, 0x0A, 0x01)
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

    
  m_x1 /= NUM_SAMPLES
  m_x2 /= NUM_SAMPLES
  m_y1 /= NUM_SAMPLES
  m_y2 /= NUM_SAMPLES
  m_z1 /= NUM_SAMPLES
  m_z2 /= NUM_SAMPLES
  
  m_x = m_x1 + (m_x2*256)
  m_y = m_y1 + (m_y2*256)
  m_z = m_z1 + (m_z2*256)
  
  m_x = m_x1 + (m_x2*256)
  m_x = twos_comp(m_x, 16) / float(32768) * 2
  m_y = m_y1 + (m_y2*256)
  m_y = twos_comp(m_y, 16) / float(32768) * 2
  m_z = m_z1 + (m_z2*256)
  m_z = twos_comp(m_z, 16) / float(32768) * 2
  
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
    
  a_x1 /= NUM_SAMPLES
  a_x2 /= NUM_SAMPLES
  a_y1 /= NUM_SAMPLES
  a_y2 /= NUM_SAMPLES
  a_z1 /= NUM_SAMPLES
  a_z2 /= NUM_SAMPLES
  
  a_x = a_x1 + (a_x2*256)
  a_x = twos_comp(a_x, 16) / float(32768) * 2
  a_y = a_y1 + (a_y2*256)
  a_y = twos_comp(a_y, 16) / float(32768) * 2
  a_z = a_z1 + (a_z2*256)
  a_z = twos_comp(a_z, 16) / float(32768) * 2
  
  #print("{0:+.3f}, {1:+.3f}, {2:+.3f}".format(a_x, a_y, a_z))
  
  if abs(a_x) < 0.3:
    a_x = 0
  if abs(a_y) < 0.3:
    a_y = 0
  if abs(a_z) < 0.3:
    a_z = 0
  else:
    a_z += 0.07    
       
  
  #total_a = math.sqrt(a_x*a_x + a_y*a_y * a_z*a_z)
 # a_x /= total_a
  #a_y /= total_a
  #a_z /= total_a
  
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
    
 # g_x1 /= NUM_SAMPLES
  #g_x2 /= NUM_SAMPLES
  #g_y1 /= NUM_SAMPLES
  #g_y2 /= NUM_SAMPLES
  #g_z1 /= NUM_SAMPLES
 # g_z2 /= NUM_SAMPLES
 
  g_x = g_x1 + (g_x2*256)
  g_x = twos_comp(g_x, 16) / float(32768) * 245 - final_gx_offset
  g_y = g_y1 + (g_y2*256)
  g_y = twos_comp(g_y, 16) / float(32768) * 245 - final_gy_offset
  g_z = g_z1 + (g_z2*256)
  g_z = twos_comp(g_z, 16) / float(32768) * 245 - final_gz_offset
 
  #if average_counter < 1000:
  average_counter += 1
  average_gz = (average_gz*(average_counter-1) + g_z) / average_counter
  average_gx = (average_gx*(average_counter-1) + g_x) / average_counter
  average_gy = (average_gy*(average_counter-1) + g_y) / average_counter
  if average_counter == 500:
    final_gx_offset = average_gx
    final_gy_offset = average_gy
    final_gz_offset = average_gz
    heading = 0
    pitch = 0
    roll = 0
    heading_mag = 0
  
  #  print(average_counter)
 # else:
  if first_time:
    prev_time = time.clock()
    prev_gz = g_z
    prev_gy = g_y
    prev_gx = g_x
    first_time = False
  else:
    if abs(g_x) > 0.5:    
        pitch += (prev_gx + g_x)*(0.5)*(time.clock() - prev_time)*22.5
    if abs(g_y) > 0.5: 
        roll += (prev_gy + g_y)*(0.5)*(time.clock() - prev_time)*22.5
       
    heading_mag = math.atan2(m_y, m_x)*180.0/math.pi
    if heading_mag < 0:
      heading_mag += 360.0
        
    if math.sqrt(abs(a_x) + abs(a_y) + abs(a_z)) > 1.0 and math.sqrt(abs(a_x) + abs(a_y) + abs(a_z)) < 2.0:
      pitch_acc = math.atan2(a_y, a_z)
      roll_acc = math.atan2(a_x, a_z)
      pitch = pitch*0.95 + pitch_acc*180.0/math.pi*0.05
      roll = roll*0.95 + (-1)*roll_acc*180.0/math.pi*0.05        
 
    prev_time = time.clock()
    prev_gz = g_z
    prev_gx = g_x
    prev_gy = g_y
  
    print("X Current: {0:+.3f}, {1:+.3f}, {2:+.3f} G Current: {3:+.3f}, {4:+.3f}, {5:+.3f} M Current: {6:+.3f}, {7:+.3f}, {8:+.3f} Pitch: {9:+.1f}  Roll: {10:+.1f}  Heading_Mag: {11:+.1f}".format(a_x, a_y, a_z, g_x, g_y, g_z, m_x, m_y, m_z, pitch, roll, heading_mag))
  #conn.send("{0:+.1f},{1:+.1f},{2:+.1f}|".format(pitch, roll, heading))
  

   # if math.sqrt(abs(a_x) + abs(a_y) + abs(a_z)) > 1.0 and math.sqrt(abs(a_x) + abs(a_y) + abs(a_z)) < 2:
       #   adjustment = math.atan2(a_y, a_x)
       #   if adjustment > 0:
       #     rotation = rotation*0.98 + (math.pi-abs(adjustment))*180.0/math.pi*0.02
        #  else:
        #    rotation = rotation*0.98 + (-1.0)*(math.pi+abs(adjustment))*180.0/math.pi*0.02
  
