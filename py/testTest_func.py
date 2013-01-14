#!/usr/bin/env python
from test_func import TestClass
import sys

if __name__ == "__main__" :
	try:                      # turns on fatal error catching
		tc = TestClass(5)
		#TestClass.myfunction(tc)
		tc.myfunction()
		
		tc.setData(10)
		temp = TestClass.getData(tc)
		print temp
		
		a = "4.556563"
		
	#	print(a)
		print(int(float(a)))
	#	print(float(a))
		
	except:
		print("Die Die Die")
		sys.exit(1)           # quit and tell the OS the program closed due to an error
