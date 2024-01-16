import cv2
import numpy as np 
  
 
cap = cv2.VideoCapture(r'C:\Users\pl232602\Work Folders\Documents\EDD-Capstone-Project\30 minute Fat Burning Indoor Cycling Workout Alps South Tyrol Lake Tour Garmin 4K Video.mp4') 
  

while(cap.isOpened()): 
      

    ret, frame = cap.read() 
    if ret == True: 
        slope_left = []
        slope_right = []
        x1s = []
        x2s = []
        y1s = []
        y2s = []
        stash = frame
        lower_yellow = np.array([220,220,220])
        upper_yellow = np.array([255,255,255])

        h, w, l = frame.shape

        frame = frame[int(h/2):h,0:w]

        mask = cv2.inRange(frame, lower_yellow, upper_yellow)
        edges = cv2.Canny(mask, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi/180, 70)

        try:

            for r_theta in lines:
                arr = np.array(r_theta[0], dtype=np.float64)
                r, theta = arr
                a = np.cos(theta)
            
                b = np.sin(theta)
            
                x0 = a*r
            
                y0 = b*r
            
                x1 = int(x0 + 1000*(-b))
            
                y1 = int(y0 + 1000*(a))
            
                x2 = int(x0 - 1000*(-b))
            
                y2 = int(y0 - 1000*(a))

                average_slope = (x2-x1)/(y2-y1)
                if abs(average_slope) < 2:
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    x1s.append(x1)
                    x2s.append(x2)
                    y1s.append(y1)
                    y2s.append(y2)
                    if average_slope > 0:
                        slope_left.append(average_slope)
                    elif average_slope < 0:
                        slope_right.append(average_slope)
                cv2.line(frame, (100,100), (800,800), (0,0,255),2)
            try:
                average_slope_left = sum(slope_left)/len(slope_left)
            except ZeroDivisionError as nothing:
                print("left borked")

            try:
                average_slope_right = sum(slope_right)/len(slope_right)
            except ZeroDivisionError as nothing:
                print("right borked")

            



        except TypeError as e:
            pass


        result = cv2.bitwise_and(frame,frame, mask= mask)

        

        

        cv2.imshow('Frame', frame) 
          
        if cv2.waitKey(25) & 0xFF == ord('q'): 
            break
 
    else: 
        break
  
cap.release() 

cv2.destroyAllWindows() 