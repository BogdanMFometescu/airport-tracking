import os
from .db_base import Database
from src.models.airport import AirportBaseModel
from src.models.schedule import ScheduleBaseModel
from src.models.airplane import AirplaneBaseModel
from sqlalchemy.orm import Session


class DBOperations(Database):
    def __init__(self):
        super().__init__()

    def save_airport_data(self, data: list, db: Session):
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

    def save_schedule_data(self, data: list, db: Session):
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

    def save_airplane_data(self, data: list, db: Session):
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

    @staticmethod
    def get_database_url():
        DB_NAME = os.getenv('DB_NAME')
        DB_USERNAME = os.getenv('DB_USERNAME')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        DB_HOST = os.getenv('DB_HOST')
        DB_PORT = os.getenv('DB_PORT')

        if not all([DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT]):
            raise ValueError("One or more database environment variables are missing.")

        DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        return DATABASE_URL
