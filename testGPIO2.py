import RPi.GPIO as GPIO
import time
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

GPIO.setmode(GPIO.BOARD)

#GPIO.cleanup()

TRIG = 38 
ECHO1 = 7
ECHO2 = 40


#print ("Distance Measurement In Progress")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO1,GPIO.IN)
GPIO.setup(ECHO2, GPIO.IN)

GPIO.output(TRIG, False)
#print ("Waiting For Sensor To Settle")
#time.sleep(2)

tempArray = [0,0,0]
pubnubConf = PNConfiguration()
pubnubConf.subscribe_key = 'sub-c-1aa69146-117c-11e7-9faf-0619f8945a4f'
pubnubConf.publish_key = 'pub-c-a2c67d8e-1b26-4e00-878b-8b74a6ef3393'
pubnubConf.ssl = False
pubnub = PubNub(pubnubConf)

def my_publish_callback(result, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
        print(result)
    else:
        print(status.original_response)
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

while True:
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO1)==0:
        pulse_start1 = time.time()

    while GPIO.input(ECHO1)==1:
        pulse_end1 = time.time()

    pulse_duration1 = pulse_end1 - pulse_start1

    distance1 = pulse_duration1 * 17150
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
   
    while GPIO.input(ECHO2)==0:
        pulse_start2 = time.time()

    while GPIO.input(ECHO2)==1:
        pulse_end2 = time.time()
    
    pulse_duration2 = pulse_end2 - pulse_start2

    distance2 = pulse_duration2 * 17150
    

    distance1 = round(distance1, 2)
    distance2 = round(distance2, 2)
  
    if distance1 <= 6.0 and distance2 <= 6.0:
        tempArray[0] = 1
        tempArray[1] = 0
        tempArray[2] = 1
    elif distance1 < 6.0 and distance2 > 6.0:
        tempArray[0] = 0
        tempArray[1] = 0
        tempArray[2] = 1
    elif distance1 > 6.0 and distance2 < 6.0:
        tempArray[0] = 1
        tempArray[1] = 0
        tempArray[2] = 0
    else:
        tempArray[0] = 0
        tempArray[1] = 0
        tempArray[2] = 0
    pubnub.publish().channel('awesomeChannel').message(tempArray).should_store(True).use_post(True).async(my_publish_callback)
    time.sleep(1)

GPIO.cleanup()
