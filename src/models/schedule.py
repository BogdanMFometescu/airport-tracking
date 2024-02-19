from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Schedule(BaseModel):
    id: Optional[int] = None
    dep_iata: str
    flight_number: int
    dep_time: datetime
    arr_iata: str
    arr_time: datetime
    duration: int
    status: str

    class Config:
        orm_mode = True


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
