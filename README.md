# Virtual-Telepresence
3d Telepresence(SBS)  Platform using Google Cardboard and Raspberry Pi 2

View our current Implementation: https://www.youtube.com/watch?v=YWjOEWO5lFs

(I really need expertise in perfecting this project from you fellow tinkers. Any contributions are gladly accepted with a transfer of ASCII cookies. Here, have a cookie :')

               -=[ cookies & milk ]=- 

                               .-'''''-.
                               |'-----'|
                               |-.....-|
                               |       |
                               |       |
              _,._             |       |
         __.o`   o`"-.         |       |
      .-O o `"-.o   O )_,._    |       |
     ( o   O  o )--.-"`O   o"-.`'-----'`
      '--------'  (   o  O    o)  
                   `----------`
 

Requirements:  

Hardware:  

  Firebird V Platform (Nex Robotics):http://www.nex-robotics.com/fire-bird-v-atmega2560/fire-bird-v-atmega2560.html  
  Raspberry Pi 2  
  Raspicam camera module  
  USB-UART cable  
  Jumper Wires  
  2 servo motors (pan and tilt)  
  camera gimbal platform(self made)  
  Wifi dongle  
  
Software:

Scripts: Pyhton(Bash for automation of scripts on Raspi boot: http://www.instructables.com/id/Raspberry-Pi-Launch-Python-script-on-startup/?ALLSTEPS)  
  1. servo_blasteroid: For recieving udp packets and running servos on gpio pin 4 and 17  
  2. Sample_Experiments.py: modified using pygame library for control using keyboard (W,A,S,D). Modified based on prior work by Saurav Shandilya.  

Libraries/Utilities/Dependancies:
  
  ServoBlaster: https://github.com/richardghirst/PiBits/tree/master/ServoBlaster  
  FireBird-RPi Interface: https://github.com/sauravshandilya/Fi-Pi (modified)  
  Pygame: http://www.pygame.org/wiki/about  
  UV4L: http://www.linux-projects.org/modules/sections/index.php?op=viewarticle&artid=14  
  
Apps: (Available for Android Market)  
  
  Wireless IMU: https://play.google.com/store/apps/details?id=org.zwiener.wimu&hl=en  
  DualScreen: https://play.google.com/store/apps/details?id=com.goestoweb.dualbrowser&hl=en  



