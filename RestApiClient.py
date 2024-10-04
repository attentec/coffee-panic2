import requests
import time
import json

class RestApiClient:
    def __init__(self):
        self.api_url = "https://linkaffe.azurewebsites.net"
    
    def publish_weight(self, scale_reading):
        data = {"weight": scale_reading["weight"], "timestamp": int(time.time() * 1000)}
        response = requests.post(self.api_url, json=data)
        print("Posted update with response code: " + str(response.status_code))
    
    def get_weight(self):
        response = requests.get(self.api_url)
        print("Got data with response code: " + response.status_code)
        return json.loads(response.json())
        