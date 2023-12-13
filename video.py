import cv2
import numpy as np
from inference import road_lines

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    frame = road_lines(frame)
    cv2.imshow("Frame", frame)

    if cv2.waitKey(25) & 0xFF == ord('q'): 
        break


cap.release()
cv2.destroyAllWindows()