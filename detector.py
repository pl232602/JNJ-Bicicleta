import cv2
import numpy as np 
  
 
cap = cv2.VideoCapture(r'C:\Users\pl232602\Work Folders\Documents\EDD-Capstone-Project\30 minute Fat Burning Indoor Cycling Workout Alps South Tyrol Lake Tour Garmin 4K Video.mp4') 
  

while(cap.isOpened()): 
      

    ret, frame = cap.read() 
    if ret == True: 
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        mask = cv2.threshold(frame, thresh=180, maxval=255, type=cv2.THRESH_BINARY)
        im_thresh_gray = cv2.bitwise_and(frame, mask)
        cv2.imshow('Frame', im_thresh_gray) 
          

        if cv2.waitKey(25) & 0xFF == ord('q'): 
            break
 
    else: 
        break
  

cap.release() 

cv2.destroyAllWindows() 