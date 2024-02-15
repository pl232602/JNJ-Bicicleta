import cv2
import numpy as np
import motor

cap = cv2.VideoCapture(r'C:\Users\Niles\OneDrive\Documents\EDD-Capstone-Project\30 minute Fat Burning Indoor Cycling Workout Alps South Tyrol Lake Tour Garmin 4K Video.mp4')

def avg(input_list):
    try:
        return (sum(input_list)/len(input_list))
    except ZeroDivisionError as error:
        pass

def denoiser(image):
    try:
        kernel = np.ones((3,3), np.uint8)
        eroded = cv2.erode(image, kernel, iterations = 1)
        return eroded
    except:
        pass


left_counter = 0
left_lock = False
right_counter = 0
right_lock = False

turned_right = False
turned_left = False

delay = 10

x=0

while True:
    ret, frame = cap.read()
    if ret == True:
        slope_left = 0
        slope_right = 0
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
        lower_white = np.array([230,230,230])
        upper_white = np.array([255,255,255])

        h, w, l = frame.shape


        mask = cv2.inRange(frame, lower_white, upper_white)

        mask = denoiser(mask)

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
                    elif average_slope < 0:
                        rx1s.append(x1)
                        rx2s.append(x2)
                        ry1s.append(y1)
                        ry2s.append(y2)

            alx1s = int(avg(lx1s))
            alx2s = int(avg(lx2s))
            aly1s = int(avg(ly1s))
            aly2s = int(avg(ly2s))

            arx1s = int(avg(rx1s))
            arx2s = int(avg(rx2s))
            ary1s = int(avg(ry1s))
            ary2s = int(avg(ry2s))

            m1 = (aly2s - aly1s) / (alx2s - alx1s)
            b1 = aly1s - m1 * alx1s

            m2 = (ary2s - ary1s) / (arx2s - arx1s)
            b2 = ary1s - m2 * arx1s

            x_intersection = (b2 - b1) / (m1 - m2)
            y_intersection = m1 * x_intersection + b1


            bottom_y = h  # y-coordinate of the bottom of the image

            new_alx2s = int((bottom_y - b1) / m1)
            cv2.line(frame, (int(x_intersection),int(y_intersection)), (new_alx2s, bottom_y), (0, 0, 255), 2)

            new_arx2s = int((bottom_y - b2) / m2)
            cv2.line(frame, (int(x_intersection), int(y_intersection)), (new_arx2s, bottom_y), (0, 0, 255), 2)

            frame = cv2.circle(frame, (int(x_intersection), int(y_intersection)), radius=0, color=(255, 255, 0), thickness=10)

            frame = cv2.circle(frame,(int(w/2),l),radius = 5,color = (255,255,255),thickness = 3)

            left_distance = abs(w/2 - new_alx2s)
            right_distance = abs(w/2 - new_arx2s)


            if left_distance>right_distance:
                left_counter = left_counter + 1
            elif right_distance>left_distance:
                right_counter = right_counter + 1

            if left_counter > right_counter + delay:
                left_lock = True
                right_lock = False
                left_counter = 0
                right_counter = 0

            if right_counter > left_counter + delay:
                right_lock = True
                left_lock = False
                left_counter = 0
                right_counter = 0

            if left_lock == True:
                if turned_left == True:
                    print("compensating right")
                    motor.right(60)
                    turned_left = False
                    
                if turned_right == False:
                    print("right turn motor call")
                    motor.right(60)
                    turned_right = True

            if right_lock == True:
                if turned_right == True:
                    print("compensating left")
                    motor.left(60)
                    turned_right = False
                
                if turned_left == False:
                    print("left turn motor call")
                    motor.left(60)
                    turned_left = True


        except TypeError as e:
            pass

        try:
            cv2.imshow('Frame', frame)
        except:
            pass
        x = x+1
        if (cv2.waitKey(25) & 0xFF == ord('q')) or (x == 9000):
            break

    else:
        break

cap.release()

cv2.destroyAllWindows()
