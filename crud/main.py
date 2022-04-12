from typing import Dict

from fastapi import Depends, FastAPI, HTTPException
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from pydantic import BaseModel
from sqlalchemy import JSON, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from loguru import logger
app = FastAPI()
engine = create_engine("sqlite:///./app.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()


class TaskCreate(BaseModel):
    task_id: str
    task_type: str
    task_status: str
    task_result: Dict


class Task(TaskCreate):
    id: int

    class Config:
        orm_mode = True


class TaskModel(Base):
    __tablename__ = "Taskes"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    task_type = Column(String)
    task_status = Column(String)
    task_result = Column(JSON, nullable=True)


def get_id(db: Session, task_id: str):
    return db.query(TaskModel).filter(TaskModel.task_id == task_id).first()


app = FastAPI()

Base.metadata.create_all(bind=engine)

router = SQLAlchemyCRUDRouter(
    schema=Task,
    create_schema=TaskCreate,
    db_model=TaskModel,
    db=get_db,
    prefix="task",
)

app.include_router(router)


@app.get("/ping")
async def root():
    try:
        with engine.connect() as con:
            con.execute("SELECT 1")
        logger.info('engine is valid')
    except Exception as e:
        logger.info(f'Engine invalid: {str(e)}')
    return {"message": "pong"}


@app.get("/id/{task_id}")
def read_id(task_id: str, db: Session = Depends(get_db)):
    db_task = get_id(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": db_task.id, "task_type": db_task.task_type}
