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
        from_attributes = True


