from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import AWSIoTPythonSDK
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
		self.query_topic = 'stockholm/coffee/query'
		self.query_callback = None

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


	def subscribe_to_coffee_level_queries(self,callback):
		self.query_callback = callback
		#self.AWSIoTMQTTClient.subscribe(self.query_topic, 1, self.coffee_level_query_callback)


	def coffee_level_query_callback(self, client, userdata, encoded_message):
		decoded_message = json.loads(encoded_message.payload.decode('utf-8'))
		if 'request' in decoded_message and decoded_message['request'] == 'coffee_level':
			print('Coffee level query')
			self.query_callback()



	def publish_weight(self, scale_reading):
		self.publish_coffee_message(scale_reading,self.topic)


	def publish_coffee_level_reply(self, scale_reading):
		self.publish_coffee_message(scale_reading,self.query_topic)


	def publish_coffee_message(self, scale_reading, topic):
		message = scale_reading
		message['unit'] = "gram"
		message['time'] = str(datetime.datetime.now())
		messageJson = json.dumps( {'state': {"reported": message } } )
		shadow_minister = self.AWSIoTMQTTClient.createShadowHandlerWithName("AS-RPI", True)
		shadow_minister.shadowUpdate(messageJson, self.shadow_callback, 5 )
