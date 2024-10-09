import requests

class ApiService:
    def __init__(self):
        self.url = "https://linkaffe.azurewebsites.net"
    
    def get_state(self):
        response = requests.get(self.url)
        return response.json()

    def post_state(self, state):
        response = requests.post(self.url, json=state)
        return response.status_code