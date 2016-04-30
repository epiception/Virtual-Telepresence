import serial
import time 
import glob
import logging
########### Variable declaration
global device_id 
global device_type 
global function_type 
global param_count
global port
#global wl_threshold
wl_threshold = 20
sharp_threshold = 100
ir_threshold = 95
left_sensor_value = 0
centre_sensor_value = 0
right_sensor_value = 0 
front_sharp_value = 0
front_ir_value = 0

port_detect = glob.glob("/dev/ttyUSB*") # stores all /dev/ttyUSB* into a list port_detect

def serial_port_connection():
	global port 
	
	print len(port_detect),"Ports detected" # print number of ports detected
	
	#------------- print all detectec ports - STARTS ---------#
	if (len(port_detect) != 0):				
		print "Port(s) detected is/are:"	
		
		for i in range (0,len(port_detect)):
			print port_detect[i]
	#------------- print all detectec ports - END ---------#
	
	#------------- connect to PORT if only one port is detected - STARTS ---------#
		if (len(port_detect) == 1):
			port = serial.Serial(port_detect[0],baudrate=9600)
			print "connected to: ", port_detect[0]
	#------------- connect to PORT if only one port is detected - END ---------#	
	
	#------------- Ask for user i/p if more then one port is detected - STARTS ---------#
		else:
			for i in range(0,len(port_detect)):
				print "Enter",i,"to connect to:",port_detect[i]
			
			y = int(raw_input("Enter your choice of connection: "))
			
			while y >= len(port_detect):
				print "Invalid choice"
				for i in range(0,len(port_detect)):
					print "Enter",i,"to connect to:",port_detect[i]
				y = int(raw_input("Enter your choice of connection: "))
	#------------- Ask for user i/p if more then one port is detected - END ---------#			
			
			port = serial.Serial(port_detect[y],baudrate=9600)
			print "connected to: ", port_detect[y]
		return
      
try:
	serial_port_connection()
			
	if port.isOpen() == True:
		print "Port is open"
	else:
		serial_port_connection()
			
except:
	print "No USB port detected....check connection"
	sys.exit(0)		# stop program execution when exception occur

def assemble_data (device_id,device_type,function_type,param_count):
	
	return data

def forward ():
	 print "In forward"
	 data = []
	 device_id = 2				#DC Motors has device id = 2
	 device_type = 1			#DC Motors is o/p device. hence device type = 0	
	 function_type = 0			#Function_type = 0 for forward motion 
	 param_count = 0			#No parameter is sent through forward function hence param_count = 0
	 data.append(chr(device_id))
	 data.append(chr(device_type))
	 data.append(chr(function_type))
	 data.append(chr(param_count))
	 data.append("\n")
	 data.append("\r") 
	 
	 for i in range(0,len(data)):
		 port.write(str(data[i]))
		 print str(data[i])
	 #port.write(str(device_id))
	 #print "device_id =", device_id
	 #port.write(str(device_type))
	 #port.write(str(function_type))
	 #port.write(str(param_count))
	 #port.write("\n")
	 #port.write("\r")
	 print "packet sent is" , str(data)
	 return
	
def stop ():
	 print "in Stop"
	 device_id = 2
	 device_type = 1
	 function_type = 4
	 param_count = 0
	 port.write(chr(device_id))
	 port.write(chr(device_type))
	 port.write(chr(function_type))
	 print "function_type =",function_type
	 port.write(chr(param_count))
	 port.write("\n")
	 port.write("\r")
	 return

def buzzer_on():
	 device_id = 1
	 device_type = 1
	 function_type = 0
	 param_count = 0
	 port.write(chr(device_id))
	 port.write(chr(device_type))
	 port.write(chr(function_type))
	 port.write(chr(param_count))
	 port.write("\n")
	 port.write("\r")
	 return
	
def buzzer_off():
	 device_id = 1
	 device_type = 1
	 function_type = 1
	 param_count = 0
	
	 port.write(chr(device_id))
	 port.write(chr(device_type))
	 port.write(chr(function_type))
	 port.write(chr(param_count))
	 port.write("\n")
	 port.write("\r")
	 #print "buzzer off"
	 return

def velocity(left_motor,right_motor):
	data = []
	device_id = 2
	device_type = 1
	function_type = 9
	param_count = 2
	param_1 = left_motor
	param_2 = right_motor
	data.append(chr(device_id))
	data.append(chr(device_type))
	data.append(chr(function_type))
	data.append(chr(param_count))
	data.append(chr(param_1)) 
	data.append(chr(param_2))
	data.append("\n")
	data.append("\r") 
	 
	for i in range(0,len(data)):
		port.write(str(data[i]))
		#print str(data[i])
	print "packet sent is ", str(data)
	return

def adc_conversion(channel_no):
	data = []
	device_id = channel_no
	device_type = 0			# sensors are input so device_type is 0
	function_type = 0
	param_count = 0
	data.append(chr(device_id))
	data.append(chr(device_type))
	data.append(chr(function_type))
	data.append(chr(param_count))
	data.append("\n")
	data.append("\r") 
	
	for i in range(0,len(data)):
		port.write(str(data[i]))
		#print str(data[i])
	print "packet sent is ", str(data)
	
	ret = port.read()
	print "channel no:",channel_no, "returned: ", '%s' %str(ord(ret))
	
	return '%s' %str(ord(ret))

while True:
	
	y= raw_input("Enter the number:")
	if y == '0':
		stop()
		print "good bye"
		break
	if y == '1':
		print "test running"
		forward()
		time.sleep(5)
		stop()
		time.sleep(2)
		
		#buzzer_on()
		#time.sleep(1)
		#buzzer_off()
		#time.sleep(1)
		
		velocity(255,255)
		print "velocity set to 255,255"
		ret = port.read()
		print "value returned by bot is ", ret
		time.sleep(3)
		velocity(255,200)
		print "velocity set to 200,200"
		time.sleep(5)
		velocity(0,0)
		print "velocity set to 0,0"
		time.sleep(3)
		velocity(255,255)
		print "velocity set to 255,255"
		time.sleep(3)
	
#----------------------- Line following ----------------------#	
	if y == '2':
		while (1):
			print "wl_threshold set to: ",wl_threshold
			left_sensor_value = int(adc_conversion(3))
			centre_sensor_value = int(adc_conversion(2))
			right_sensor_value = int(adc_conversion(1))
			#time.sleep(1) 				# for debugging purpose
			
		#	'''
			if ((left_sensor_value < wl_threshold) and (centre_sensor_value < wl_threshold) and (right_sensor_value < wl_threshold)):			# all 3 on white
				print "all on white"
				velocity(0,0)			# Stop
				
			if ((left_sensor_value > wl_threshold) and (centre_sensor_value < wl_threshold) and (right_sensor_value  < wl_threshold)):	# Right & centre on white - left deviation	
				print "right and centre on white"
				velocity(230,200)		# right turn
			
			if ((left_sensor_value > wl_threshold) and (centre_sensor_value > wl_threshold) and (right_sensor_value  < wl_threshold)):	# Right on white - more left deviation
				print "right on white"
				velocity(255,180)		# right turn
				
			if ((left_sensor_value < wl_threshold) and (centre_sensor_value < wl_threshold) and (right_sensor_value  > wl_threshold)):	# Left & centre on white - right deviation		
				print "left and centre on white"
				velocity(200,230)		# left turn
				
			if ((left_sensor_value < wl_threshold) and (centre_sensor_value > wl_threshold) and (right_sensor_value  > wl_threshold)):	# Left on white - more right deviation	
				print "left on white"
				velocity(180,255)		# left turn
			
			if ((left_sensor_value > wl_threshold) and (centre_sensor_value < wl_threshold) and (right_sensor_value  > wl_threshold)):	# centre on white - no deviation	
				print "centre on white"
				velocity(255,255)		# forward
			
			if ((left_sensor_value > wl_threshold) and (centre_sensor_value > wl_threshold) and (right_sensor_value  > wl_threshold)):	# no 3 on white
				print "all on black"
				velocity(0,0)			# Stop
			
			time.sleep(0.5)
			port.flushInput()
			port.flushOutput()
			
			#adc_conversion(1)		# R WL
			#adc_conversion(2)		# C WL
			#adc_conversion(3)		# L WL
		
			#adc_conversion(4)
			#adc_conversion(5)
			#adc_conversion(6)

		#	'''
	
#----------------------- Adaptive cruise control ----------------------#	
	if y == '3':
		print "Line threshold set to: ",wl_threshold
		print "Sharp threshold set to: ",sharp_threshold
		print "IR threshold set to: ",ir_threshold
		while (1):
			left_sensor_value = int(adc_conversion(3))
			centre_sensor_value = int(adc_conversion(2))
			right_sensor_value = int(adc_conversion(1))
			
			front_sharp_value = int(adc_conversion(11))
			front_ir_value = int(adc_conversion(6))
			
			buzzer_off()
			#time.sleep(1)
			flag_object = 0				# goes high when object is detected in-front of robot
			
				
			if ((front_sharp_value > sharp_threshold) or (front_ir_value < ir_threshold)):
				print "Object detected"
				flag_object = 1
				velocity(0,0)			# Stop
				buzzer_on()
				#time.sleep(1)
			#else:
			#	print "not in if"
			#	buzzer_off()
			
		#	"""		
			if ((left_sensor_value < wl_threshold) and (centre_sensor_value < wl_threshold) and (right_sensor_value < wl_threshold) and (flag_object == 0)):			# all 3 on white
				print "all on white"
				velocity(0,0)			# Stop
				buzzer_off()
				
			if ((left_sensor_value > wl_threshold) and (centre_sensor_value < wl_threshold) and (right_sensor_value  < wl_threshold) and (flag_object == 0)):	# Right & centre on white - left deviation	
				print "right and centre on white"
				velocity(230,200)		# right turn
				buzzer_off()
			
			if ((left_sensor_value > wl_threshold) and (centre_sensor_value > wl_threshold) and (right_sensor_value  < wl_threshold) and (flag_object == 0)):	# Right on white - more left deviation
				print "right on white"
				velocity(255,180)		# right turn
				buzzer_off()
				
			if ((left_sensor_value < wl_threshold) and (centre_sensor_value < wl_threshold) and (right_sensor_value  > wl_threshold) and (flag_object == 0)):	# Left & centre on white - right deviation		
				print "left and centre on white"
				velocity(200,230)		# left turn
				buzzer_off()
				
			if ((left_sensor_value < wl_threshold) and (centre_sensor_value > wl_threshold) and (right_sensor_value  > wl_threshold) and (flag_object == 0)):	# Left on white - more right deviation	
				print "left on white"
				velocity(180,255)		# left turn
				buzzer_off()
			
			if ((left_sensor_value > wl_threshold) and (centre_sensor_value < wl_threshold) and (right_sensor_value  > wl_threshold) and (flag_object == 0)):	# centre on white - no deviation	
				print "centre on white"
				velocity(255,255)		# forward
				buzzer_off()
				
			if ((left_sensor_value > wl_threshold) and (centre_sensor_value > wl_threshold) and (right_sensor_value  > wl_threshold) and (flag_object == 0)):	# no 3 on white
				print "all on black"
				velocity(0,0)			# Stop
				buzzer_off()
		#	'''
			time.sleep(0.5)
			port.flushInput()
			port.flushOutput()
			
			#adc_conversion(1)		# R WL
			#adc_conversion(2)		# C WL
			#adc_conversion(3)		# L WL
		
			#adc_conversion(4)
			#adc_conversion(5)
			#adc_conversion(6)

	
	#port.flushOutput()
	#ret = port.read()
	#print "data returned by bot = ", ret
	
	

print "out of the loop"
port.close()
