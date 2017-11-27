import time
import RPi.GPIO as GPIO
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pubnubConf = PNConfiguration()

pubnubConf.subscribe_key = 'sub-c-1aa69146-117c-11e7-9faf-0619f8945a4f'
pubnubConf.publish_key = 'pub-c-a2c67d8e-1b26-4e00-878b-8b74a6ef3393'
pubnubConf.ssl = False
pubnub = PubNub(pubnubConf)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
GPIO.setwarnings(False)

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

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
 
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost
 
        elif status.category == PNStatusCategory.PNConnectedCategory:
            pass
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            #pubnub.publish().channel("awesomeChannel").message("hello!!").async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.
 
    def message(self, pubnub, message):
        print(message.message)
        if message.message == "1":
             GPIO.output(16, GPIO.HIGH)
             time.sleep(5)
             #GPIO.output(8, GPIO.LOW)
             GPIO.output(16, GPIO.LOW)
        pass  # Handle new message stored in message.message



pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('entry-exit').execute()
