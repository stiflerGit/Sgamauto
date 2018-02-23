#!/usr/bin/python
# shutdown/reboot(/power on) Raspberry Pi with pushbutton
import RPi.GPIO as GPIO
from subprocess import call
from datetime import datetime
import time
import client

# pushbutton connected to this GPIO pin, using pin 5 also has the benefit of
# waking / powering up Raspberry Pi when button is pressed
shutdownPin = 5
readyPin = 36 
# if button pressed for at least this long then shut down. if less then reboot.
shutdownMinSeconds = 3

# button debounce time in seconds
debounceSeconds = 0.01

GPIO.setmode(GPIO.BOARD)
GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

buttonPressedTime = None
clientDev = None

def buttonStateChanged(pin):
    global buttonPressedTime

    if not (GPIO.input(pin)):
        # button is down
        if buttonPressedTime is None:
            buttonPressedTime = datetime.now()
    else:
        # button is up
        if buttonPressedTime is not None:
            elapsed = (datetime.now() - buttonPressedTime).total_seconds()
            buttonPressedTime = None
            if elapsed >= shutdownMinSeconds:
                # button pressed for more than specified time, shutdown
                call(['shutdown', '-h', 'now'], shell=False)
            elif elapsed >= debounceSeconds:
                GPIO.output(readyPin, GPIO.HIGH)
                clientDev.finalTest()
                GPIO.output(readyPin, GPIO.LOW)
                # button pressed for a shorter time, reboot
                call(['shutdown', '-r', 'now'], shell=False)


# subscribe to button presses
print "ciao"
#inizializzo il client
GPIO.setup(readyPin, GPIO.OUT)
GPIO.output(readyPin, GPIO.HIGH)
clientDev = client.clientDevice("AB123CD","192.168.1.73","5052")
clientDev.initialTest()
GPIO.output(readyPin, GPIO.LOW)
GPIO.add_event_detect(shutdownPin, GPIO.BOTH, callback=buttonStateChanged)
while True:
# sleep to reduce unnecessary CPU usage
    time.sleep(5)
