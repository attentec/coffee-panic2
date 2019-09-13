import usb.core
import usb.util
import config
from time import sleep
import threading
from scale import Scale
from AwsClient import AwsClient

PUBLISH_WEIGHT_INTERVAL = 300

if not config.config_file_exists():
	config.create_config_file()

dymo_scale = Scale()
aws_client = AwsClient()

while True:
	scale_reading = dymo_scale.read_scale()
	aws_client.publish_weight(scale_reading)
	print(scale_reading)
	sleep(PUBLISH_WEIGHT_INTERVAL)
