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
		certificatePath, privateKeyPath = self._get_cert_files()
		settings =  self._get_settings()
		host = settings['host_name']
		rootCAPath = "cert/AmazonRootCA1.pem"
		port = 8883
		clientId = "coffee-panic-client"

		# Init AWSIoTMQTTClient
		client = AWSIoTMQTTShadowClient(clientId)
		client.configureEndpoint(host, port)
		client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

		# AWSIoTMQTTClient connection configuration
		client.configureAutoReconnectBackoffTime(1, 32, 20)
		client.configureConnectDisconnectTimeout(10)  # 10 sec
		client.configureMQTTOperationTimeout(5)  # 5 sec

		# Connect to AWS IoT
		client.connect()

		self.shadow_handler = client.createShadowHandlerWithName(settings['thing_name'], True)

	def _get_settings(self):
		with open('./settings.conf') as config_file:
			settings = json.loads(config_file.read())
			return settings


	def _get_cert_files(self):
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
		return (certificatePath, privateKeyPath)


	def publish_weight(self, scale_reading):
		self.publish_coffee_message(scale_reading)


	def shadow_callback(self, *args):
		pass

	def publish_coffee_message(self, scale_reading):
		message = scale_reading
		message['unit'] = "gram"
		message['time'] = str(datetime.datetime.now())
		messageJson = json.dumps( {'state': {"reported": message } } )
		self.shadow_handler.shadowUpdate(messageJson, self.shadow_callback, 5 )
