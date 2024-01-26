import cv2
import numpy as np

cap = cv2.VideoCapture(r'/home/bicicleta/JNJ-Bicicleta/30 minute Fat Burning Indoor Cycling Workout Alps South Tyrol Lake Tour Garmin 4K Video.mp4')

def avg(input_list):
    try:
        return (sum(input_list)/len(input_list))
    except ZeroDivisionError as error:
        pass


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
        lower_yellow = np.array([210,210,210])
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
                print("close to left")
            elif right_distance>left_distance:
                print("close to right")

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
