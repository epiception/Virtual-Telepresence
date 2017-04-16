# Virtual-Telepresence
## 3d Telepresence(SBS)  Platform using Google Cardboard and Raspberry Pi 2

### View our current Implementation: 
<a href="http://www.youtube.com/watch?feature=player_embedded&v=YWjOEWO5lFs
" target="_blank"><img src="http://img.youtube.com/vi/YWjOEWO5lFs/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>

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
 

### Requirements:  

#### Hardware:  
1. Firebird V Platform ([Nex Robotics](http://www.nex-robotics.com/fire-bird-v-atmega2560/fire-bird-v-atmega2560.html))  
2. Raspberry Pi 2  
3. Raspicam camera module  
4. USB-UART cable  
5. Jumper Wires  
6. 2 servo motors (pan and tilt)  
7. camera gimbal platform(self made)  
8. Wifi dongle  
  
#### Software:

1. Scripts: Python([Startup Script](http://www.instructables.com/id/Raspberry-Pi-Launch-Python-script-on-startup/?ALLSTEPS))
    * servo_blasteroid: For recieving udp packets and running servos on gpio pin 4 and 17
    * Sample_Experiments.py: modified using pygame library for control using keyboard (W,A,S,D). Modified based on prior work by Saurav Shandilya.  

2. Libraries/Utilities/Dependancies:
    * [ServoBlaster](https://github.com/richardghirst/PiBits/tree/master/ServoBlaster) 
    * [FireBird-RPi Interface](https://github.com/sauravshandilya/Fi-Pi) (modified)
    * [Pygame](http://www.pygame.org/wiki/about)
    * [UV4L](http://www.linux-projects.org/modules/sections/index.php?op=viewarticle&artid=14)  

3. Apps: (Available for Android Market)
    * Wireless IMU: https://play.google.com/store/apps/details?id=org.zwiener.wimu&hl=en
    * DualScreen: https://play.google.com/store/apps/details?id=com.goestoweb.dualbrowser&hl=en
