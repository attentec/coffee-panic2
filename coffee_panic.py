import usb.core
import usb.util
import config
from time import sleep
import threading
from scale import Scale
from AwsClient import AwsClient
from ArduinoClient import ArduinoClient

PUBLISH_WEIGHT_INTERVAL = 10
READ_WEIGHT_INTERVAL = 2

publish_counter = 0

if not config.config_file_exists():
	config.create_config_file()

dymo_scale = Scale()
aws_client = AwsClient()
arduino_client = ArduinoClient()

while True:
	scale_reading = dymo_scale.read_scale()
	print(scale_reading)
	arduino_client.publish_weight(scale_reading)

	if publish_counter * READ_WEIGHT_INTERVAL >= PUBLISH_WEIGHT_INTERVAL:
		publish_counter = 0
		aws_client.publish_weight(scale_reading)
	else:
		publish_counter += 1

	sleep(READ_WEIGHT_INTERVAL)
