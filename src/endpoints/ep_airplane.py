from fastapi import APIRouter, HTTPException, Depends
from src.models.airplane import Airplane, AirplaneBaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.storage.utils import get_database_url

engine = create_engine(get_database_url())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.bind = engine
Base.metadata.create_all(engine)

airplane_router = APIRouter(prefix="/airplane", tags=["airplane"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@airplane_router.get("/", tags=['airplane'], )
def get_airplanes(db: SessionLocal = Depends(get_db)):
    airplanes = db.query(AirplaneBaseModel).all()
    if airplanes:
        return airplanes
    raise HTTPException(status_code=404, detail="No airplanes in the database")


@airplane_router.get("/{airplane_id}", tags=['airplane'], )
def get_airplane(airplane_id: int, db: SessionLocal = Depends(get_db)):
    airplane = db.query(AirplaneBaseModel).filter(AirplaneBaseModel.id == airplane_id).first()
    if airplane:
        return airplane
    raise HTTPException(status_code=404, detail="No such airplane")


@airplane_router.post("/", tags=['airplane'], )
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


@airplane_router.put("/{airplane_id}", tags=['airplane'], )
def update_airplane(airplane_id: int, airplane: Airplane, db: SessionLocal = Depends(get_db)):
    updated_airplane = db.query(AirplaneBaseModel).filter(AirplaneBaseModel.id == airplane_id).first()
    if updated_airplane:
        for var, value in vars(airplane).items():
            setattr(updated_airplane, var, value) if value else None
    db.commit()
    db.refresh(updated_airplane)
    return updated_airplane


@airplane_router.delete("/{airplane_id}", tags=['airplane'])
def delete_airplane(airplane_id: int, db: SessionLocal = Depends(get_db)):
    deleted_airplane = db.query(AirplaneBaseModel).filter(AirplaneBaseModel.id == airplane_id).first()
    if deleted_airplane is None:
        raise HTTPException(status_code=404, detail='Airplane not found')
    db.delete(deleted_airplane)
    db.commit()
