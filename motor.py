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

vibrate_input_1 = 5
vibrate_input_2 = 6

vibrate_input_3 = 17
vibrate_input_4 = 27

vibrate_left_clock = 13
vibrate_right_clock = 22

GPIO.setup(vibrate_input_1, GPIO.OUT)
GPIO.setup(vibrate_input_2, GPIO.OUT)
GPIO.setup(vibrate_input_3, GPIO.OUT)
GPIO.setup(vibrate_input_4, GPIO.OUT)
GPIO.setup(vibrate_left_clock, GPIO.OUT)
GPIO.setup(vibrate_right_clock, GPIO.OUT)
pwm_vibrate_left = GPIO.PWM(vibrate_left_clock,1000)
pwm_vibrate_right = GPIO.PWM(vibrate_right_clock,1000)

def left(speed):
    pwm.start(speed)
    GPIO.output(input_1,GPIO.LOW)
    GPIO.output(input_2,GPIO.HIGH)
    time.sleep(0.35)
    pwm.ChangeDutyCycle(0)

def right(speed):
    pwm.start(speed)
    GPIO.output(input_1,GPIO.HIGH)
    GPIO.output(input_2,GPIO.LOW)
    time.sleep(0.35)
    pwm.ChangeDutyCycle(0)

def vibrate_left():
    pwm_vibrate_left.start(100)
    GPIO.output(vibrate_input_3, GPIO.HIGH)
    GPIO.output(vibrate_input_4, GPIO.LOW)
    time.sleep(0.1)
    pwm_vibrate_left.ChangeDutyCycle(0)
    x=0
    while x < 4:
        time.sleep(0.1)
        pwm_vibrate_left.ChangeDutyCycle(100)
        time.sleep(0.1)
        pwm_vibrate_left.ChangeDutyCycle(0)
        x = x + 1

def vibrate_right():
    pwm_vibrate_right.start(100)
    GPIO.output(vibrate_input_1, GPIO.HIGH)
    GPIO.output(vibrate_input_2, GPIO.LOW)
    time.sleep(0.1)
    pwm_vibrate_right.ChangeDutyCycle(0)
    x=0
    while x < 4:
        time.sleep(0.1)
        pwm_vibrate_right.ChangeDutyCycle(100)
        time.sleep(0.1)
        pwm_vibrate_right.ChangeDutyCycle(0)
        x = x + 1

if __name__ == "__main__":
    left(80)
    right(80)
