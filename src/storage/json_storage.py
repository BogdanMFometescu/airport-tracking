import os
from .base import Storage
import requests
from sqlalchemy.orm import Session
from src.models.airport import AirportBaseModel
from src.models.schedule import ScheduleBaseModel
from src.models.airplane import AirplaneBaseModel

API_KEY = os.environ.get('AIRLAB_API_KEY')


class JsonStorage(Storage):
    def __init__(self):
        super().__init__()

    def get_airplane_details(self):
        api_base = f'https://airlabs.co/api/v9/fleets?api_key={API_KEY}'
        api_result = requests.get(api_base)
        api_response = api_result.json()
        airplane_data = api_response['response']
        filtered_data = []

        for airplane in airplane_data:
            filtered_info = {}
            keys = ['iata', 'model', 'manufacturer', 'built', 'age']
            for key in keys:
                if airplane.get(key) is not None:
                    filtered_info[key] = airplane.get(key)
            if filtered_info:
                filtered_data.append(filtered_info)
        return filtered_data

    def get_airport_details(self, iata_code: str):
        api_base = f'https://airlabs.co/api/v9/airports?iata_code={iata_code}&api_key={API_KEY}'
        api_result = requests.get(api_base)
        api_response = api_result.json()
        data = api_response['response']
        return data

    def get_airport_schedule(self, iata_code: str):
        api_base = f'https://airlabs.co/api/v9/schedules?dep_iata={iata_code}&api_key={API_KEY}'
        api_result = requests.get(api_base)
        api_response = api_result.json()
        flight_data = api_response['response']
        filtered_data = []
        for flight in flight_data:
            filtered_info = {}
            keys = ['dep_iata',
                    'flight_number',
                    'dep_terminal',
                    'dep_time',
                    'arr_iata',
                    'arr_terminal',
                    'arr_time',
                    'duration',
                    'status']
            for key in keys:
                if flight.get(key) is not None:
                    filtered_info[key] = flight.get(key)
            if filtered_info:
                filtered_data.append(filtered_info)
        return filtered_data

    def save_airport_details_to_db(self, data: list, db: Session):
        airports = []
        for airport_data in data:
            existing_airport = db.query(AirportBaseModel).filter(
                AirportBaseModel.iata_code == airport_data['iata_code']).first()
            if existing_airport is None:
                airport = AirportBaseModel(
                    name=airport_data['name'],
                    iata_code=airport_data['iata_code'],
                    icao_code=airport_data['icao_code'],
                    lat=airport_data['lat'],
                    lng=airport_data['lng'],
                    country_code=airport_data['country_code'],
                )
                airports.append(airport)
                db.add(airport)
        db.commit()
        return airports

    def save_schedule_details_to_db(self, data: list, db: Session):
        schedules = []
        for schedule_data in data:
            existing_schedule = db.query(ScheduleBaseModel).filter(
                ScheduleBaseModel.dep_iata == schedule_data['dep_iata']).first()
            if existing_schedule is None:
                schedule = ScheduleBaseModel(
                    dep_iata=schedule_data['dep_iata'],
                    flight_number=schedule_data['flight_number'],
                    dep_time=schedule_data['dep_time'],
                    arr_iata=schedule_data['arr_iata'],
                    arr_time=schedule_data['arr_time'],
                    duration=schedule_data['duration'],
                    status=schedule_data['status'],
                )
                schedules.append(schedule)
                db.add(schedule)
        db.commit()
        return schedules

    def save_airplane_details_to_db(self, data: list, db: Session):
        airplanes = []
        for airplane_data in data:
            existing_airplane = db.query(AirplaneBaseModel).filter(
                AirplaneBaseModel.iata == airplane_data['iata']).first()
            if existing_airplane is None:
                airplane = AirplaneBaseModel(
                    iata=airplane_data['iata'],
                    model=airplane_data['model'],
                    manufacturer=airplane_data['manufacturer'],

                )
                airplanes.append(airplane)
                db.add(airplane)
        db.commit()
        return airplanes
