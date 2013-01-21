#!/usr/bin/python
from serial_com import SerialCom
import sys
import time

if __name__ == "__main__" :
	print 'Number of arguments:', len(sys.argv), 'arguments.'
	print 'Argument' , str(sys.argv[1])
	desPos = sys.argv[1]
	sc = SerialCom()

	while(1):
		print desPos
		sc.setBedPosition(float(desPos))
		time.sleep(1)
		sc.logBedData()
		print("----------------")	
		time.sleep(1)
