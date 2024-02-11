from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from typing import Optional

Base = declarative_base()


class Airplane(BaseModel):
    id: Optional[int] = None
    iata: str
    model: str
    manufacturer: str

    class ConfigDict:
        from_attributes = True


class AirplaneBaseModel(Base):
    __tablename__ = "airplane"
    id = Column(Integer, primary_key=True, unique=True, index=True)
    iata = Column(String)
    model = Column(String)
    manufacturer = Column(String)
