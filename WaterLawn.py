#!/usr/bin/env python
#LIBRARIES
import sys
import os

import smbus
import time
import numpy as np
import board
import busio
from datetime import date
from datetime import datetime
import signal
import yagmail
import json
import requests

#Email info
g_email = 'xxxxxxxxxx' #Gmail account.
y_email = 'xxxxxxxxxx' #Yahoo account.
password='xxxxxxxxx' #Password for Gmail account - protected for privacy.


body = json.dumps({

 "notification": "Unusually High Flowrate detected, irrigation stopped",

 "accessCode": "xxxxxxxxxxxxxxxxxxxx"

})

number1 = 'xxxxxxxxxx' #Text numbers.
number2 = 'xxxxxxxxxx' #Text numbers.
yag = yagmail.SMTP(g_email, password)


#CONSTANTS
decadeCounter = [29, 4, 30, 22, 7, 19, 27, 20, 31, 23] #1 5 2 7 6 - unique 5 digit binary code for each digit.
bv_MAXTIME=15; #Maximum amount of time to wait for ball valve to open/close.
bv_initOpen = 0b01000000; #State of BallValveMCP GPA pins when valve is open and not being opened.
bv_open = 0b01000011; #State of BallValveMCP GPA pins when valve is open and being opened.
bv_initClosed = 0b10000000; #State of BallValveMCP GPA pins when valve is closed and not being closed.
bv_closed = 0b10000101; #State of BallValveMCP GPA pins when valve is closed and being closed.
bus = smbus.SMBus(1) 
BallValveMCP = 0x20 # Controls the ball valve and the transformer.
RelayBoardMCP= 0x21 # MCP chip that controls the relays that opens and closes the solenoids for each irrigation zone.
TempSensor=0x77 #Temperature/pressure sensor
FlowMeterMCP=0x23 #Decade counter MCP chip that counts the number of gallons that are used in irrigation.
IODIRA = 0x00 # Pin direction register
OLATA  = 0x14 # Register for outputs
GPIOA  = 0x12 # Register for inputs
IODIRB = 0x01 # Pin direction register
OLATB  = 0x15 # Register for outputs
GPIOB  = 0x13 # Register for inputs
zoneArea=[0, 551, 2447, 1737, 2496, 3787, 957] #Area, in square feet, of each irrigation zone. Calculated by field measurements and using the Johnson County Assessor mapping tool. zoneArea[i] stores the area of zone i.
flowRate=[0, 5.065, 4.5575, 8.0, 4.66, 4.71, 8.2] #Flow rate, in seconds per gallon, of each irrigation zone. Measured by connecting the flow meter output to an oscilloscope for each zone. These flow rates have not changed over time, and a significant change in them indicates a broken pipe.

bus.write_byte_data(BallValveMCP,IODIRA,0b11000000) 
bus.write_byte_data(FlowMeterMCP,IODIRB,0b11111000)
bus.write_byte_data(FlowMeterMCP,IODIRA,0b11111000)
bus.write_byte_data(RelayBoardMCP, IODIRA, 0b00000000)
bus.write_byte_data(RelayBoardMCP, IODIRB, 0b00000000)

bus.write_byte_data(BallValveMCP,OLATA,0)
bus.write_byte_data(FlowMeterMCP,OLATA,0)
bus.write_byte_data(FlowMeterMCP,OLATB,0)
bus.write_byte_data(RelayBoardMCP,OLATA,0)
bus.write_byte_data(RelayBoardMCP,OLATB,0)


#FUNCTIONS
def signal_handler(sig, frame): #Turns off the relays when the program is keyboard quit.
    print('\n You quit the program, turning relays off\n') 
    bus.write_byte_data(RelayBoardMCP,OLATA,0)
    bus.write_byte_data(RelayBoardMCP,OLATB,0)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def rewriteFile(): #Remove zones/lines already run from IrrigationSchedule.txt.
    with open("xxxxxxxx/waterpai/IrrigationSchedule.txt", "r") as my_file: #Delete first #zones run -1 lines.
        lines = my_file.readlines()
    for i in range(0, zonesRun):
        del lines[0]
    with open("xxxxxxxx/waterpai/IrrigationSchedule.txt", "w") as my_file:
        for line in lines:
            my_file.write(line)
    print("Rewrote file\n")
            
def restartProgram(): #Re-runs this program.
    print("Restarting program\n")
    with open("xxxxxxxxx/waterpai/restartcount.txt", "r") as my_file: #program cannot restart more than 10 times
        lines = my_file.readlines()
    cur=int(lines[0])                   #cur is the number of times the program has already restarted
    if(cur>9): #Quit program
        bus.write_byte_data(RelayBoardMCP,OLATA,0)
        bus.write_byte_data(RelayBoardMCP,OLATB,0)
        sys.exit(0)
    with open("xxxxxxxxx/waterpai/restartcount.txt", "w") as my_file: #program cannot restart more than 10 times
        my_file.write(str(cur+1))
    os.execv(sys.executable, ['python'] + sys.argv)

def onTransformer(): #Turns on the transformer by controlling relay. 
    bus.write_byte_data(BallValveMCP, OLATB, 2) #GPB0 is for the Internet, GPB1 is the transformer for the ball valve.
    print("Transformer on")
    time.sleep(2)

def offTransformer(): #Turns off the transformer by controlling relay. 
    bus.write_byte_data(BallValveMCP, OLATB, 0)
    print("Transformer off")
    time.sleep(2)

def openBallValve(): #Opens the ball valve.
   input = bus.read_byte_data(BallValveMCP,GPIOA)
   if not(input == bv_initOpen or input == bv_open): #Check if ball valve is not fully open.
      print ("Opening")
      time.sleep(1)
      bus.write_byte_data(BallValveMCP,OLATA,3) #011 - 1,2 Enable HIGH, 1A HIGH, 2A LOW on H-driver.
   counter=0;
   while bus.read_byte_data(BallValveMCP,GPIOA)!=bv_open and counter<10*bv_MAXTIME:
      time.sleep(.1)
      counter += 1;
   input = bus.read_byte_data(BallValveMCP,GPIOA)
   if input==bv_open:
      print("Opened successfully")
   else:
      print("Open unsuccessful")
   else:
     print("Valve open")
   bus.write_byte_data(BallValveMCP,OLATA,0) #000 - Turn all BallValveMCP outputs to LOW.

def closeBallValve(): #Closes the ball valve.
   input = bus.read_byte_data(BallValveMCP,GPIOA)
   if not(input == bv_initClosed or input == bv_closed): #Check if ball valve is not fully closed.
      print ("Closing")
      time.sleep(1)
      bus.write_byte_data(BallValveMCP,OLATA,5) #101 - 1,2 Enable HIGH, 1A LOW, 2A HIGH on H-driver.
   counter=0;
   while bus.read_byte_data(BallValveMCP,GPIOA)!=bv_closed and counter<10*bv_MAXTIME:
      time.sleep(.1)
      counter=counter+1;
   input = bus.read_byte_data(BallValveMCP,GPIOA)
   if input==bv_closed:
      print("Closed successfully")
   else:
      print("Close unsuccessful")
   else:
      print("Valve closed")
   bus.write_byte_data(BallValveMCP,OLATA,0) #000 - Turn all BallValveMCP outputs to LOW.

def startZone(zone, t): #Irrigates the specified zone (which can range from 1 to 6) for t seconds.
   if(zone==0):
       sleep(t)
   else:
       pin = zone-1
       resetCounter()
       onTransformer()
       time.sleep(5)
       openBallValve()
       print("Zone: " + str(zone) + "  Time: " + str(t) + "\n")
       print(datetime.now().isoformat())
       print("\n")
       bus.write_byte_data(RelayBoardMCP,OLATB, 2) #Turning on relay 8 activates the power to the other relays. Moreover, relays 1-6 are only powered if relay 8 is powered and relay 7 is not powered. This is a preventative measure.
       bus.write_byte_data(RelayBoardMCP, OLATA, np.power(2, pin)) #Turning on the zone-th relay.
       if(t>=20): #If no water flows in the first 20 seconds since opening the ball valve and solenoid plunger, that means we need to restart the program.
           time.sleep(20)
           if (getCounterValue() == 0):
               print("No gallons flowed\n") #No flow was detected  by the flow meter.
               bus.write_byte_data(RelayBoardMCP, OLATA, 0) #Turn off relays.
               print("Relays turned off\n")
               rewriteFile() 
               restartProgram() #Re-run the program. 
           else:
               print("Gallons flowing\n") #Flow meter detected flow.
               #time.sleep(t-20)
               sec_counter = 0
               gallon_counter = 0
               interval=300 #We want to reset the counter every interval seconds because the decade counter only counts up to 99. 
               while(sec_counter + interval < t - 20): #Runs the irrigation for t-20 seconds (not t because we used 20 of the t seconds to check the flow meter).
                  time.sleep(interval)
                  gallon_counter += getCounterValue() #After interval seconds, update gallon_counter and reset the gallon counter.
                  if(gallon_counter>1.5*interval/flowrate[i]): #Check if flowrate is too high; if so, send email and quit
                     requests.post(url = "xxxxxxxxxxxxx", data = body)
                     yag.send(to = number1, subject = 'POSSIBLE LEAK', contents = 'Unusually High Flowrate in zone '+str(zone))
                     yag.send(to = number2, subject = 'POSSIBLE LEAK', contents = 'Unusually High Flowrate in zone '+str(zone))
                     yag.send(to = y_email, subject = 'POSSIBLE LEAK', contents = 'Unusually High Flowrate in zone '+str(zone))
                     sys.exit(0)
                  if(gallon_counter<interval/flowrate[i]/2):#Check if flowrate is too low; if so, send email and quit
                     yag.send(to = y_email, subject = 'Unusually low flowrate', contents = 'Unusually low flowrate in zone '+str(zone))
                     sys.exit(0)
                  resetCounter() 
                  sec_counter += interval
              time.sleep(t - 20 - sec_counter) 
              gallon_counter += getCounterValue() #Update gallon_counter for the remainder of the irrigation time.
              resetCounter()
       else: #Irrigation time is < 20 seconds.
           time.sleep(t)
       
       bus.write_byte_data(RelayBoardMCP,OLATA,0) #Turn off all relays once time is up
       bus.write_byte_data(RelayBoardMCP,OLATB, 0)
       print("Zone "+str(zone)+"  end \n") #Watering has ended for this zone
       closeBallValve() #Opening and closing the ball valve after each zone ensures a constant flow rate.
       time.sleep(5)
       offTransformer() 
       time.sleep(5)

def getCounterValue(): #Reads the decade counter that counts the number of gallons of water that have passed through the flow meter.
   input_ones = bus.read_byte_data(FlowMeterMCP,GPIOB)
   input_tens = bus.read_byte_data(FlowMeterMCP,GPIOA)
   tens=np.floor(input_tens/0b1000)
   ones=np.floor(input_ones/0b1000)
   value=10*getDigit(tens)+getDigit(ones)
   return(value)

def resetCounter(): #Resets the decade counter.
   bus.write_byte_data(FlowMeterMCP,OLATB,0b00000001)
   time.sleep(1)
   bus.write_byte_data(FlowMeterMCP,OLATB,0b00000000)

def getDigit(output): #Gets the output from a single decade counter.
   for i in range(0, 10):
      if(decadeCounter[i]==output):
         return i

def writeOriginalFile(): 
    original=["2 695\n", "3 866\n", "1 348\n", "4 1450\n", "5 2224\n", "6 978\n", "2 695\n", "3 866"] #These are the times we need for watering .2 inches to each zone, which are calculated by the formula flowRate[i]*.2*zoneArea[i]*7.48052/12
    with open("xxxxxxxxxxxx/waterpai/IrrigationSchedule.txt", "w") as my_file:
        for line in original:
            my_file.write(line)
    with open("xxxxxxxxxxxx/waterpai/restartcount.txt", "w") as my_file: #program cannot restart more than 10 times
        my_file.write("0")
      
     
#TESTING
try:        
    zonesRun=0
    with open("xxxxxxxxxxxx/waterpai/IrrigationSchedule.txt", "r") as my_file:
        for line in my_file:
            s = line.split()
            if(len(s)>=0):
                zone=int(s[0])
                runtime=int(s[1])
                #print(str(zone)+"-"+str(runtime));
                startZone(zone,runtime)
                zonesRun=zonesRun+1
    
    bus.write_byte_data(RelayBoardMCP,OLATA,0)
    writeOriginalFile()
except:
    print("\nThere was an error\n")
    bus.write_byte_data(RelayBoardMCP, OLATA, 0)
closeBallValve()
    
 
# Set all bits to zero
bus.write_byte_data(BallValveMCP,OLATA,0)
#f.close()


