from abc import abstractmethod, ABC


class Storage(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_airport_details(self, iata_code):
        raise NotImplementedError('Method get_airport_detail not implemented')

    @abstractmethod
    def get_airport_schedule(self, iata_code):
        raise NotImplementedError('Method get_airport_schedules not implemented')

    @abstractmethod
    def get_airplane_details(self):
        raise NotImplementedError('Method get_airplane_details not implemented')

    @abstractmethod
    def save_airport_details_to_db(self, data, db):
        raise NotImplementedError('Method save_airport_details_to_db not implemented')

    @abstractmethod
    def save_schedule_details_to_db(self, data, db):
        raise NotImplementedError('Method save_schedule_details_to_db not implemented')

    @abstractmethod
    def save_airplane_details_to_db(self, data, db):
        raise NotImplementedError('Method save_schedule_details_to_db not implemented')
