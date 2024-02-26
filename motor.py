import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

input_1 = 23
input_2 = 24
clock = 25

GPIO.setup(input_1, GPIO.OUT)
GPIO.setup(input_2, GPIO.OUT)
GPIO.setup(clock, GPIO.OUT)
pwm = GPIO.PWM(clock, 1000)
##pwm.start(25)

def left(speed):
    pwm.start(speed)
    GPIO.output(input_1,GPIO.LOW)
    GPIO.output(input_2,GPIO.HIGH)
    time.sleep(0.3)
    pwm.ChangeDutyCycle(0)

def right(speed):
    pwm.start(speed)
    GPIO.output(input_1,GPIO.HIGH)
    GPIO.output(input_2,GPIO.LOW)
    time.sleep(0.3)
    pwm.ChangeDutyCycle(0)
if __name__ == "__main__":
    left(60)
    time.sleep(2)
    right(60)
    time.sleep(2)
