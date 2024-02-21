from sqlalchemy import create_engine
from src.database.db_operations import DBOperations
from src.database.db_schema import Base
from sqlalchemy.orm import sessionmaker


def get_engine():
    url = DBOperations.get_database_url()
    engine = create_engine(url)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def get_db():
    db = get_engine()
    try:
        yield db
    finally:
        db.close()
