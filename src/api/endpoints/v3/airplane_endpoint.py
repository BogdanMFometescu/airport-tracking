import sqlalchemy.exc
from requests.exceptions import RequestException
from fastapi import APIRouter, HTTPException, Depends
from src.models.airplane import Airplane
from src.database.db_schema import AirplaneBaseModel
from src.api.api_calls import ApiCalls
from src.database.db_operations import DBOperations
from src.database.db_config import get_db, get_engine

airplane_router_api = APIRouter(prefix="/api/airplane", tags=["api/airplane"])

api_call = ApiCalls()
db_action = DBOperations()
SessionLocal = get_engine()


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
