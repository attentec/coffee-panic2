from threading import Timer
from serial.tools import list_ports
from datetime import datetime
from zoneinfo import ZoneInfo
import serial
import time
import boto3

MAX_WEIGHT_G = 2000.0
CUTOFF_WEIGHT_G = 10.0
OFFICE_HOUR_START_H = 7
OFFICE_HOUR_END_H = 18

# Modify this to fit the connected port on your Pi
arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)

port = list(list_ports.comports())
for p in port:
    print(p.device)

def arduino_write(x):
    arduino.write(str.encode(str(x)))
    time.sleep(0.05)
    data = arduino.readline()
    print("Arduino response: " + str(data))


def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

session = boto3.Session()
def create_page_iterator():
    global session, query_client, paginator
    query_client = session.client('timestream-query')
    paginator = query_client.get_paginator('query')
    return paginator.paginate(
        QueryString=f"SELECT Weight FROM linkaffe.\"kannvikt\" ORDER BY time DESC",
        PaginationConfig={'MaxItems': 1}
    )

def print_scales(percent):
    out_string = "["
    for i in range(0, 100):
        out_string += "█" if i < percent else "-" 
    out_string += "]"
    print(out_string, end='\r')

def read_scales():
    dt = datetime.now(tz = ZoneInfo("Europe/Stockholm"))
    if dt.weekday() >= 5 or dt.hour not in range(OFFICE_HOUR_START_H, OFFICE_HOUR_END_H + 1):
        print(f"Skipping: weekend or outside of office hours ({dt})")
        return
    for page in create_page_iterator():
        for row in page["Rows"]:
            data = row.get("Data")
            weight = float(data[0].get("ScalarValue"))
            percentage_filled = clamp((weight / MAX_WEIGHT_G), 0, 1)
            print("\nPercentage filled: " + str(percentage_filled*100) + "%")
            arduino_write(round(percentage_filled, 3))


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

read_scales()
timer = RepeatTimer(20, read_scales)
timer.start()
