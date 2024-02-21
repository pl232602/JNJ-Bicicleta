import cv2
from ultrafastLaneDetector import UltrafastLaneDetector, ModelType

model_path = "/home/nilesosa/Documents/JNJ-Bicicleta/tensorflow_tingz/models/model_float32.tflite"
model_type = ModelType.TUSIMPLE

# Initialize video
# cap = cv2.VideoCapture("video.mp4")

cap = cv2.VideoCapture("/home/nilesosa/Documents/JNJ-Bicicleta/30 minute Fat Burning Indoor Cycling Workout Alps South Tyrol Lake Tour Garmin 4K Video.mp4")

# Initialize lane detection model
lane_detector = UltrafastLaneDetector(model_path, model_type)

cv2.namedWindow("Detected lanes", cv2.WINDOW_NORMAL)	

while cap.isOpened():
	try:
		# Read frame from the video
		ret, frame = cap.read()
	except:
		continue
		continue

	if ret:	

		height, width, _ = frame.shape
		cropped_frame = frame[int(height / 2.5):, :]

		# Detect the lanes
		output_img = lane_detector.detect_lanes(cropped_frame)

		cv2.imshow("Detected lanes", output_img)

	else:
		break

	# Press key q to stop
	if cv2.waitKey(1) == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()