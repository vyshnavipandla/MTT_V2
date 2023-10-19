import threading
import os
import RPi.GPIO as GPIO

import subprocess
GPIO.setmode(GPIO.BCM)
led_blue = 17
led_green=27
led_red=22
GPIO.setwarnings(False)
GPIO.setup(led_blue, GPIO.OUT)
GPIO.setup(led_green, GPIO.OUT)
GPIO.setup(led_red, GPIO.OUT)
switch_pin = 23

switch_state = False

GPIO.setup(switch_pin, GPIO.IN)

running_process = None

def start_script(file_path):
    global running_process
    if running_process is None:
        print("Starting the script...")
        running_process = subprocess.Popen(["python", file_path])

def stop_script():
    global running_process
    if running_process is not None:
            print("Stopping the script...")
            GPIO.output(led_blue,GPIO.LOW)
            GPIO.output(led_green,GPIO.LOW)
            GPIO.output(led_red,GPIO.LOW)

            running_process.terminate()
            running_process.wait()
            running_process = None

def switch_thread():
    global switch_state
    while True:
        input_state = GPIO.input(switch_pin)
        if input_state == GPIO.LOW and not switch_state:
            switch_state = True
            start_script(file1)
        elif input_state == GPIO.HIGH and switch_state:
            switch_state = False
            stop_script()
        else:
            pass
        

file1 = "/home/Vyshnavi/Desktop/pytree/talktree/main_1.py"


switch_thread = threading.Thread(target=switch_thread)

switch_thread.start()

try:
    while True:
            pass

finally:
    GPIO.cleanup()



