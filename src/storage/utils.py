import os
import json


def save_airport_info(data, relative_path=''):
    base_directory = os.path.dirname(os.path.abspath(__file__))
    file_name = 'json_files/airport.json'
    filepath = os.path.join(base_directory, relative_path, file_name)
    with open(filepath, 'w') as file:
        json.dump(data, file)


def save_schedule_info(data, relative_path=''):
    base_directory = os.path.dirname(os.path.abspath(__file__))
    file_name = 'json_files/schedule.json'
    filepath = os.path.join(base_directory, relative_path, file_name)
    with open(filepath, 'w') as file:
        json.dump(data, file)


def save_airplane_info(data, relative_path=''):
    base_directory = os.path.dirname(os.path.abspath(__file__))
    file_name = 'json_files/airplane.json'
    filepath = os.path.join(base_directory, relative_path, file_name)
    with open(filepath, 'w') as file:
        json.dump(data, file)


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
