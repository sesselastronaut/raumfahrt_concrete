#!/usr/bin/env python
import serial
import time
import datetime as dt
import sys
import os
from serial.tools import list_ports


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
		self.portName = 0
		self.connectionStatus = 0
		try:
			# turns on fatal error catching	
			print("Opening Serial Com")
			print("checking: " + "/dev/ttyUSB"+str(self.portName))
			self.ser = serial.Serial('/dev/ttyUSB'+str(self.portName), 9600,timeout=1) # set the correct device name and baudrate
			print("Connection success!")
			self.connectionStatus = 1
			#self.portName = 1
		except:                  
		# do the following if a fatal error was detected
		# please give the user a suitable error message
		# quit and tell the OS the program closed due to an error
			self.connectionStatus = 0 
		#	if(self.portName == 4) :
		#		self.portName  = 0
		#	else:
		#		self.portName = self.portName+1
			
			while self.portName<=4 :
				try:
					print("Connection Error..trying another port");
					#print([port[0] for port in list_ports.comports()])
				
					#import serial.tools.list_ports
					#serial.tools.list_ports.comports()#list(serial.tools.list_ports.comports())
					print("checking: " + "/dev/ttyUSB"+str(self.portName))
					self.ser = serial.Serial('/dev/ttyUSB'+str(self.portName), 9600,timeout=1) # set the correct device name and baudrate
					print("Connection success!")
					self.connectionStatus = 1
					break
				except:
					self.connectionStatus = 0
					print("Checking other Serial Connections")
					self.portName = self.portName+1
			
			if self.portName == 4:
				print("SerialCom error please check..shutting SerialCom down now")
				sys.exit(1)           
		
	def serialReconnect(self):
		print("Trying to Reconnect");
		while self.portName<4 :
			try:
				# turns on fatal error catching	
				#self.ser = serial.Serial('/dev/ttyUSB0', 9600,timeout=1) # set the correct device name and baudrate
				print("checking: " + "/dev/ttyUSB"+str(self.portName))
				self.ser = serial.Serial('/dev/ttyUSB'+str(self.portName), 9600,timeout=1)			
				self.connectionStatus = 1
				print("Connection success!")
				
				try:
					self.resetBedFromLog()
				except:
					print("Reset BedError")
				break
			except:                  
				self.connectionStatus = 0
				self.portName = self.portName+1
				
				# do the following if a fatal error was detected
				# please give the user a suitable error message
				# quit and tell the OS the program closed due to an error
				print("..Reconnection Error..");
				#print([port[0] for port in list_ports.comports()])
		self.portName = 0
		
				#sys.exit(1) 
		
	def sendData(self, dataType, data):
		print("---------------")
		try:
			self.ser.flushOutput()
			sentString = str(int(10*data))
			numZeros = 4 - len(sentString)
			sentString = dataType + switch(numZeros) + sentString;
			print("Send to Bed")
			print(sentString)
			self.ser.write(sentString)	
			self.ser.flushOutput()
			print("---------------")
		except:
			print("Communication Error..ReConnecting..")
			#time.sleep(2) 
			self.serialReconnect()
			
	def receiveData(self):
		print("---------------")
		print("Read from Bed :")
		try:
			self.ser.flushInput()
			data = self.ser.readline()
			dataCtr = 0
			cCtr = 0
			tCtr = 0
			rCtr = 0
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
		except:
			print("Communication Error..ReConnecting..")
			time.sleep(2) 
			self.serialReconnect()
			
	'''		
	def checkTarget(self):
		print("---------------")
		print("Checking Target in bed :")
		returnValue = 0
		#try:
		self.ser.flushInput()
		data = self.ser.readline()
		tCtr = 0
		while data and tCtr==0:			
			if(len(data)==7):
				#dataCtr = cCtr + tCtr + rCtr#dataCtr+1
				print(data)
				#print(data[0]+":"+data[1:5])
				value = int(data[1:5])
				value = float(value) / 10
				
				if('t' in data[0] and tCtr == 0):
					returnValue =  value
					print("currentTarget : "+str(value))
					tCtr = 1
					break
				self.ser.flushInput()
			data = self.ser.readline()	
		print("---------------")
		return returnValue
		#except:
		#	print("Communication Error..ReConnecting..")
	#		time.sleep(2) 
		#	self.serialReconnect()

	def checkReference(self):
		print("---------------")
		print("Checking Reference in bed :")
		returnValue = 0
		#try:
		self.ser.flushInput()
		data = self.ser.readline()
		rCtr = 0
		while data and rCtr==0:			
			if(len(data)==7):
				#dataCtr = cCtr + tCtr + rCtr#dataCtr+1
					#print(data)
				#print(data[0]+":"+data[1:5])
				value = int(data[1:5])
				value = float(value) / 10
				
				if('r' in data[0] and rCtr == 0):
					returnValue =  value
					print("currentReference : "+str(value))
					rCtr = 1
					break
				self.ser.flushInput()
			data = self.ser.readline()	
		print("---------------")
		return returnValue
		#except:
		#	print("Communication Error..ReConnecting..")
	#		time.sleep(2) 
		#	self.serialReconnect()
	'''
						
	def setBedPosition(self,desiredPos):
		self.desiredPos = desiredPos
		#send angle
		self.sendData('t',self.desiredPos)
	#	self.checkTarget()
		#time.sleep(1) #pause		#read target and store
		#self.receiveData()
		
	def setBedReference(self,desiredReference):
		self.sendData('r',desiredReference)
		#time.sleep(1)
		self.currentReference = desiredReference
	#	self.checkReference()

	def logBedData(self):
		self.receiveData()
		f = open(self.bedStatusFile,'a')
		n1 = dt.datetime.now()
				
		currentPos = str(int(self.currentPos))
		numZeros = 3 - len(currentPos)
		currentPos = switch(numZeros) + str(self.currentPos);

		currentTarget = str(int(self.currentTarget))
		numZeros = 3 - len(currentTarget)
		currentTarget = switch(numZeros) + str(self.currentTarget);
		
		currentReference = str(int(self.currentReference))
		numZeros = 3 - len(currentReference)
		currentReference = switch(numZeros) + str(self.currentReference);
		if(self.connectionStatus != 0):
			towrite  = "\n"+str(n1.time()) + " :" +"c: "+ currentPos+" | "+"t: "+ currentTarget +" | "+"r: "+ currentReference
		else:
			towrite  = "\n"+str(n1.time()) + " :" +"c: "+currentPos+" | "+"t: "+ currentTarget+" | "+"r: "+ currentReference + " | COM LOST!"
		f.write(towrite)
		print("writeToLogfile :");
		print(towrite)		
		
		#print("RESETBEDFROMLOG :" + str(float(towrite[31:36])) + "," + str(float(towrite[42:47])))
		f.close()
		
	def resetBedFromLog(self):
		f = open(self.bedStatusFile,'r+')
		
		#st_results = os.stat(self.bedStatusFile)
		#st_size = st_results[6]
		#print st_size
		#f.seek(st_size)
		dataList = f.readlines()
		data = dataList[len(dataList)-1]

		f.close()

		#data = file(self.bedStatusFile, "r").readlines()[-1]
		
		#print("RESET:"+data[len(data)-1])
		
		print("RESETBEDFROMLOG : " + str(float(data[31:36])) + "," + str(float(data[42:47])))#data[37:41] + "," + data[52:56])
		#str(float(data[27:31]) + " , " + str(float(data[34:38])))) 
		
		bedref = float(data[42:47])
		self.setBedReference(bedref)
		'''
		while(self.checkReference() != bedref):
			print("trying to reset reference aaaaaaaaaaaaaaaaaah")
			self.setBedReference(bedref)
			time.sleep(1)
		'''
		bedpos = float(data[31:36])	
		self.setBedPosition(bedpos)
		'''
		while(self.checkTarget != bedpos):
			print("trying to reset target aaaaaaaaaaaaaaaaaah")
			self.setBedPosition(bedpos)
			time.sleep(1)
		'''
		
		#print("setting position" + (float(data[27:31])/10)+"setting reference" +(float(data[34:38]/10)))
		
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

