import os
import cv2
import yaml
from inference import Lanefinder


def read_config():
    if not os.path.isfile('/home/bicicleta/JNJ-Bicicleta/lanefinder/config.yaml'):
        raise FileNotFoundError('Could not find config file')

    with open('/home/bicicleta/JNJ-Bicicleta/lanefinder/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    return config


def main():
    # set video stream to fullscreen
    window_name = 'lanefinder'
    config = read_config()

    lanefinder = Lanefinder(
        model=config['model'],
        input_shape=config['input_shape'],
        output_shape=tuple(config['output_shape']),
        quant=config['quantization'],
        dequant=config['dequantization']
    )

    # set window name to one with fullscren property
    # and run
    lanefinder.window = window_name
    lanefinder.stream()
    lanefinder.destroy()


if __name__ == '__main__':
    main()
