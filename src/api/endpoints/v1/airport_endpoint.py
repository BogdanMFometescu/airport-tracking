from typing import List
import sqlalchemy.exc
from requests.exceptions import RequestException
from fastapi import APIRouter, HTTPException, Depends
from src.models.airport import Airport
from src.api.api_calls import ApiCalls
from src.database.db_operations import DBOperations
from src.database.db_config import get_db, get_engine
from src.database.db_schema import AirportBaseModel

airport_router_api = APIRouter(prefix='/api/airport', tags=['api/airport'])

api_call = ApiCalls()
db_action = DBOperations()
SessionLocal = get_engine()


@airport_router_api.get('/', tags=['api/airport'], )
def get_airports(db: SessionLocal = Depends(get_db)):
    try:
        db_airports = db.query(AirportBaseModel).all()
        if db_airports:
            return db_airports
    except sqlalchemy.exc.SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=404, detail='No airplane found in the database ')


@airport_router_api.get('/{iata_code}', response_model=List[Airport], tags=['api/airport'], )
def get_airport(iata_code: str, db: SessionLocal = Depends(get_db)):
    try:
        db_airport = db.query(AirportBaseModel).filter(AirportBaseModel.iata_code == iata_code).first()
        if db_airport:
            return [db_airport]

    except sqlalchemy.exc.SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    try:
        api_airport = api_call.get_airport_details(iata_code)
        if api_airport:
            saved_airport = db_action.save_airport_data(api_airport, db)
            return [saved_airport]

    except RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))

    raise HTTPException(status_code=404, detail='Airport not found in the database or API request is invalid')


@airport_router_api.post('/', tags=['api/airport'])
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


@airport_router_api.put('/{airport_id}', tags=['api/airport'], )
def update_airport(airport_id: int, airport: Airport, db: SessionLocal = Depends(get_db)):
    updated_airport = db.query(AirportBaseModel).filter(AirportBaseModel.id == airport_id).first()
    if updated_airport is None:
        raise HTTPException(status_code=404, detail='Invalid IATA_CODE')
    for var, value in vars(airport).items():
        setattr(updated_airport, var, value) if value else None
    db.commit()
    db.refresh(updated_airport)
    return updated_airport


@airport_router_api.delete('/{airport_id}', )
def delete_airport(airport_id: int, db: SessionLocal = Depends(get_db)):
    deleted_airport = db.query(AirportBaseModel).filter(AirportBaseModel.id == airport_id).first()
    if deleted_airport is None:
        raise HTTPException(status_code=404, detail='Invalid IATA_CODE')
    db.delete(deleted_airport)
    db.commit()
