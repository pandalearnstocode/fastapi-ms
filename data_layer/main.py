from typing import List
from io import BytesIO
from fastapi import Depends, FastAPI, HTTPException, File, UploadFile, Body
from sqlalchemy.orm import Session
import pandas as pd
import sqlalchemy
import crud, models, schemas, utils
from database import SessionLocal, engine
import joblib
from fastapi.responses import JSONResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.post("/register_dataset")
async def register_dataset(file: UploadFile = File(...)):
    list_of_valid_files = ["iris","flights","gapminder","mtcars","titanic","wine"]
    file_name_wo_type = file.filename.replace(".csv", "")
    if file.content_type not in ["text/csv"]:
        raise HTTPException(400, detail="Invalid dataset file. Upload csv files only")
    if file_name_wo_type not in list_of_valid_files:
        raise HTTPException(
            400,
            detail="Invalid dataset name. Rename the file to one of the following: {}".format(
                list_of_valid_files
            ),
        )
    contents = await file.read()
    buffer = BytesIO(contents)
    df = pd.read_csv(buffer)
    buffer.close()
    df.to_sql(
        name=file_name_wo_type,
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=100,
        method="multi",
    )
    data_schema = utils.generate_schema(df)
    return {
        "dataset_id": joblib.hash(df, hash_name="sha1"),
        "dataset_filename": file.filename,
        "dataset_table": file_name_wo_type,
        "dataset_schema": data_schema,
    }


@app.post("/dataset")
async def create_dataset(
    payload: schemas.DatasetSchemaCreate, db: Session = Depends(get_db)
):
    db_schema = crud.get_dataset_by_hash(db, dataset_id=payload.dataset_id)
    if db_schema:
        raise HTTPException(status_code=400, detail="Dataset already registered")
    return crud.create_dataset_schema(db=db, payload=payload)


@app.put("/dataset/{dataset_id}", response_model=schemas.DatasetCreate)
async def update_dataset(dataset_id: str, dataset: schemas.DatasetBase):
    return {"dataset_id": dataset_id, **dataset.dict()}
