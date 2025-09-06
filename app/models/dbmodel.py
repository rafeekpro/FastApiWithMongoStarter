from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from .rwmodel import RWModel


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, _):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler):
        schema.update(type="string")
        return schema


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")


class DBModelMixin(RWModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
