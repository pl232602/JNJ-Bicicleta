import serial
import time
import re

ser = serial.Serial('/dev/ttyACM1',9600)

def encoder(encoder_list):
    global broke_down
    while True:
        line = ser.readline()
        try:
            line = line.decode('utf-8').strip()
            matches = re.findall(r'enca(-?\d+)', line)

            if matches:
                enca_value = int(matches[0])

                encoder_list[0] = enca_value
                if __name__ == "__main__":
                    print(encoder_list)

        except UnicodeDecodeError as e:
            print("broken")

if __name__ == "__main__":
    list = [0]
    encoder(list)