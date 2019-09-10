from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import json
import datetime
from time import sleep
from signal import pause


class AwsClient:	
	
	def __init__(self):
		host = "a4e3a80el53pq-ats.iot.eu-central-1.amazonaws.com"
		rootCAPath = "cert/AmazonRootCA1.pem"
		certificatePath = "cert/AS-RPI.cert.pem"
		privateKeyPath = "cert/AS-RPI.private.key"
		port = 8883
		clientId = "coffee-panic"
		self.topic = "stockholm/coffee"
		
		# Configure logging
		logger = logging.getLogger("AWSIoTPythonSDK.core")
		logger.setLevel(logging.DEBUG)
		streamHandler = logging.StreamHandler()
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		streamHandler.setFormatter(formatter)
		logger.addHandler(streamHandler)
		
		# Init AWSIoTMQTTClient
		Client = AWSIoTMQTTClient(clientId)
		Client.configureEndpoint(host, port)
		Client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
		
		# AWSIoTMQTTClient connection configuration
		Client.configureAutoReconnectBackoffTime(1, 32, 20)
		Client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
		Client.configureDrainingFrequency(2)  # Draining: 2 Hz
		Client.configureConnectDisconnectTimeout(10)  # 10 sec
		Client.configureMQTTOperationTimeout(5)  # 5 sec
		
		# Connect and subscribe to AWS IoT
		Client.connect()
		Client.subscribe(self.topic, 1, self.customCallback)
		
		self.AWSIoTMQTTClient = Client
	

	def customCallback(self, client, userdata, message):
		print("Received a new message: ")
		print(message.payload)
		print("from topic: ")
		print(message.topic)
		print("--------------\n\n")
	
	def publish_weight(self, scale_reading):
		message = scale_reading
		message['unit'] = "gram"
		message['time'] = str(datetime.datetime.now())
		messageJson = json.dumps(message) 
		self.AWSIoTMQTTClient.publish(self.topic, messageJson, 1)
		print('Published topic %s: %s\n' % (self.topic, messageJson))
