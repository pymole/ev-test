import datetime
from typing import Literal

from pydantic import BaseModel


class MarkCreate(BaseModel):
    datetime: datetime.datetime
    payload: int


class Command(BaseModel):
    id: int
    datetime: datetime.datetime
    status: Literal['up', 'down']

    class Config:
        orm_mode = True


class SensorBase(BaseModel):
    name: str


class SensorCreate(SensorBase):
    password: str


class Sensor(SensorBase):
    id: int

    class Config:
        orm_mode = True
