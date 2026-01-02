from .BaseController import basecontroller
from .ProjectController import projectcontroller
from Models.DB_Schemes import Project
from fastapi import UploadFile
from Models import ResponseSignal
import re
import os



class NLPController (basecontroller) : 

    def __init__(self ,genration_client ,embedding_client ,vectordb_client) :
        super().__init__()
        self.genration_client = genration_client
        self.embedding_client = embedding_client
        self.vectordb_client = vectordb_client  


    def create_collection_name (self , project_id  : str) :
        return f"collection_{project_id}".strip()


    def reset_vector_db_collection (self , project : Project) :
        collection_name = self.create_collection_name(project_id = project.project_id)
        return self.vectordb_client.delete_collection(collection_name = collection_name)

    def get_vector_collection_info ( self , project : Project) :
        collection_name = self.create_collection_name(project_id = project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name = collection_name)
        return collection_info
       