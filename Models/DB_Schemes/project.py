from pydantic import BaseModel ,Field, validator
from typing import Optional
from bson.objectid import ObjectId


class Project (BaseModel) :
    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id :str = Field(...,min_length=1)

    @validator("project_id")
    def validate_project_id (cls, value):
        if not value .isalnum() :
            raise ValueError("project id must be alphanumeric")
        

        return value
    

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True

    @classmethod
<<<<<<< HEAD
    def get_indexes(cls) :
        return[
            {
                "key" : [("project_id,1")],
                "name" : "project_id_index_1",
                "uniqe" : True
            }
        ]
=======
    def get_indexes (cls ):
        pass


>>>>>>> 7187f73183e524281dc5ec5a762a962a71e75747
