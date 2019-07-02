#!/usr/bin/env python
# license removed for brevity
import rospy
import os
import threading
#import Rpi.GPIO as GPIO 
#from std_msgs.msg import Int16
from kumpulan_msgs.msg import it_control
from kumpulan_msgs.msg import it_vision
from kumpulan_msgs.msg import arduino_it
from urllib2 import urlopen
#from gpiozero import DistanceSensor
from time import sleep
import socket

#=================Database===============================
#def readSensor():
#    global jarak

 #   jarak = 0    
    #jarak = us.distance

def sendDataToServer():

   #threading.Timer(600,sendDataToServer).start()
   urlopen("http://172.20.10.4/cebbot/add_data.php?dist="+str(distance)).read()
   urlopen("http://172.20.10.4/cebbot/add_data.php?rpm="+str(rpm)).read()

#========================Variable========================
#raw data from GUI      (socket)
pitch               = 0                                       
modeManual          = 0         #1 = manual, 0 = auto         

#raw data from vision   (rosmsg)
lineExist           = 0
lineGradient        = 0
#minus = serong kiri | plus = serong kanan
distance = 0
rpm = 0
#data dikirim ke romeo  (serial)
sendKiri            = 0
sendKanan           = 0

#data baca romeo        (serial)
speed               = 0
jarakDepan          = 0 #pake ultrasonik, mungkin fungsinya buat ngurangin kecepatan(?)

#data gerakin roda
lastRodaKanan       = 0
lastRodaKiri        = 0

counterGarisIlang   = 0

wheelSpeed          = 0

toggleForward       = 0

#=================Subscriber it_vision===================
def itcallback(data):
	#rospy.loginfo(rospy.get_caller_id() + "I heard %d", data.line_red)

	global lineGradient 
	lineGradient = data.theta
	rospy.loginfo("i hear R %d",lineGradient)
	#rospy.loginfo(rospy.get_caller_id() + "I heard %d", data.line_blue)

#=================Subscriber arduino_it===================
def itcallback_arduino(arduino_it):
	#rospy.loginfo(rospy.get_caller_id() + "I heard %d", data.line_red)

	global distance 
	distance = arduino_it.distance
	rospy.loginfo("i hear R %d",distance)
	global rpm 
	rpm = arduino_it.rpm
	rospy.loginfo("i hear R %d",rpm)
	#rospy.loginfo(rospy.get_caller_id() + "I heard %d", data.line_blue)

#====================serial function====================

def forward(rodaKiri, rodaKanan, speed, mode):
    global lastRodaKiri
    lastRodaKiri    = rodaKiri
    global  lastRodaKanan
    lastRodaKanan   = rodaKanan

    sendKiri        = (rodaKiri / 5) * speed
    sendKanan       = (rodaKanan/ 5) * speed
    
    #di bawah ini script serial diterusin ke romeo
    #.............................................
    #.............................................

# def kirimSocket():
#     #di bawah ini script socket buat kirim ke GUI
#     #.............................................
#     #.............................................    

# def terimaSocket():
#     #di bawah ini script socket buat terima dari GUI
#     #.............................................
#     #.............................................    

#=======reading the ultrasonic to decide the wheelSpeed=======

def decideWheelSpeed(distance):
    if(distance>2000):
        wheelSpeed = 5
    elif(distance>1500):
        wheelSpeed = 4
    elif(distance>1000):
        wheelSpeed = 3
    elif(distance>500):
        wheelSpeed = 2
    elif(distance>250):
        wheelSpeed = 1
    else:
        wheelSpeed = 0
    
#=======reading the slope(theta) from vision / controller=======

def degreeDecision(slope):

    #diisi gradient kalo acuannya garis, diisi pitch kalo acuannya controller
    if(slope>0):                    #harus belok kanan
        if(slope<5):
            forward(255, 240, wheelSpeed, 1)
        elif(slope<30):
            forward(255, 180, wheelSpeed, 1)
        elif(slope<60):
            forward(255, 120, wheelSpeed, 1)
        elif(slope<90):
            forward(255, 60, wheelSpeed, 1)
        else:
            forward(255, 30, wheelSpeed, 1)
    elif(slope<0):
        if(slope>-5):
            forward(240, 255, wheelSpeed, 1)
        elif(slope>-30):
            forward(180, 255, wheelSpeed, 1)
        elif(slope>-60):
            forward(120, 255, wheelSpeed, 1)
        elif(slope>-90):
            forward(60, 255, wheelSpeed, 1)
        else:
            forward(30, 255, wheelSpeed, 1)
    else:
        forward(255, 255, wheelSpeed, 1)

#=====================MODE BERMAIN=====================#

def manualMode():
    degreeDecision(pitch)
    if(not toggleForward):
        wheelSpeed = 0
        forward(0, 0, wheelSpeed, HIGH)

def autoMode():
    global counterGarisIlang
    rospy.loginfo("masuk auto")
    if(1):#lineExist):
        degreeDecision(lineGradient)
        counterGarisIlang = 0
        rospy.loginfo("masuk eko")
    else:
        if(counterGarisIlang<50):
	    LOW = 0
	    HIGH = 0
            forward(lastRodaKiri, lastRodaKanan, LOW, HIGH)
        else:
	    LOW = 0
	    HIGH = 0
            forward(0, 0, HIGH, LOW)
        counterGarisIlang+=1

#=====================MAIN CODE=====================#

def main():
    rospy.init_node('control', anonymous=True)
    pub = rospy.Publisher('it_control', it_control, queue_size=10)
    sub = rospy.Subscriber('it_vision',it_vision, itcallback)
    sub = rospy.Subscriber('arduino_it',arduino_it, itcallback_arduino)
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
	#decideWheelSpeed()
        if(modeManual==1):
            manualMode()
        else:
            autoMode()
	msg = it_control()
	msg.lastRodaKiri=lastRodaKiri
	msg.lastRodaKanan=lastRodaKanan
	#rospy.loginfo("masuk %d",data_visionB)
	#pub.Publish(msg)
	rospy.loginfo(lastRodaKiri)
	pub.publish(msg)
	#rospy.spin()
	#pub.publish(hello_str2)
	rate.sleep()
	sendDataToServer()

if __name__ == '__main__':
	main()

