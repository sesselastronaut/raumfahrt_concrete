#!/usr/bin/env python
import sys
from serial_com import SerialCom
import time
if __name__ == "__main__" :
	#try:                      # turns on fatal error catching
	sc = SerialCom()
	#SerialCom.bedReferenceTest(sc)
	print("metascript trying to set a bed position")
		
	#SerialCom.bedReferenceTest(sc)
	SerialCom.setBedPosition(sc,116.6)
	
	theta = 116.6
	ctr = 0
	while(1) :
		print("Changing target : ")
		if(theta == 116.6):
			theta = 156.6
		elif(theta == 156.6):
			theta = 116.6
		
	#	while(theta!= sc.checkTarget()):
		sc.setBedPosition(theta)
		
		while(ctr<10):
			
			#sc.setBedReference(223.4)
			sc.setBedPosition(theta)
			time.sleep(1)
			sc.logBedData()
			#sc.resetBedFromLog()
			time.sleep(2)
			ctr = ctr+1
			print("------------------")
		
		ctr = 0	
	#	sc.resetBedFromLog()
		
	#	time.sleep(5);
		
	
	#	sc.resetBedFromLog()
	
	
	#except:
	#	sys.exit(1)           # quit and tell the OS the program closed due to an error

