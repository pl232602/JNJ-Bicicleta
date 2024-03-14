from encoder import encoder
from multiprocessing import Process, Value, Manager
import threading as th
import time
import RPi.GPIO as GPIO
from simple_pid import PID


GPIO.setmode(GPIO.BCM)

input_1 = 19
input_2 = 26
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

manager = Manager()

global encoder_values

encoder_values = manager.list([0])
encoder_process = Process(target = encoder, args=(encoder_values,))
encoder_process.start()

def left(speed):
    direction = "left"
    motorp = th.Thread(target = motor_controller, args = (direction,))
    motorp.start()

def right(speed):
    direction = "right"
    motorp = th.Thread(target = motor_controller, args = (direction,))
    motorp.start()

def motor_controller(direction):
    kp = 1
    ki = 1
    kd = 1
    motor_pid = PID(kp,ki,kd,setpoint = 0)
    motor_pid.output_limits = (-1000,1000)
    if direction == "right":
        change_value = -25
    elif direction == "left":
        change_value = 25
    motor_pid.setpoit = change_value
    while True:
        pid_output = motor_pid(encoder_values[0])
        print(pid_output)
def motor_left(speed):
    pwm.start(speed)
    GPIO.output(input_1, GPIO.HIGH)
    GPIO.output(input_2, GPIO.LOW)

def motor_right(speed):
    pwm.start(speed)
    GPIO.output(input_1, GPIO.HIGH)
    GPIO.output(input_2,GPIO.LOW)

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
    vibrate_left()
    vibrate_right()
