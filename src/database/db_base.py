from abc import ABC, abstractmethod


class Database(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def save_airport_data(self, data, db):
        raise NotImplementedError('Method save_airport_details_to_db not implemented')

    @abstractmethod
    def save_schedule_data(self, data, db):
        raise NotImplementedError('Method save_schedule_details_to_db not implemented')

    @abstractmethod
    def save_airplane_data(self, data, db):
        raise NotImplementedError('Method save_schedule_details_to_db not implemented')

    @staticmethod
    def get_database_url():
        raise NotImplementedError('Method get_database_url not implemented')
