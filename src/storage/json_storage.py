import os
from .base import Storage
import requests
from sqlalchemy.orm import Session
from src.models.airport import AirportBaseModel
from src.models.schedule import ScheduleBaseModel
from src.models.airplane import AirplaneBaseModel
import sqlalchemy.exc

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
        saved_airports = []
        for airport_data in data:
            try:
                required_fields = ['name', 'iata_code', 'icao_code', 'lat', 'lng', 'country_code']
                if not all(field in airport_data for field in required_fields):
                    continue

                existing_airport = db.query(AirportBaseModel).filter(
                    AirportBaseModel.iata_code == airport_data['iata_code']).first()
                if existing_airport is None:
                    airport = AirportBaseModel(**airport_data)
                    db.add(airport)
                    db.commit()
                    saved_airports.append(airport)
            except sqlalchemy.exc.SQLAlchemyError as e:
                f'Some error occurred {e}'
                continue
        return saved_airports

    def save_schedule_details_to_db(self, data: list, db: Session):
        saved_schedules = []
        for schedule_data in data:
            try:
                required_fields = ['dep_iata', 'flight_number', 'dep_time', 'arr_iata', 'arr_time', 'duration',
                                   'status']
                if not all(field in schedule_data for field in required_fields):
                    continue
                existing_schedule = db.query(ScheduleBaseModel).filter(
                    ScheduleBaseModel.dep_iata == schedule_data['dep_iata'],
                    ScheduleBaseModel.flight_number == schedule_data['flight_number']).first()
                if existing_schedule is None:
                    schedule = ScheduleBaseModel(**schedule_data)
                    db.add(schedule)
                    db.commit()
                    saved_schedules.append(schedule)
            except sqlalchemy.exc.SQLAlchemyError as e:
                f'Some error occurred {e}'
                continue
        return saved_schedules

    def save_airplane_details_to_db(self, data: list, db: Session):
        saved_airplanes = []
        for airplane_data in data:
            try:
                required_fields = ['iata', 'model', 'manufacturer']
                if not all(field in airplane_data for field in required_fields):
                    continue
                existing_airplane = db.query(AirplaneBaseModel).filter(
                    AirplaneBaseModel.iata == airplane_data['iata']).first()
                if existing_airplane is None:
                    airplane = AirplaneBaseModel(**airplane_data)
                    db.add(airplane)
                    db.commit()
                    saved_airplanes.append(airplane)
            except sqlalchemy.exc.SQLAlchemyError as e:
                f'Some error occurred {e}'
                continue
        return saved_airplanes
