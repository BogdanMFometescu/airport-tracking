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

    class Config:
        from_attributes = True


