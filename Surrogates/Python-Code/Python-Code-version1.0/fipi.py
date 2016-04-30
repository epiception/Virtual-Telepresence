'''

Created: 23-04-2015 
Last Modified: 30-03-2016
Author: Original: Saurav Shandilya (e-Yantra Team) [Modified]
Application: Development of Raspberry Pi controlled Firebird-V Robot.
Hardware: Firebird-V Atmega2560 Robot and Raspberry Pi 1
Python Version: 2.7

----------------------------------


'''

#***********************Library Import Starts*********************
import serial
import time 
import glob			# Glob module finds all the pathnames matching a specified pattern. It is used for detecting serial ports in use
import sys			# This module provides access to some variables used or maintained by the interpreter. It is used to exit from program when exception occur

#***********************Library Import Ends*********************


#**********************Variable declaration Starts*********************
global device_id 
global device_type 
global function_type 
global param_count
global port
global port_detect
barLED1 = 1
barLED2 = 2
barLED3 = 4
barLED4 = 8
barLED5 = 16
barLED6 = 32
barLED7 = 64
barLED8 = 128

#**********************Variable declaration Ends*********************

#**********************Communication/Serial Port Detection Starts*********************
def serial_port_connection(port_detect):
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
#**********************Communication/Serial Port Detection Ends*********************

#**********************Open Communication/Serial Port Starts*********************	
def serial_open():	
	port_detect = glob.glob("/dev/ttyUSB*") # stores all /dev/ttyUSB* into a list port_detect
	
	try:
		serial_port_connection(port_detect)
				
		if port.isOpen() == True:
			print "Port is open"
		else:
			serial_port_connection()
				
	except:
		print "No USB port detected....check connection"
		sys.exit(0)		# stop program execution when exception occur
#**********************Open Communication/Serial Port Starts*********************	


#**********************Close Communication/Serial Port Starts*********************	
def serial_close():
	port.close()
#**********************Close Communication/Serial Port Ends*********************


#**********************Forward Starts*********************	
def forward ():
	 print "Forward Motion"
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
#**********************Forward Ends*********************

#**********************Back Starts*********************
def back ():
	 print "Back Motion"
	 data = []
	 device_id = 2				#DC Motors has device id = 2
	 device_type = 1			#DC Motors is o/p device. hence device type = 0	
	 function_type = 1			#Function_type = 0 for forward motion 
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
#**********************Back Starts*********************

#**********************Left Starts*********************	
def left ():
	 print "Forward Motion"
	 data = []
	 device_id = 2				#DC Motors has device id = 2
	 device_type = 1			#DC Motors is o/p device. hence device type = 0	
	 function_type = 2			#Function_type = 0 for forward motion 
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
#**********************Left Ends*********************

#**********************Right Starts*********************	
def right ():
	 print "Forward Motion"
	 data = []
	 device_id = 2				#DC Motors has device id = 2
	 device_type = 1			#DC Motors is o/p device. hence device type = 0	
	 function_type = 3			#Function_type = 0 for forward motion 
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
#**********************Right Ends*********************

#**********************Stop Starts*********************	 
def stop ():
	 print "Stopping DC Motors"
	 device_id = 2
	 device_type = 1
	 function_type = 4
	 param_count = 0
	 port.write(chr(device_id))
	 port.write(chr(device_type))
	 port.write(chr(function_type))
	 port.write(chr(param_count))
	 port.write("\n")
	 port.write("\r")
	 return
#**********************Stop Ends*********************

#**********************Buzzer On Starts*********************
def buzzer_on():
	 print "Buzzer On"
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
#**********************Buzzer On Ends*********************	

#**********************Buzzer Off Starts*********************
def buzzer_off():
	 print "Buzzer OFF"
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
	 return
#**********************Buzzer Off Ends*********************

#**********************Velocity Control Starts*********************
def velocity(left_motor,right_motor):
	print "Left motor velocity = ", '%s' %str(left_motor), "Right motor velocity = ",'%s' %str(right_motor)
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
		print str(data[i])
	print "packet sent is ", str(data)
	return
#**********************Velocity Control Ends*********************

#**********************Forward distance travelled Starts*********************
def forward_mm(distanceinmm):			# maximum allowable value for distanceinmm = 65535
	print "Forward motion for ", "%s" %str(distanceinmm), "mm"
	data = []
	device_id = 3
	device_type = 1
	function_type = 0
	param_count = 1
	param_1 = distanceinmm
	data.append(chr(device_id))
	data.append(chr(device_type))
	data.append(chr(function_type))
	if distanceinmm > 255:
		param_1_1 = distanceinmm%256
		param_1_2 = distanceinmm/256
		data.append(chr(param_count + 16)) 	# adding 16 = 0x10 => if value to be sent over UART > 8 bits
		data.append(chr(param_1_1))
		data.append(chr(param_1_2))
	else: 
		param_1 = distanceinmm
		data.append(chr(param_count))
		data.append(chr(param_1))
	data.append("\n")
	data.append("\r") 
	 
	for i in range(0,len(data)):
		port.write(str(data[i]))
		print str(data[i])
	print "packet sent is ", str(data)
	return
#**********************Forward distance travelled Ends*********************

#**********************Backward distance travelled Starts*********************
def back_mm(distanceinmm):	# maximum allowable value for distanceinmm = 65535
	print "Backward motion for ", "%s" %str(distanceinmm), "mm"
	data = []
	device_id = 3
	device_type = 1
	function_type = 1
	param_count = 1
	param_1 = distanceinmm
	data.append(chr(device_id))
	data.append(chr(device_type))
	data.append(chr(function_type))
	if distanceinmm > 255:
		param_1_1 = distanceinmm%256
		param_1_2 = distanceinmm/256
		data.append(chr(param_count + 16)) 	# adding 16 = 0x10 => if value to be sent over UART > 8 bits
		data.append(chr(param_1_1))
		data.append(chr(param_1_2))
	else: 
		param_1 = distanceinmm
		data.append(chr(param_count))
		data.append(chr(param_1))
	data.append("\n")
	data.append("\r") 
	 
	for i in range(0,len(data)):
		port.write(str(data[i]))
		print str(data[i])
	print "packet sent is ", str(data)
	return	
#**********************Backward distance travelled Ends*********************

#**********************ADC Conversion Starts*********************	
def adc_conversion(channel_no):
	data = []
	device_id = 0
	device_type = 0			# sensors are input so device_type is 0
	function_type = channel_no
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
	port.flushInput()
	port.flushOutput()
	return
#**********************ADC Conversion Ends*********************	

#**********************SPI Starts*********************	
def spi_master_tx_and_rx(channel_no):
	data = []
	device_id = 1
	device_type = 0			# sensors are input so device_type is 0
	function_type = channel_no
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
	print "spi_channel no:",channel_no, "returned: ", '%s' %str(ord(ret))
	port.flushInput()
	port.flushOutput()
	return	
#**********************SPI Ends*********************	

#**********************Servo Control Starts*********************	
def servo_1(degree):
	data = []
	if degree > 180:
		degree = 180
	device_id = 4
	device_type = 1
	function_type = 0
	param_count = 1
	param_1 = degree
	data.append(chr(device_id))
	data.append(chr(device_type))
	data.append(chr(function_type))
	data.append(chr(param_count))
	data.append(chr(param_1)) 
	data.append("\n")
	data.append("\r") 
	 
	for i in range(0,len(data)):
		port.write(str(data[i]))
		print str(data[i])
	print "packet sent is ", str(data)
	
def servo_2(degree):
	data = []
	if degree > 180:
		degree = 180
	device_id = 4
	device_type = 1
	function_type = 1
	param_count = 1
	param_1 = degree
	data.append(chr(device_id))
	data.append(chr(device_type))
	data.append(chr(function_type))
	data.append(chr(param_count))
	data.append(chr(param_1)) 
	data.append("\n")
	data.append("\r") 
	 
	for i in range(0,len(data)):
		port.write(str(data[i]))
		print str(data[i])
	print "packet sent is ", str(data)

def servo_3(degree):
	data = []
	if degree > 180:
		degree = 180
	device_id = 4
	device_type = 1
	function_type = 2
	param_count = 1
	param_1 = degree
	data.append(chr(device_id))
	data.append(chr(device_type))
	data.append(chr(function_type))
	data.append(chr(param_count))
	data.append(chr(param_1)) 
	data.append("\n")
	data.append("\r") 
	 
	for i in range(0,len(data)):
		port.write(str(data[i]))
		print str(data[i])
	print "packet sent is ", str(data)

def servo_1_free():
	data = []
	device_id = 4
	device_type = 1
	function_type = 3
	param_count = 0
	data.append(chr(device_id))
	data.append(chr(device_type))
	data.append(chr(function_type))
	data.append(chr(param_count))
	data.append("\n")
	data.append("\r") 
	 
	for i in range(0,len(data)):
		port.write(str(data[i]))
		print str(data[i])
	print "packet sent is ", str(data)
	
def servo_2_free():
	data = []
	device_id = 4
	device_type = 1
	function_type = 4
	param_count = 0
	data.append(chr(device_id))
	data.append(chr(device_type))
	data.append(chr(function_type))
	data.append(chr(param_count))
	data.append("\n")
	data.append("\r") 
	 
	for i in range(0,len(data)):
		port.write(str(data[i]))
		print str(data[i])
	print "packet sent is ", str(data)
	
def servo_3_free():
	data = []
	device_id = 4
	device_type = 1
	function_type = 5
	param_count = 0
	data.append(chr(device_id))
	data.append(chr(device_type))
	data.append(chr(function_type))
	data.append(chr(param_count))
	data.append("\n")
	data.append("\r") 
	 
	for i in range(0,len(data)):
		port.write(str(data[i]))
		print str(data[i])
	print "packet sent is ", str(data)
#**********************Servo Control Ends*********************
	
def led_bargraph_on(led_no):
	data = []
	device_id = 5
	device_type = 1
	function_type = 0
	param_count = 1
	param_1 = led_no
	data.append(chr(device_id))
	data.append(chr(device_type))
	data.append(chr(function_type))
	data.append(chr(param_count))
	data.append(chr(param_1))
	data.append("\n")
	data.append("\r") 
	 
	for i in range(0,len(data)):
		port.write(str(data[i]))
		print str(data[i])
	print "packet sent is ", str(data)

def led_bargraph_off(led_no):
	data = []
	device_id = 5
	device_type = 1
	function_type = 1
	param_count = 1
	param_1 = (~(led_no)&0xFF)			# python ~ is -x-1 two's complement
	data.append(chr(device_id))
	data.append(chr(device_type))
	data.append(chr(function_type))
	data.append(chr(param_count))
	data.append(chr(param_1))
	data.append("\n")
	data.append("\r") 
	 
	for i in range(0,len(data)):
		port.write(str(data[i]))
		print str(data[i])
	print "packet sent is ", str(data)

	
