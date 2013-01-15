#!/usr/bin/env python
import sys

class TestClass:
	def __init__(self,data):
		self.data = data
	
	def setData(self,data):
		self.data  = data
		self.myfunction()
	
	def myfunction(self):
		print "mProgram ran with" + str(int(self.data))
		
	def getData(self):
		return self.data;
		
   
   # try:
	#	tc = TestClass(10)
#		tc.myfunction()
        #myfunction(10)
 #   except:
  #      sys.exit(1) 
