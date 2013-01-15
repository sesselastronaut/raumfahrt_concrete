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
	def __init__(self):
		import sys
		self.mode = 3
		self.currentTarget = 0.0
		self.currentPos = 0.0
		self.currentReference = 0.0
		self.theta = 0.0
		self.bedStatusFile = './../currentBedStatus'
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
		
	def sendData(self, dataType, data):
		print("---------------")
		self.ser.flushOutput()
		sentString = str(int(10*data))
		numZeros = 4 - len(sentString)
		sentString = dataType + switch(numZeros) + sentString;
		print("Send to Bed")
		print(sentString)
		self.ser.write(sentString)	
		print("---------------")
		
	def receiveData(self):
		self.ser.flushInput()
		data = self.ser.readline()
		dataCtr = 0
		cCtr = 0
		tCtr = 0
		rCtr = 0
		print("---------------")
		print("Read from Bed :")
		while data and dataCtr<3:			
			if(len(data)==7):
				dataCtr = cCtr + tCtr + rCtr#dataCtr+1
				#print(data)
				#print(data[0]+":"+data[1:5])
				value = int(data[1:5])
				value = float(value) / 10
				if("c" in data[0] and cCtr == 0):
					self.currentPos = value 
					cCtr = 1
					print("currentPos : "+str(value))
				elif("t" in data[0] and tCtr == 0):
					self.currentTarget = value
					print("currentTarget : "+str(value))
					tCtr = 1
				elif('r' in data[0] and rCtr == 0):
					self.currentReference =  value
					print("currentReference : "+str(value))
					rCtr = 1
				self.ser.flushInput()
			data = self.ser.readline()	
		print("---------------")

	def setBedPosition(self,desiredPos):
		self.desiredPos = desiredPos
		#send angle
		self.sendData('t',self.desiredPos)
		#time.sleep(1) #pause		#read target and store
		#self.receiveData()
		
	def setBedReference(self,desiredReference):
		self.sendData('r',desiredReference)
		#time.sleep(1)
		self.currentReference = desiredReference

	def logBedData(self):
		self.receiveData()
		f = open(self.bedStatusFile,'w')
		n1 = dt.datetime.now()
				
		currentPos = str(int(10*self.currentPos))
		numZeros = 4 - len(currentPos)
		currentPos = switch(numZeros) + currentPos;

		currentTarget = str(int(10*self.currentTarget))
		numZeros = 4 - len(currentTarget)
		currentTarget = switch(numZeros) + currentTarget;
		
		currentReference = str(int(10*self.currentReference))
		numZeros = 4 - len(currentReference)
		currentReference = switch(numZeros) + currentReference;
		
		towrite  = str(n1.time()) + " : " +"c:"+currentPos+","+"t:"+ currentTarget +","+"r:"+ currentReference
		f.write(towrite)
		print("writeToLogfile :");
		print(towrite)		
		f.close()
		
	def resetBedFromLog(self):
		f = open(self.bedStatusFile,'r')
		#f.write("c:"+str(self.currentPos)+","+"t:"+str(self.currentTarget)+","+"r:"+str(self.currentReference))
		data = f.read()
		#print(data)
		self.setBedPosition(float(data[27:31])/10)
		self.setBedReference(float(data[34:38])/10)
		
		
		#print("setting position" + (float(data[27:31])/10)+"setting reference" +(float(data[34:38]/10)))
		f.close()

	def sensorTest(self):
		print "---initiating serialtest---"
			
		#Change path to your local directory if you want
		f = open('./sensorTest.dat','w')
				
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
		#while 1:
		# write motor ouputs spontaneously (bed rotation test)
			
		self.sendData('r',self.theta)	
		theta = theta + 0.1
		if self.theta > 360.0:
			self.theta = 0.0
		self.x=self.x+1
		print "sleep"
		time.sleep(15)    
	
	def bedReferenceTest(self):
		#print("bedReferenceTest")
			
		#while 1:
		# write rotating motor ouputs spontaneously 
		# (bed rotation test) and read and store the new north reference
		#ser.write(HEADER) #header byte
		self.ser.flushOutput()
		#ser.write(HEADER) #header byte
				# Padding of zeros in front of the int to make sure there are always 4 digit numbers sent
		# We multiply theta by 10 to ignore difficulties of sending floats
		self.sendData('r',self.theta)
		
		self.theta = self.theta + 0.1
		if self.theta > 360.0:
			self.theta = 340.0
		if self.theta < 340.0:
			self.theta = 340				
		#self.x=self.x+1
		print "sleep"
		time.sleep(15)    
			
	def run(self,mode):
		self.x = 0
		self.theta = 186.5
		self.mode = mode
		
		print "start"
		if self.mode == 2 :
			print("bedRotationTest")
		elif self.mode == 3 :
			print("bedReferenceTest")
		else :
			print("sensorTest")
			
		while 1:
			if self.mode == 2 :
				self.bedRotationTest()
			elif self.mode == 3:
				self.bedReferenceTest()
			else :
				self.sensorTest()

