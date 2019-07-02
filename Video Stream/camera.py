import cv2
import time
import numpy as np
import math

def getROI(frame):
    upper_left  = (50, 50)
    bottom_right = (720, 480)  
    rect_frame = frame[upper_left[1]:bottom_right[1], upper_left[0]:bottom_right[0]]
    return rect_frame

#def display_lines(frame,lines):
#    line_frame=np.zeros_like(frame)
#    if lines is not None:
#        for x1,y1,x2,y2 in lines:
#           cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
#    return line_frame

cap=cv2.VideoCapture(0)

while True:
    theta=0
    ret, frame= cap.read()
    time.sleep(0.3)
    frame=getROI(frame)
    #frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    gray=cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    blurred=cv2.GaussianBlur(gray,(15,15),0)
    edged=cv2.Canny(blurred,40,120)
    lines=cv2.HoughLinesP(edged,10,np.pi/180,15, 5, 10)

    if lines is not None:
        for x in range (0, len(lines)):
            for x1,y1,x2,y2 in lines [x]:
                cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
                theta=theta+math.atan2((y2-y1),(x2-x1))

    #Draw lines on input image
    if lines is not None:
        for x1,y1,x2,y2 in lines[0]:
            cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(frame,'lines_detected',(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)  
    #line_frame=display_lines(frame,lines)
    
    threshold=5
    print('data: ',theta)
    print('threshold: ', threshold)
        
    cv2.imshow('input', blurred)
    cv2.imshow('canny', edged)
    #cv2.imshow('output', lines)
    cv2.imshow('kamera',frame)

    if(theta > threshold):
        print("left")
    if(theta < -threshold):
        print("right")
    if(abs(theta) < threshold):
        print("straight")
            
    k= cv2.waitKey(5) & 0xFF
    if exit == ord('q'):
        break

cv2.destroyAllWindows()
cap.release
