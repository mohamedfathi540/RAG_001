from .Providers import QdrantDBProvider
from Enums import VectorDBEnums
from Controllers.BaseController import basecontroller



class VectorDBProviderFactory :
    def __init__(self,config : dict):
        self.config = config
        self.base_controller = basecontroller()
    def create (self , provider : str ) :
        if provider == VectorDBEnums.QDRANT.value :
            db_path = self.base_controller.get_database_path(db_name = self.config.VECTOR_DB_PATH)


            return QdrantDBProvider(
                db_path = db_path,
                distancemethod = self.config.QDRANT_DISTANCE_METHOD,
            )
        return None 