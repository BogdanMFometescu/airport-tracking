from typing import List
import sqlalchemy.exc
from requests.exceptions import RequestException
from fastapi import APIRouter, HTTPException, Depends
from src.models.airplane import AirplaneBaseModel, Airplane
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


@airplane_router_api.post("/", tags=['api/airplane'], )
def create_airplane(airplane: Airplane, db: SessionLocal = Depends(get_db)):
    new_airplane = AirplaneBaseModel(
        iata=airplane.iata,
        model=airplane.model,
        manufacturer=airplane.manufacturer,
    )
    db.add(new_airplane)
    db.commit()
    db.refresh(new_airplane)
    return new_airplane


@airplane_router_api.put("/{airplane_id}", tags=['api/airplane'], )
def update_airplane(airplane_id: int, airplane: Airplane, db: SessionLocal = Depends(get_db)):
    updated_airplane = db.query(AirplaneBaseModel).filter(AirplaneBaseModel.id == airplane_id).first()
    if updated_airplane:
        for var, value in vars(airplane).items():
            setattr(updated_airplane, var, value) if value else None
    db.commit()
    db.refresh(updated_airplane)
    return updated_airplane


@airplane_router_api.delete("/{airplane_id}", tags=['api/airplane'])
def delete_airplane(airplane_id: int, db: SessionLocal = Depends(get_db)):
    deleted_airplane = db.query(AirplaneBaseModel).filter(AirplaneBaseModel.id == airplane_id).first()
    if deleted_airplane is None:
        raise HTTPException(status_code=404, detail='Airplane not found')
    db.delete(deleted_airplane)
    db.commit()


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


@schedule_router_api.post('/', tags=['api/schedule'], )
def create_schedule(schedule: Schedule, db: SessionLocal = Depends(get_db)):
    new_schedule = ScheduleBaseModel(
        dep_iata=schedule.dep_iata,
        flight_number=schedule.flight_number,
        dep_time=schedule.dep_time,
        arr_iata=schedule.arr_iata,
        arr_time=schedule.arr_time,
        duration=schedule.duration,
        status=schedule.status,

    )
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule


@schedule_router_api.put('/{item_id}', tags=['api/schedule'], )
def update_schedule(item_id: int, schedule: Schedule, db: SessionLocal = Depends(get_db)):
    updated_schedule = db.query(ScheduleBaseModel).filter(ScheduleBaseModel.id == item_id).first()
    if updated_schedule is None:
        raise HTTPException(status_code=404, detail='Schedule not found')
    for var, value in vars(schedule).items():
        setattr(updated_schedule, var, value) if value else None
    db.commit()
    db.refresh(updated_schedule)
    return updated_schedule


@schedule_router_api.delete('/{item_id}', tags=['api/schedule'])
def delete_schedule(item_id: int, db: SessionLocal = Depends(get_db)):
    deleted_schedule = db.query(ScheduleBaseModel).filter(ScheduleBaseModel.id == item_id).first()
    if deleted_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    db.delete(deleted_schedule)
    db.commit()
