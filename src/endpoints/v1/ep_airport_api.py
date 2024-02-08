from requests.exceptions import RequestException
import sqlalchemy.exc
from fastapi import APIRouter, HTTPException, Depends
from src.models.airport import AirportBaseModel, Base, Airport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.storage.json_storage import JsonStorage
from src.storage.utils import get_database_url
from typing import List

engine = create_engine(get_database_url())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.bind = engine
Base.metadata.create_all(engine)

storage = JsonStorage()

airport_router_api = APIRouter(prefix='/api/airport', tags=['api/airport'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@airport_router_api.get('/', tags=['api/airport'], )
def get_airports(db: SessionLocal = Depends(get_db)):
    try:
        db_airports = db.query(AirportBaseModel).all()
        if db_airports:
            return db_airports
    except sqlalchemy.exc.SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=404, detail='No airplane found in the database ')


# Get airport from DB or API based on IATA code
@airport_router_api.get('/{iata_code}', response_model=List[Airport], tags=['api/airport'], )
def get_airport(iata_code: str, db: SessionLocal = Depends(get_db)):
    try:
        db_airport = db.query(AirportBaseModel).filter(AirportBaseModel.iata_code == iata_code).all()
        if db_airport:
            return [Airport.from_orm(airport) for airport in db_airport]
    except sqlalchemy.exc.SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    try:
        api_airport = storage.get_airport_details(iata_code)
        if api_airport:
            saved_airport = storage.save_airport_details_to_db(api_airport, db)
            return [Airport.from_orm(airport) for airport in saved_airport]
    except RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))

    raise HTTPException(status_code=404, detail='Airport not found in the database or API request is invalid')
