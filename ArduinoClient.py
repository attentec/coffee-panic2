import serial

class ArduinoClient:

    def __init__(self):
        self.MAX_WEIGHT = 2000
        self.arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)
        self.previous_weight = 0

    def clamp(num, min_value, max_value):
        return max(min(num, max_value), min_value)

    def arduino_write(self, x):
        self.arduino.write(str.encode(str(x)))

    def publish_weight(self, scale_reading):
        weight = scale_reading["weight"]
        if weight != self.previous_weight:
            self.previous_weight = weight
            percentage = weight / self.MAX_WEIGHT
            percentage_filled = max(min(percentage, 1), 0)
            # percentage_filled = self.clamp(percentage, 0, 1)
            self.arduino_write(round(percentage_filled, 3))
