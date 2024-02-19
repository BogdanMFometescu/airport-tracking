from typing import List
import sqlalchemy.exc
from requests.exceptions import RequestException
from fastapi import APIRouter, HTTPException, Depends
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

schedule_router_api = APIRouter(prefix='/api/schedule', tags=['api/schedule'])

api_call = ApiCalls()
db_action = DBOperations()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
        db_schedule = db.query(ScheduleBaseModel).filter(ScheduleBaseModel.dep_iata == iata_code).all()
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
