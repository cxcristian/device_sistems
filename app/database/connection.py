from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# url de la conecion a la base de datos
DATABASE_URL = "sqlite:///./device_systems.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

#base para los modelos
class Base(DeclarativeBase):
    pass

def create_tables():
    Base.metadata.create_all(bind=engine)