#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import pygame
import sys

cnl = 19
mypin = 16
GPIO.setmode(GPIO.BCM)
step_pins = [17, 22, 23, 24]
# 
# this is from here: https://defendtheplanet.net/2014/05/04/controlling-a-stepper-motor-28byi-48-with-a-raspberry-pi/
#
# import required libs



def turn_motor(angle, step_sleep=0.001, pulse_sleep=0.001):
    GPIO.setwarnings(False)
#    GPIO.cleanup() #cleaning up in case GPIOS have been preactivated
     
    # Use BCM GPIO references
    # instead of physical pin numbers
#    GPIO.setmode(GPIO.BCM)
     
    # be sure you are setting pins accordingly
    step_pins = [17, 22, 23, 24]
     
    # Set all pins as output
    for pin in step_pins:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin, False)

    time.sleep(0.5)
    STEPS_PER_TURN = 512
    FULL_TURN = 360  # degrees
# Define simple sequence
    seq1 = [
            [1,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            [0,0,0,1],
           ]
     
# Define advanced sequence
# as shown in manufacturers datasheet
    seq2 = [
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1],
           ]

#Full torque
    seq3 = [
            [0,0,1,1],
            [1,0,0,1],
            [1,1,0,0],
            [0,1,1,0],
           ]
     
# Choose the sequence
    seq = seq2
# How many steps
    steps = int(angle * (STEPS_PER_TURN / FULL_TURN))
    if steps < 0:
        steps = abs(steps)
        seq.reverse()

    for step in range(steps):
        for pulse in range(len(seq)):
            #print("Step: ", step)
            for pin in range(len(step_pins)):
                GPIO.output(step_pins[pin], bool(seq[pulse][pin]))
                time.sleep(pulse_sleep)
                #print("Pin: ", step_pins[pin], "Signal: ", bool(seq[pulse][pin]))
    # Wait before moving on
        time.sleep(step_sleep)


def reset_motor(pins):
 #   GPIO.cleanup();
 #   GPIO.setmode(GPIO.BCM)
    for pin in pins:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin, False)

def main():
    GPIO.setup(cnl, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setwarnings(False)
    GPIO.setup(mypin, GPIO.OUT, initial=GPIO.LOW) 
    pygame.mixer.init()
    pygame.mixer.music.load("alarm.wav")
    try:
        while(True):
            if GPIO.input(cnl) == 1:
                GPIO.output(mypin, GPIO.HIGH)  #turn led on
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()
                    turn_motor(180)
            else:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
     #               reset_motor(step_pins)
                GPIO.output(mypin, GPIO.LOW)
            time.sleep(0.05)
    except KeyboardInterrupt:
          GPIO.cleanup()
          print("Exiting")


if __name__ == "__main__":
    main()

