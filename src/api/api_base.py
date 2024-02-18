from abc import abstractmethod, ABC


class GetRequests(ABC):
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

