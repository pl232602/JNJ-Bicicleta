import cv2
import numpy as np 
  
 
cap = cv2.VideoCapture(r'C:\Users\Niles\OneDrive\Documents\EDD-Capstone-Project\30 minute Fat Burning Indoor Cycling Workout Alps South Tyrol Lake Tour Garmin 4K Video.mp4')
def avg(input_list):
    try:
        print(abs(sum(input_list)/len(input_list)))
        return (sum(input_list)/len(input_list))
    except ZeroDivisionError as error:
        pass


while True: 
    ret, frame = cap.read() 
    if ret == True: 
        slope_left = []
        slope_right = []
        x1s = []
        x2s = []
        y1s = []
        y2s = []
        lx1s = []
        lx2s = []
        ly1s = []
        ly2s = []
        rx1s = []
        rx2s = []
        ry1s = []
        ry2s = []
        stash = frame
        lower_yellow = np.array([220,220,220])
        upper_yellow = np.array([255,255,255])

        h, w, l = frame.shape


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
                    
                    x1s.append(x1)
                    x2s.append(x2)
                    y1s.append(y1)
                    y2s.append(y2)
                    if average_slope > 0:
                        lx1s.append(x1)
                        lx2s.append(x2)
                        ly1s.append(y1)
                        ly2s.append(y2)
                        print("bigger")
                        
                    elif average_slope < 0:
                        rx1s.append(x1)
                        rx2s.append(x2)
                        ry1s.append(y1)
                        ry2s.append(y2)
                        print("smaller")
                        
            alx1s = int(avg(lx1s))
            alx2s = int(avg(lx2s))
            aly1s = int(avg(ly1s))
            aly2s = int(avg(ly2s))
            cv2.line(frame, (alx1s,aly1s), (alx2s,aly2s), (0,0,255), 2)

            arx1s = int(avg(rx1s))
            arx2s = int(avg(rx2s))
            ary1s = int(avg(ry1s))
            ary2s = int(avg(ry2s))
            cv2.line(frame, (arx1s,ary1s), (arx2s,ary2s), (0,0,255), 2)

            m1 = (aly2s - aly1s) / (alx2s - alx1s)
            b1 = aly1s - m1 * alx1s

            m2 = (ary2s - ary1s) / (arx2s - arx1s)
            b2 = ary1s - m2 * arx1s

            x_intersection = (b2 - b1) / (m1 - m2)

            y_intersection = m1 * x_intersection + b1

            frame = cv2.circle(frame, (int(x_intersection),int(y_intersection)), radius=0, color=(255, 255, 0), thickness=10)



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