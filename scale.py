import RPi.GPIO as GPIO
import usb.core
import usb.util
from time import sleep
import time
import threading
import sys
import sched
import os


class Scale:

	def __init__(self):
		self.DATA_MODE_GRAMS = 2
		self.DATA_MODE_OUNCES = 11
		self.VENDOR_ID = 0x0922
		self.PRODUCT_ID = 0x8003
		self.UNIT_BUTTON_PIN = 12
		self.POWER_BUTTON_PIN = 8
		self.UNIT_BUTTON_PRESS_INTERVAL = 60
		self._init_scale_gpio_pins()
		self._start_scale()
		self._keep_scale_alive()
		self._init_scale_usb_connection()


	def _init_scale_gpio_pins(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.UNIT_BUTTON_PIN,GPIO.OUT)
		GPIO.setup(self.POWER_BUTTON_PIN,GPIO.OUT)


	def _press_button(self,pin_number):
		GPIO.output(pin_number,GPIO.HIGH)
		sleep(0.2)
		GPIO.output(pin_number,GPIO.LOW)


	def _press_button_twice(self,pin_number):
		self._press_button(pin_number)
		sleep(0.5)
		self._press_button(pin_number)


	def _start_scale(self):
		# button is pressed twice to restart the scale if it was already on
		self._press_button_twice(self.POWER_BUTTON_PIN)
		sleep(3) # wait for scale to start


	def _press_and_schedule_unit_button(self):
		self._press_button_twice(self.UNIT_BUTTON_PIN)
		self.keep_alive_scheduler.enter(120, 1, self._press_and_schedule_unit_button)


	def _keep_scale_alive(self):
		self.child_pid = os.fork()
		if self.child_pid == 0:
			self.keep_alive_scheduler = sched.scheduler(time.time, sleep)
			self.keep_alive_scheduler.enter(120, 1, self._press_and_schedule_unit_button)
			self.keep_alive_scheduler.run()


	def _init_scale_usb_connection(self):
		self.device = usb.core.find(idVendor=self.VENDOR_ID,
			                        idProduct=self.PRODUCT_ID)

		if self.device.is_kernel_driver_active(0):
			self.device.detach_kernel_driver(0)

		self.device.set_configuration()

		self.endpoint = self.device[0][(0,0)][0]


	def _convert_scale_data(self, scale_data):
		return scale_data[4] + (256 * scale_data[5])


	def _read_scale_usb(self):
		read_attempts = 10
		while read_attempts > 0:
			try:
				return self.device.read(self.endpoint.bEndpointAddress,
                                        self.endpoint.wMaxPacketSize)
			except usb.core.USBError as error:
				read_attempts -= 1
		sys.exit("USB ERROR")


	def read_scale(self):
		scale_reading = self._read_scale_usb()
		if scale_reading[4] == 0:
			weight = 0
		elif scale_reading[2] is self.DATA_MODE_OUNCES:
			ounce_to_gram_factor = 28.3495231
			scaling_factor = 0.1
			weight = ounce_to_gram_factor * (scaling_factor * self._convert_scale_data(scale_reading))
		elif scale_reading[2] is self.DATA_MODE_GRAMS:
			weight = self._convert_scale_data(scale_reading)

		if scale_reading[1] is 2:
			status = "zero"
		elif scale_reading[1] is 4:
			status = "ok"
		elif scale_reading[1] is 5:
			weight = -weight
			status = "minus"
		elif scale_reading[1] is 6:
			status = "overweight"

		return {"weight": weight, "status": status}

