import os
from .api_base import GetRequests
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('AIRLAB_API_KEY')


class ApiCalls(GetRequests):
    def __init__(self):
        self.api_base = f'https://airlabs.co/api/v9'
        super().__init__()

    def get_airplane_details(self):
        api_result = requests.get(f'{self.api_base}/fleets?api_key={API_KEY}')
        api_response = api_result.json()
        airplane_data = api_response['response']
        filtered_data = []

        for airplane in airplane_data:
            filtered_info = {}
            keys = ['iata', 'model', 'manufacturer', ]
            for key in keys:
                if airplane.get(key) is not None:
                    filtered_info[key] = airplane.get(key)
            if filtered_info:
                filtered_data.append(filtered_info)
        return filtered_data

    def get_airport_details(self, iata_code: str):
        api_result = requests.get(f'{self.api_base}/airports?iata_code={iata_code}&api_key={API_KEY}')
        api_response = api_result.json()
        data = api_response['response']
        return data

    def get_airport_schedule(self, iata_code: str):
        api_result = requests.get(f'{self.api_base}/schedules?dep_iata={iata_code}&api_key={API_KEY}')
        api_response = api_result.json()
        flight_data = api_response['response']
        filtered_data = []
        for flight in flight_data:
            filtered_info = {}
            keys = ['dep_iata',
                    'flight_number',
                    'dep_time',
                    'arr_iata',
                    'arr_time',
                    'duration',
                    'status']
            for key in keys:
                if flight.get(key) is not None:
                    filtered_info[key] = flight.get(key)
            if filtered_info:
                filtered_data.append(filtered_info)
        return filtered_data
