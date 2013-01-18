import time
while 1:
	try:
		from celestial_body import celestial_body_func
		
		celestial_body_func()		
		time.sleep(1)
	except:
		print("Some gravitational slingshots creating wormholes in celestial body...restarting the big bang")
		
