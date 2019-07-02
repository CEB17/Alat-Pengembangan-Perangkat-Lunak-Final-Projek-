#!/usr/bin/env python
# Author: Divisi Vision kelas 2TKB 
# program ini menggunakan kamera webcam logitech
# untuk mendeteksi garis hitam


from kumpulan_msgs.msg import it_vision

import rospy
import math
import cv2
import numpy as np

upper_left=(0,0)
bottom_right=(0,0)

def getRoi(image):
	global upper_left
	upper_left=(0,180)
	global bottom_right
	bottom_right=(480,480)
	
	rect_image = image[upper_left[1]:bottom_right[1], upper_left[0]:bottom_right[0]]
	return rect_image
	
def select_hsv_black(image):
	low_black   = np.uint8([0, 0, 0])
	upper_black = np.uint8([180, 255, 40])
	black_mask  = cv2.inRange(image, low_black, upper_black)
	return black_mask

def init_program_vision():
	rospy.init_node('vision', anonymous=True)
        pub = rospy.Publisher('it_vision', it_vision, queue_size=10)
	rate = rospy.Rate(10) # 10hz
        rospy.loginfo("set ROS done")

	theta = 0
	video = cv2.VideoCapture(0)	

	while not rospy.is_shutdown():
		#rospy.loginfo("in looping")
		ret, frame_ori = video.read()#init_program_vision()
		#if not ret:
			# video = cv2.VideoCapture("../resources/solidWhiteRight.mp4")
			# video = cv2.VideoCapture(1)
			# rospy.loginfo("in not")
			#continue
	
		frame = getRoi(frame_ori)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
		# mask  = select_rgb_white_yellow(frame)
		mask  = select_hsv_black(hsv) 
		edges = cv2.Canny(mask, 75, 150)
	
		lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)
		#rospy.loginfo("sebelum for")
		if lines is not None:
			for x in range(0, len(lines)):
				for x1, y1, x2, y2 in lines[x]:
					cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
					theta = theta + math.atan2((y2-y1), (x2-x1))
			
		#rospy.loginfo("setelah for")
		threshold = 5
		print("theta: ", theta)
		print("threshold: ", threshold)
		if(theta > threshold):
			print("left")
		if(theta < -threshold):
			print("right")
		if(abs(theta) < threshold):
			print("straight")


		cv2.imshow("frame", frame)
		cv2.imshow("mask", mask)


		msg = it_vision()
		#msg.line_red=100
		msg.theta=theta
		#pub.Publish(msg)
		#rospy.loginfo(hello_str)
		pub.publish(msg)
		#rospy.loginfo("Data published: %d",msg.line_red)
		#pub.publish(hello_str2)

		theta = 0
		rate.sleep()


		key = cv2.waitKey(25)
		if key == 27:
			break

	video.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	init_program_vision()
