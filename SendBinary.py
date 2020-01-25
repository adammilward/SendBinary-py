# 26 Aug 2014 - Robin2

# demo program to illustrate sending binary data to an Arduino
# designed to work with ReceiveBinary.ino

# the demo was created to explore sending data to control
#   three stepper motors

# ADAM
# must be ryn with python2 and module 'pyserial'

#=====================================

def sendToArduino(sendStr):
  ser.write(sendStr)

#=====================================

def recvFromArduino():
  global startMarker, endMarker
  
  ck = ""
  x = "z" # any value that is not an end- or startMarker
  byteCount = -1 # to allow for the fact that the last increment will be one too many
  
  # wait for the start character
  while  ord(x) != startMarker: 
    x = ser.read()
    
  # save data until the end marker is found
  while ord(x) != endMarker:
  
    if ord(x) != startMarker:
      ck = ck + x 
      byteCount += 1
      
    x = ser.read()
  
  # print "Bytes received " + str(byteCount + 1)
  return(ck)


#============================

def waitForArduino():

   # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
   # it also ensures that any bytes left over from a previous message are discarded
   
    global startMarker, endMarker # TODO maybe not needed here
    
    msg = ""
    while msg.find("Arduino is ready") == -1:

      while ser.inWaiting() == 0:
        pass
        
      msg = recvFromArduino()

      print (msg)
      print

#======================================

# THE DEMO PROGRAM STARTS HERE

#======================================

import serial
import time
from struct import *

print
print

# NOTE the user must ensure that the serial port and baudrate are correct
serPort = "/dev/ttyACM0"
baudRate = 9600
ser = serial.Serial(serPort, baudRate)
print ("Serial port " + serPort + " opened  Baudrate " + str(baudRate))


startMarker = 60
endMarker = 62


waitForArduino()

print ("Ready sent from Arduino")

# data to send to Arduino
#    unsigned long totalMicros; // 4 bytes
#    int xInterval;              // 2
#    int yInterval;              // 2
#    int zInterval;              // 2
#    byte xorVal;                // 1

totalMicros = 54732
xInterval = 321
yInterval = -654
zInterval = 789
xorVal = 23 # just a fudge, for now

# these need to be made into a string

dataToSend = pack('<LhhhB', totalMicros, xInterval, yInterval, zInterval, xorVal)

# the <Lhhhb  is interpreted as follows
#   see https://docs.python.org/2/library/struct.html
#     <   little-endian
#     L   unsigned long
#     h   signed short
#     B   unsigned char - same as Arduino BYTE

# the following lines of code can be used to explore the packed data
print dataToSend
for character in dataToSend:
  print character.encode('hex')
  
dataBack = unpack('LhhhB', dataToSend)
print dataBack


numLoops =  0
while numLoops < 5:
  retStr = recvFromArduino()
  if retStr == 'M':
    sendToArduino(dataToSend)
    print ("Data Sent" + dataToSend)
  retStr = recvFromArduino()
  print (retStr)
  numLoops += 1


  


