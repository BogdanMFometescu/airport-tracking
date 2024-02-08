from requests.exceptions import RequestException
import sqlalchemy.exc
from fastapi import APIRouter, HTTPException, Depends
from src.models.airplane import AirplaneBaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.storage.utils import get_database_url
from src.storage.json_storage import JsonStorage

storage = JsonStorage()

engine = create_engine(get_database_url())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.bind = engine
Base.metadata.create_all(engine)

airplane_router_api = APIRouter(prefix="/api/airplane", tags=["api/airplane"])


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
        api_airplanes = storage.get_airplane_details()
        if api_airplanes:
            saved_airplanes = storage.save_airplane_details_to_db(api_airplanes, db)
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
