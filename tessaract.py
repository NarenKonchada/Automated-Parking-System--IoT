from picamera import PiCamera
from time import sleep
import pytesseract
from PIL import Image
import RPi.GPIO as GPIO
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)

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
if GPIO.input(11) == 1:
    camera = PiCamera()
    camera.rotation = 180
    while True:
        camera.start_preview(alpha = 200)
        sleep(2)
        camera.capture('test.jpg')
        img = Image.open('test.jpg')
        w, h = img.size
        #img.crop((0, 30, w, h/2)).save('test.jpg')
        #img = Image.open('test.jpg')
        text = pytesseract.image_to_string(img).strip()
        camera.stop_preview()
        print(text)
        if len(text) != 0:
            pubnub.publish().channel('Reg_No_Push').message(text).should_store(True).use_post(True).async(my_publish_callback)
            break
GPIO.cleanup()
