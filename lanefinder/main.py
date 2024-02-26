import os
import cv2
import yaml
from lanefinder.inference.lanefinder import Lanefinder

config_path = "/home/nilesosa/Documents/JNJ-Bicicleta/lanefinder/config.yaml"
model_path = "/home/nilesosa/Documents/JNJ-Bicicleta/lanefinder/assets/models/nightlane_rev2_edgetpu.tflite"
video_path = "/home/nilesosa/Documents/JNJ-Bicicleta/30 minute Fat Burning Indoor Cycling Workout Alps South Tyrol Lake Tour Garmin 4K Video.mp4"

def read_config():
    if not os.path.isfile(config_path):
        raise FileNotFoundError('Could not find config file')

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    return config


def main():
    # set video stream to fullscreen
    config = read_config()
    lanefinder = Lanefinder(
        model=model_path,
        input_shape=config['input_shape'],
        output_shape=tuple(config['output_shape']),
        quant=config['quantization'],
        dequant=config['dequantization'],
        video_path=video_path
    )

    # set window name to one with fullscren property
    # and run
    for frame, edge in lanefinder.stream():
        yield frame,edge


if __name__ == '__main__':
    main()
