#!/usr/bin/env python
import serial
import time
import sys
import datetime as dt

mode = 1 # read from arduino is mode 1, write to arduino is mode 2
 
def switch(numZeros):
	return {
	1 : '0',
	2 : '00',
	3 : '000',
	}.get(numZeros,'') 

def myprogram():
    # put some code here which either ends nicely or crashes the program
    # if you put a sys.exit() call here, don't forget to first close the input: ser.close(),
    # otherwise you probably can't restart the script successfully without detaching and 
    # reattaching the Arduino
	x = 0
	theta = 186.5
	
	print "start"
	while 1:
		if mode == 2 :
			# write motor ouputs spontaneously (bed rotation test)
			#ser.write(HEADER) #header byte
			ser.flushOutput()
			#ser.write(HEADER) #header byte
		
			# Padding of zeros in front of the int to make sure there are always 4 digit numbers sent
			# We multiply theta by 10 to ignore difficulties of sending floats
		
			sentString = str(int(10*theta))
			numZeros = 4 - len(sentString)
			sentString = 'g' + switch(numZeros) + sentString;

			ser.write(sentString)
		
			print "WRITE:"+sentString
			data="1"
			theta = theta + 0.1
			if theta > 360.0:
				theta = 0.0
			x=x+1
			print "sleep"
			time.sleep(15)    

		
		else :
			print "---initiating serialtest---"
			
			#Change path to your local directory if you want
			f = open('./data/sensor/sensorTest-4-5V-CW_rotation.dat','w');
					
			#This string initialises the data logging. Presumably you have just reset the arduino before running this python code		
			sentString = "S"
			ser.flushOutput()
			ser.write(sentString)			
			n1=dt.datetime.now()

			time.sleep(1);
			print "---reading---"
			
			ser.flushInput()
			data = ser.readline()
			while data:
				#ser.flushOutput()
				n2=dt.datetime.now()
			
				# Add timestampt to data and write to dat file
				f.write(str((n2-n1).microseconds)+","+data)
				print str((n2-n1).microseconds)+","+data
				#time.sleep(1) 
				ser.flushInput()
				data = ser.readline()	
			f.close()
if __name__ == "__main__" :
    try:                      # turns on fatal error catching
        ser = serial.Serial('/dev/ttyUSB0', 9600,timeout=1) # set the correct device name and baudrate
    except:                   # do the following if a fatal error was detected
							# please give the user a suitable error message
        sys.exit(1)           # quit and tell the OS the program closed due to an error
    # Reset the Arduino to make sure it's working properly
    #ser.setDTR( level=False ) # set the reset signal
    #time.sleep(2)             # wait two seconds, an Arduino needs some time to really reset
                              # don't do anything here which might overwrite the Arduino's program
    #ser.setDTR( level=True )  # remove the reset signal, the Arduino will restart
    try:
        myprogram()
    except:
        ser.close()
        raise                 # show any traceback messages and quit
    ser.close()               # make sure to always close the serial connection


"""
try:
	ser = serial.Serial('/dev/ttyUSB0', 9600) # set the correct device name and baudrate
except:
	sys.exit(1)
"""
"""
x = 0
ser = serial.Serial('/dev/ttyUSB1', 9600,timeout=1) # set the correct device name and baudrate	

while 1:
	#ser.write(HEADER) #header byte
	

	ser.write(str(x))
	#ser.write(HEADER) #header byte
	print "WRITE: "+str(x)
	data="1"
	while data:
		print "-------reading"
		data = ser.readline()
		ser.flushInput()
		#ser.flushOutput()
		print data
		print "------------end"
	

	x=x+1
	print "sleep"
	time.sleep(1)
ser.close()	
"""

