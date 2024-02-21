import cv2
from ultrafastLaneDetector import UltrafastLaneDetector, ModelType

model_path = r"/home/nilesosa/Documents/JNJ-Bicicleta/tensorflow_tingz/models/model_float32.tflite"
model_type = ModelType.TUSIMPLE


image_path = r"/home/nilesosa/Downloads/Lane-Segmentation-master/data/istockphoto-843184110-612x612.jpg"

# Initialize lane detection model
lane_detector = UltrafastLaneDetector(model_path, model_type)

# Read RGB images
img = cv2.imread(image_path, cv2.IMREAD_COLOR)

# Detect the lanes
output_img = lane_detector.detect_lanes(img)

# Draw estimated depth
cv2.namedWindow("Detected lanes", cv2.WINDOW_NORMAL) 
cv2.imshow("Detected lanes", output_img)
cv2.waitKey(0)

cv2.imwrite("output.jpg",output_img)
