import usb.core
import usb.util
import config
from time import sleep
import threading
from scale import Scale
from AwsClient import AwsClient
from ArduinoClient import ArduinoClient
from WebsocketServer import WebsocketServer
from RestApiClient import RestApiClient

PUBLISH_WEIGHT_INTERVAL = 20
READ_WEIGHT_INTERVAL = 5

publish_counter = 0

if not config.config_file_exists():
    config.create_config_file()

dymo_scale = Scale()
#aws_client = AwsClient()
api_service = RestApiClient()
#websocket = WebsocketServer()
#arduino_client = ArduinoClient()

while True:
    scale_reading = dymo_scale.read_scale()
    print(scale_reading)
    #arduino_client.publish_weight(scale_reading)

    if publish_counter * READ_WEIGHT_INTERVAL >= PUBLISH_WEIGHT_INTERVAL:
        publish_counter = 1
        #websocket.broadcast(scale_reading)
        #aws_client.publish_weight(scale_reading)
        api_service.publish_weight(scale_reading)
    else:
        publish_counter += 1

    sleep(READ_WEIGHT_INTERVAL)
