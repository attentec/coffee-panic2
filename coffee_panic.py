import usb.core
import usb.util
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
	sleep(10)
