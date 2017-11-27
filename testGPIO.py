import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
GPIO.setwarnings(False)
while True :
    
    #GPIO.setup(8, GPIO.OUT)
    GPIO.output(16, GPIO.HIGH)
    time.sleep(0.5)
    #GPIO.output(8, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)
    time.sleep(0.5)
