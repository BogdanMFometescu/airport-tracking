from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String,Float,DateTime

Base = declarative_base()


class AirplaneBaseModel(Base):
    __tablename__ = "airplane"
    id = Column(Integer, primary_key=True, unique=True, index=True)
    iata = Column(String)
    model = Column(String)
    manufacturer = Column(String)


class AirportBaseModel(Base):
    __tablename__ = 'airport'
    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String)
    iata_code = Column(String)
    icao_code = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    country_code = Column(String)


class ScheduleBaseModel(Base):
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True, unique=True, index=True)
    dep_iata = Column(String)
    flight_number = Column(Integer)
    dep_time = Column(DateTime)
    arr_iata = Column(String)
    arr_time = Column(DateTime)
    duration = Column(Integer)
    status = Column(String)
