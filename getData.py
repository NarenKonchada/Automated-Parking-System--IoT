
import time
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

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

message = 'hello'
#message = urlencode(message)
while True:
    pubnub.publish().channel('awesomeChannel').message(message).should_store(True).use_post(True).async(my_publish_callback)
    time.sleep(1)
