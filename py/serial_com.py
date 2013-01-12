#!/usr/bin/env python
import serial
import time
import datetime as dt


def switch(numZeros):
	return {
	1 : '0',
	2 : '00',
	3 : '000',
	}.get(numZeros,'') 
# read from arduino is mode 1 (sensorTest), 
# write to arduino is mode 2 (rotatingBedTest), 
# read/write to arduino is mode 3 (checkReferenceAngle and currentAngle) 
    

class SerialCom:
	def __init__(self,mode):
		import sys
		self.mode = 3
		self.desiredPos = 0.0
		self.currentPos = 0.0
		self.currentNorthPos = 0.0
		self.theta = 0.0
		try:
			# turns on fatal error catching	
			self.ser = serial.Serial('/dev/ttyUSB0', 9600,timeout=1) # set the correct device name and baudrate
		except:                  
		# do the following if a fatal error was detected
		# please give the user a suitable error message
		# quit and tell the OS the program closed due to an error
			sys.exit(1)           
		#def serialOpen(self):
		#def serialClose(self):
		
	def setMode(self,mode):
		self.mode = mode
		return 'mode set'
	
	def setBedPosition(self,desiredPos):
		#send angle
		self.ser.flushOutput()
		self.desiredPos = desiredPos;
		sentString = str(int(10*self.desiredPos))
		numZeros = 4 - len(sentString)
		sentString = 't' + switch(numZeros) + sentString;
		self.ser.write(sentString)
		time.sleep(1) #pause
		self.ser.flushInput()
		data = self.ser.readline()
		dataCtr = 1
		while data and dataCtr<4:
			#ser.flushOutput()
			#n2=dt.datetime.now()
			#print(data);
			
			#print("Length : "+str(len(data))+",")
			
			if(len(data)==7):
				dataCtr = dataCtr+1
				#print(data)
				print(data[0]+":"+data[1:5])
			
			# Add timestampt to data and write to dat file
			#time.sleep(1) 
			self.ser.flushInput()
			data = self.ser.readline()	
		#read target and store
		#read current and store
		#read reference and store		
		
#	def setBedReference(self,currentNorthPos):
		#send angle
#		self.ser.flushOutput()
#		self.currentNorthPos = currentNorthPos;
#		sentString = str(int(10*self.desiredPos))
#		numZeros = 4 - len(sentString)
#		sentString = 't' + switch(numZeros) + sentString;
#		self.ser.write(sentString)
#	def getBedReference(self):
	def sensorTest(self):
		print "---initiating serialtest---"
			
			#Change path to your local directory if you want
		f = open('./sensorTest.dat','w');
		while 1:		
			#This string initialises the data logging. Presumably you have just reset the arduino before running this python code		
			sentString = "S"
			self.ser.flushOutput()
			self.ser.write(sentString)			
			n1=dt.datetime.now()
			time.sleep(1);
			print "---reading---"
		
			self.ser.flushInput()
			data = self.ser.readline()
			while data:
				#ser.flushOutput()
				n2=dt.datetime.now()
				
				# Add timestampt to data and write to dat file
				f.write(str((n2-n1).microseconds)+","+data)
				print str((n2-n1).microseconds)+","+data
				#time.sleep(1) 
				self.ser.flushInput()
				data = self.ser.readline()	
		
		f.close()
		
	def bedRotationTest(self):
		print("bedReferenceTest")
		while 1:
			# write motor ouputs spontaneously (bed rotation test)
			#ser.write(HEADER) #header byte
			self.ser.flushOutput()
			#ser.write(HEADER) #header byte
			# Padding of zeros in front of the int to make sure there are always 4 digit numbers sent
			# We multiply theta by 10 to ignore difficulties of sending floats
			
			sentString = str(int(10*theta))
			numZeros = 4 - len(sentString)
			sentString = 't' + switch(numZeros) + sentString;

			self.ser.write(sentString)
		
			print "WRITE:"+sentString
			data="1"
			theta = theta + 0.1
			if self.theta > 360.0:
				self.theta = 0.0
			x=x+1
			print "sleep"
			time.sleep(15)    
	
	def bedReferenceTest(self):
		print("bedReferenceTest")
			
		while 1:
			# write rotating motor ouputs spontaneously 
			# (bed rotation test) and read and store the new north reference
			#ser.write(HEADER) #header byte
			self.ser.flushOutput()
			#ser.write(HEADER) #header byte
					# Padding of zeros in front of the int to make sure there are always 4 digit numbers sent
			# We multiply theta by 10 to ignore difficulties of sending floats
			sentString = str(int(10*self.theta))
			numZeros = 4 - len(sentString)
			sentString = 't' + switch(numZeros) + sentString;
			self.ser.write(sentString)
			print "WRITE:"+sentString
			data="1"
			self.theta = self.theta + 0.1
			if self.theta > 360.0:
				self.theta = 340.0
			if self.theta < 340.0:
				self.theta = 340				
			#self.x=self.x+1
			print "sleep"
			time.sleep(15)    
			
	def run(self):
		self.x = 0
		self.theta = 186.5
		
		print "start"
		if self.mode == 2 :
			print("bedRotationTest")
		elif self.mode == 3 :
			print("bedReferenceTest")
		else :
			print("sensorTest")
			
		while 1:
			if self.mode == 2 :
				self.bedRotationTest
			elif self.mode == 3:
				self.bedReferenceTest
			else :
				self.sensorTest


#sc = SerialCom(3)			
#SerialCom.bedReferenceTest(sc)
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
