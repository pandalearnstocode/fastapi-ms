from sqlalchemy.orm import Session

import models, schemas
import pandas as pd


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_dataset_by_hash(db: Session, dataset_id: str):
    return db.query(models.DatasetSchema).filter(models.DatasetSchema.dataset_id == dataset_id).first()

def create_dataset_schema(db: Session, payload: schemas.DatasetSchemaCreate):
    db_dataset_schema = models.DatasetSchema(
        dataset_id=payload.dataset_id,
        dataset_filename=payload.dataset_filename,
        dataset_table=payload.dataset_table,
        dataset_schema=payload.dataset_schema,
    )
    db.add(db_dataset_schema)
    db.commit()
    db.refresh(db_dataset_schema)
    return db_dataset_schema
