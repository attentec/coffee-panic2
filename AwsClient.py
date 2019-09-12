from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import AWSIoTPythonSDK
import logging
import time
import json
import datetime
import os
import sys
from time import sleep
from signal import pause


class AwsClient:

	def __init__(self):
		certificatePath = None
		privateKeyPath = None
		certificate_directory = os.listdir('./cert')
		for file in certificate_directory:
			if file.endswith('pem.crt'):
				certificatePath = 'cert/' + file
			elif file.endswith('.pem.key'):
				privateKeyPath = 'cert/' + file

		if not privateKeyPath or not certificatePath:
			sys.exit("You need to add a certificate and private key file to the cert directory\n"
				+"Certificate files can be generated at in AWS IoT")

		host = "a4e3a80el53pq-ats.iot.eu-central-1.amazonaws.com"
		rootCAPath = "cert/AmazonRootCA1.pem"
		port = 8883
		clientId = "coffee-panic"

		# Init AWSIoTMQTTClient
		Client = AWSIoTMQTTShadowClient(clientId)
		Client.configureEndpoint(host, port)
		Client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

		# AWSIoTMQTTClient connection configuration
		Client.configureAutoReconnectBackoffTime(1, 32, 20)
		Client.configureConnectDisconnectTimeout(10)  # 10 sec
		Client.configureMQTTOperationTimeout(5)  # 5 sec

		# Connect to AWS IoT
		Client.connect()

		self.AWSIoTMQTTClient = Client


	def publish_weight(self, scale_reading):
		self.publish_coffee_message(scale_reading,self.topic)


	def shadow_callback(self, *args):
		pass

	def publish_coffee_message(self, scale_reading, topic):
		message = scale_reading
		message['unit'] = "gram"
		message['time'] = str(datetime.datetime.now())
		messageJson = json.dumps( {'state': {"reported": message } } )
		shadow_minister = self.AWSIoTMQTTClient.createShadowHandlerWithName("Coffee-Panic-RPI", True)
		shadow_minister.shadowUpdate(messageJson, self.shadow_callback, 5 )
