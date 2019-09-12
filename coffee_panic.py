import usb.core
import usb.util
from time import sleep
import threading
from scale import Scale
from AwsClient import AwsClient


dymo_scale = Scale()
aws_client = AwsClient()



def coffee_level_query():
	scale_reading = dymo_scale.read_scale()
	aws_client.publish_coffee_level_reply(scale_reading)

aws_client.subscribe_to_coffee_level_queries(coffee_level_query)


while True:
	scale_reading = dymo_scale.read_scale()
	aws_client.publish_weight(scale_reading)
	print(scale_reading)
	sleep(10)
