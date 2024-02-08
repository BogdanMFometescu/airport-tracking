from fastapi import APIRouter, HTTPException, Depends
from src.models.airport import Airport, AirportBaseModel, Base
from src.storage.json_storage import JsonStorage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.storage.utils import get_database_url

engine = create_engine(get_database_url())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.bind = engine
Base.metadata.create_all(engine)

storage = JsonStorage()

airport_router = APIRouter(prefix='/airport', tags=['airport'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@airport_router.get('/', tags=['airport'], )
def get_airports(db: SessionLocal = Depends(get_db)):
    airports = db.query(AirportBaseModel).all()
    if airports:
        return airports
    raise HTTPException(status_code=404, detail='No airports found')


# Get airport from DB based on IATA_CODE
@airport_router.get('/{iata_code}', tags=['airport'], )
def get_airport(iata_code: str, db: SessionLocal = Depends(get_db)):
    airport = db.query(AirportBaseModel).filter(AirportBaseModel.iata_code == iata_code).all()
    if airport:
        return airport
    raise HTTPException(status_code=404, detail='Airport not found')


# Create airport (into DB)
@airport_router.post('/', tags=['airport'], )
def create_airport(airport: Airport, db: SessionLocal = Depends(get_db)):
    new_airport = AirportBaseModel(name=airport.name,
                                   iata_code=airport.iata_code,
                                   icao_code=airport.icao_code,
                                   lat=airport.lat,
                                   lng=airport.lng,
                                   country_code=airport.country_code)
    db.add(new_airport)
    db.commit()
    db.refresh(new_airport)
    return new_airport


# Update airport (from DB)

@airport_router.put('/{airport_id}', tags=['airport'], )
def update_airport(airport_id: int, airport: Airport, db: SessionLocal = Depends(get_db)):
    updated_airport = db.query(AirportBaseModel).filter(AirportBaseModel.id == airport_id).first()
    if updated_airport is None:
        raise HTTPException(status_code=404, detail='Invalid IATA_CODE')
    for var, value in vars(airport).items():
        setattr(updated_airport, var, value) if value else None
    db.commit()
    db.refresh(updated_airport)
    return updated_airport


@airport_router.delete('/{airport_id}', )
def delete_airport(airport_id: int, db: SessionLocal = Depends(get_db)):
    deleted_airport = db.query(AirportBaseModel).filter(AirportBaseModel.id == airport_id).first()
    if deleted_airport is None:
        raise HTTPException(status_code=404, detail='Invalid IATA_CODE')
    db.delete(deleted_airport)
    db.commit()
