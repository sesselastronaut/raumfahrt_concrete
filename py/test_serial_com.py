#!/usr/bin/env python
import sys
from serial_com import SerialCom

if __name__ == "__main__" :
	#try:                      # turns on fatal error catching
	sc = SerialCom(2)
	#SerialCom.bedReferenceTest(sc)
	print("Running the run function")
		
	#SerialCom.bedReferenceTest(sc)
	SerialCom.setBedPosition(sc,116.6)
	#except:
	#	sys.exit(1)           # quit and tell the OS the program closed due to an error

