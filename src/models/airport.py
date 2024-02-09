from pydantic import BaseModel
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import declarative_base
from typing import Optional
Base = declarative_base()


class Airport(BaseModel):
    id: Optional[int] = None
    name: str
    iata_code: str
    icao_code: str
    lat: float
    lng: float
    country_code: str

    class Config:
        orm_mode = True
        from_attributes = True


class AirportBaseModel(Base):
    __tablename__ = 'airport'
    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String)
    iata_code = Column(String)
    icao_code = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    country_code = Column(String)
