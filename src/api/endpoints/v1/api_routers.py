from typing import List
import sqlalchemy.exc
from requests.exceptions import RequestException
from fastapi import APIRouter, HTTPException, Depends
from src.models.airplane import AirplaneBaseModel
from src.models.airport import AirportBaseModel, Airport
from src.models.schedule import ScheduleBaseModel, Schedule, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.api.api_calls import ApiCalls
from src.database.db_operations import DBOperations

url = DBOperations.get_database_url()

engine = create_engine(url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.bind = engine
Base.metadata.create_all(engine)

airplane_router_api = APIRouter(prefix="/api/airplane", tags=["api/airplane"])
airport_router_api = APIRouter(prefix='/api/airport', tags=['api/airport'])
schedule_router_api = APIRouter(prefix='/api/schedule', tags=['api/schedule'])

api_call = ApiCalls()
db_action = DBOperations()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@airplane_router_api.get("/", tags=['api/airplane'], )
def get_airplanes(db: SessionLocal = Depends(get_db)):
    try:
        db_airplanes = db.query(AirplaneBaseModel).all()
        if db_airplanes:
            return db_airplanes
    except sqlalchemy.exc.SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    try:
        api_airplanes = api_call.get_airplane_details()
        if api_airplanes:
            saved_airplanes = db_action.save_airplane_data(api_airplanes, db)
            return saved_airplanes
    except RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))
    raise HTTPException(status_code=404, detail='No airplane found in the database or or API request is invalid')


@airplane_router_api.get("/{airplane_id}", tags=['api/airplane'], )
def get_airplane(airplane_id: int, db: SessionLocal = Depends(get_db)):
    airplane = db.query(AirplaneBaseModel).filter(AirplaneBaseModel.id == airplane_id).first()
    if airplane:
        return airplane
    raise HTTPException(status_code=404, detail="No such airplane")


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


@schedule_router_api.get('/', tags=['api/schedule'], )
def get_schedules(db: SessionLocal = Depends(get_db)):
    try:
        db_schedules = db.query(ScheduleBaseModel).all()
        if db_schedules:
            return db_schedules
    except sqlalchemy.exc.SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=404, detail='Schedules not found')


@schedule_router_api.get('/{iata_code}', response_model=List[Schedule], tags=['api/schedule'], )
def get_schedule_details(iata_code: str, db: SessionLocal = Depends(get_db)):
    try:
        db_schedule = db.query(ScheduleBaseModel).filter(ScheduleBaseModel.dep_iata == iata_code).first()
        if db_schedule:
            return [db_schedule]

    except sqlalchemy.exc.SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        api_schedule = api_call.get_airport_schedule(iata_code)
        if api_schedule:
            saved_schedule = db_action.save_schedule_data(api_schedule, db)
            return [saved_schedule]
    except RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))
    raise HTTPException(status_code=404, detail='Schedule not found')
