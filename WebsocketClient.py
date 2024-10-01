import asyncio
import json
import serial
import websockets

from serial.tools import list_ports
from websockets.client import connect

MAX_WEIGHT_G = 2000.0
CUTOFF_WEIGHT_G = 10.0
OFFICE_HOUR_START_H = 7
OFFICE_HOUR_END_H = 18

# Modify this to fit the connected port on your Pi
# arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)

port = list(list_ports.comports())
for p in port:
    print(p.device)

def arduino_write(x):
    print("Sending: " + str(x))
    #arduino.write(str.encode(str(x)))
    #time.sleep(0.05)
    #data = arduino.readline()
    #print("Arduino response: " + str(data))

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

def process_data(data):
    weight = data["weight"]
    percentage_filled = clamp((weight / MAX_WEIGHT_G), 0, 1)
    print("\nPercentage filled: " + str(percentage_filled*100) + "%")
    arduino_write(round(percentage_filled, 3))

async def setup_websocket():
    uri = "ws://localhost:8000"
    async for websocket in connect(uri):
        try:
            print("Opened connection")
            while True:
                data = json.loads(await websocket.recv())
                print(data)
                process_data(data)
                await websocket.send("ping")
        except websockets.ConnectionClosed:
            continue

asyncio.run(setup_websocket())
