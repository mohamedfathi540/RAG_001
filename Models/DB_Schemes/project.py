from pydantic import BaseModel ,Field, validator
from typing import Optional
from bson.objectid import ObjectId


class project (BaseModel) :
    id :Optional [ObjectId] = Field(alias='_id')
    project_id :str = Field(...,min_length=1)

    @validator("project_id")
    def validate_project_id (cls, value):
        if not value .isalnum() :
            raise ValueError("project id must be alphanumeric")
        

        return value
    

    class Config() :
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
