import usb.core
import usb.util
from keep_scale_alive import keep_scale_alive
from time import sleep
import threading
from scale import Scale
from AwsClient import AwsClient

dymo_scale = Scale()
aws_client = AwsClient()

while True:
	scale_reading = dymo_scale.read_scale()
	aws_client.publish_weight(scale_reading)
	print(scale_reading)
	sleep(300)
