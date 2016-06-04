'''
Application: Development of Raspberry Pi controlled Firebird-V Robot.
Hardware: Firebird-V Atmega2560 Robot and Raspberry Pi 2
Python Version: 2.7
Requirements:
App: Wireless IMU on the Android enabled smartphone
PI:  Servoblaster package for Hardware PWM pulses ON GPIO (source:github/richardghirst/PiBits)

Description: For Gimbal Control using Cardboard and Android Smartphone
This file accepts udp PACKETS from the phone and uses those values to map to angles and control 2 servos(Pan and Tilt)
on gpio pin 4(pwm hardwaee channel 0) and gpio pin 17

(name inspired by Mastodon)
--------------------------------------------------------------------
Usage:
Run the program
 
'''
import socket,traceback,os
from time import sleep
import datetime
import math
#start servo_blaster
os.system('sudo ./servod')
os.system('echo 1=150 > /dev/servoblaster')
os.system('echo 0=150 > /dev/servoblaster')

sleep(1)

host=''
port = 5555

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
s.bind((host,port))

def value_map(x, in_min, in_max, out_min, out_max):
    val=int((x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min);
    if val>250:
        val=250
    elif val<50:
        val=50
    return val

sleep(0.5)
LP=0.20
gyrolimit=0.0
gyroXangle=0.0
gyrolimit=0.0002
while 1:
    a=datetime.datetime.now()
    try:
        message,address=s.recvfrom(8192)
        axl_x=float(message[17:23])
        axl_y=float(message[25:31])
        axl_z=float(message[33:39])
	try:
		gyr_x=float(message[45:51])
		#gyr_y=float(message[53:59])
		#gyr_z=float(message[61:67])
	except:
		pass
	gyroXangle+=gyr_x*LP
        degrees=value_map(axl_z,-9.5,+9.5,50,250)
        degrees2=value_map(gyroXangle,gyrolimit-17.0,gyrolimit+18.0,250,50)
	#pitch=180*math.atan(axl_x/math.sqrt(axl_y*axl_y+axl_z*axl_z))   uncomment for complimentary filter calculations
	#roll=180*math.atan(axl_y/math.sqrt(axl_x*axl_x+axl_z*axl_z))    uncomment for complimentary filter calculations
	print "degrees: %f degrees2: %f "%(degrees,degrees2)
	string = "echo 0=%d > /dev/servoblaster" % (degrees2)
	os.system(string)
        
	string = "echo 1=%d > /dev/servoblaster" % (degrees)
	os.system(string)
	
	
    except(KeyboardInterrupt,SystemExit):
	os.system('sudo killall servod')
	break
        raise
    except:
        traceback.print_exc()
    b=datetime.datetime.now()
    print((b-a).microseconds/1000)
time.sleep(1)
os.system('sudo killall servod')

