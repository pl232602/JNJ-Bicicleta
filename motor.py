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

vibrate_clock = 22


GPIO.setup(vibrate_input_1, GPIO.OUT)
GPIO.setup(vibrate_input_2, GPIO.OUT)
GPIO.setup(vibrate_clock, GPIO.OUT)
pwm_vibrate = GPIO.PWM(vibrate_clock,1000)
def left(speed):
    pwm.start(speed)
    GPIO.output(input_1,GPIO.LOW)
    GPIO.output(input_2,GPIO.HIGH)
    time.sleep(0.25)
    pwm.ChangeDutyCycle(0)

def right(speed):
    pwm.start(speed)
    GPIO.output(input_1,GPIO.HIGH)
    GPIO.output(input_2,GPIO.LOW)
    time.sleep(0.25)
    pwm.ChangeDutyCycle(0)

def vibrate_left():
   pwm_vibrate.start(100)
   GPIO.output(vibrate_input_1, GPIO.HIGH)
   GPIO.output(vibrate_input_2, GPIO.LOW)
   time.sleep(5)
   pwm_vibrate.ChangeDutyCycle(0)

def vibrate_right():
    pwm_vibrate.start(100)
    GPIO.output(vibrate_input_3, GPIO.HIGH)
    GPIO.output(vibrate_input_4, GPIO.LOW)
    time.sleep(5)
    pwm_vibrate.ChangeDutyCycle(0)

if __name__ == "__main__":
    vibrate()
