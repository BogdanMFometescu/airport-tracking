from requests.exceptions import RequestException
import sqlalchemy.exc
from fastapi import APIRouter, HTTPException, Depends
from src.models.schedule import Schedule, ScheduleBaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.storage.json_storage import JsonStorage
from typing import List

from src.storage.utils import get_database_url

engine = create_engine(get_database_url())
storage = JsonStorage()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.bind = engine
Base.metadata.create_all(engine)

schedule_router_api = APIRouter(prefix='/api/schedule', tags=['api/schedule'])


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
        db_schedule = db.query(ScheduleBaseModel).filter(ScheduleBaseModel.dep_iata == iata_code).first()
        if db_schedule:
            return [Schedule.from_orm(db_schedule)]

    except sqlalchemy.exc.SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        api_schedule = storage.get_airport_schedule(iata_code)
        if api_schedule:
            saved_schedule = storage.save_schedule_details_to_db(api_schedule, db)
            return [Schedule.from_orm(saved_schedule)]
    except RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))
    raise HTTPException(status_code=404, detail='Schedule not found')
