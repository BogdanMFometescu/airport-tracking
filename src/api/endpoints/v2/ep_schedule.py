from fastapi import APIRouter, HTTPException, Depends
from src.models.schedule import Schedule, ScheduleBaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.api.utils import get_database_url

engine = create_engine(get_database_url())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.bind = engine
Base.metadata.create_all(engine)

schedule_router = APIRouter(prefix='/schedule', tags=['schedule'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@schedule_router.get('/', tags=['schedule'], )
def get_schedules(db: SessionLocal = Depends(get_db)):
    schedules = db.query(ScheduleBaseModel).all()
    if schedules:
        return schedules
    raise HTTPException(status_code=404, detail='Schedules not found')


@schedule_router.get('/{dep_iata}', tags=['schedule'], )
def get_schedule_details(dep_iata: str, db: SessionLocal = Depends(get_db)):
    schedule = db.query(ScheduleBaseModel).filter(ScheduleBaseModel.dep_iata == dep_iata).all()
    if schedule:
        return schedule
    raise HTTPException(status_code=404, detail='Schedule not found')


@schedule_router.post('/', tags=['schedule'], )
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


@schedule_router.put('/{item_id}', tags=['schedule'], )
def update_schedule(item_id: int, schedule: Schedule, db: SessionLocal = Depends(get_db)):
    updated_schedule = db.query(ScheduleBaseModel).filter(ScheduleBaseModel.id == item_id).first()
    if updated_schedule is None:
        raise HTTPException(status_code=404, detail='Schedule not found')
    for var, value in vars(schedule).items():
        setattr(updated_schedule, var, value) if value else None
    db.commit()
    db.refresh(updated_schedule)
    return updated_schedule


@schedule_router.delete('/{item_id}', tags=['schedule'])
def delete_schedule(item_id: int, db: SessionLocal = Depends(get_db)):
    deleted_schedule = db.query(ScheduleBaseModel).filter(ScheduleBaseModel.id == item_id).first()
    if deleted_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    db.delete(deleted_schedule)
    db.commit()
