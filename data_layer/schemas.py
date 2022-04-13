from typing import List, Optional, Dict

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class DatasetBase(BaseModel):
    dataset_name: str
    dataset_source: str
    dataset_description: str
    dataset_table: str
    dataset_filename: str


class DatasetCreate(DatasetBase):
    dataset_id: str


class Dataset(DatasetBase):
    id: int

    class Config:
        orm_mode = True


class DatasetSchemaCreate(BaseModel):
    dataset_id: str
    dataset_filename: str
    dataset_table: str
    dataset_schema: Dict
