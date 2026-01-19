from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import (DistanceMethodEnums, PgVectorTableSchemeEnums, 
                        PgvectorDistanceMethodEnums, PgvectorIndexTypeEnums)
from sqlalchemy.sql import text as sql_text
import logging
from typing import List, Dict, Any, Optional
from Models.DB_Schemes import RetrivedDocument
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine import Engine
import json, uuid

class PGVectorProvider(VectorDBInterface):
    def __init__(self, db_client ,defualt_vector_size : int = 786
                , distance_method: str = None):
        self.db_client = db_client
        self.defualt_vector_size = defualt_vector_size
        self.distance_method = distance_method
        self.pgvector_table_prefix = PgVectorTableSchemeEnums._PREFIX.value
        self.logger = logging.getLogger("uvicorn")


    async def connect(self):
        try:
            async with self.db_client() as session:
                async with session.begin():
                    await session.execute(sql_text("CREATE EXTENSION IF NOT EXISTS vector"))
                    await session.commit()

        except Exception as e:
            self.logger.error(f"Failed to connect to PGVector DB: {e}")
            raise e


    async def disconnect(self):
        pass
        

    async def is_collection_exists(self, collection_name: str) -> bool:
        try:
            record = None
            async with self.db_client() as session:
                async with session.begin():
                    list_tbl = sql_text('SELECT * FROM pg_tables WHERE tablename = :collection_name')
                    results = await session.execute(list_tbl, {"collection_name": collection_name})
                    record = results.scalar_one_or_none()
            return record is not None

        except Exception as e:
            self.logger.error(f"Failed to check if collection exists: {e}")
            raise e
    

    async def list_all_collections(self) -> List[str]:
        try:
            records = []
            async with self.db_client() as session:
                async with session.begin():
                    list_tbl = sql_text('SELECT tablename FROM pg_tables WHERE tablename LIKE :prefix')
                    results = await session.execute(list_tbl,{"prefix" : self.pgvector_table_prefix})
                    records = results.scalars().all()
            return records   

        except Exception as e:
            self.logger.error(f"Failed to list all collections: {e}")
            raise e


    async def get_collection_info(self, collection_name: str) -> dict:
       async with self.db_client() as session:
               try:
                async with session.begin():
                    table_inf_sql = sql_text('''
                    SELECT schemaname, tablename,tableowner, tablespace, hasindexes
                    FROM pg_tables
                    WHERE table_name = :collection_name
                    ''')
                     
                    count = sql_text(f'SELECT COUNT(*) FROM {collection_name}')
                    table_info = await session.execute(table_inf_sql, {"collection_name": collection_name})
                    record_count = await session.execute(count,{"collection_name": collection_name})

                    table_data = table_info.fetchone()
                    if not table_data:
                        return None

                    return {
                        "table_info": dict(table_data),
                        "record_count": record_count
                    }

                except Exception as e:
                    self.logger.error(f"Failed to get collection info: {e}")
                    raise e


    async def delete_collection(self, collection_name: str):
        try:
            async with self.db_client() as session:
                async with session.begin():
                    delete_tbl = sql_text('DROP TABLE IF EXISTS :collection_name')
                    await session.execute(delete_tbl, {"collection_name": collection_name})
                    await session.commit()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete collection: {e}")
            raise e


    async def create_collection(self, collection_name: str, embedding_size: int, do_reset: bool = False):
        try:
            if do_reset:
                await self.delete_collection(collection_name)
            
            if await self.is_collection_exists(collection_name):
                return False

            cols = PgVectorTableSchemeEnums
        
        create_table_sql = f"""
        CREATE TABLE {collection_name} (
            {cols.ID.value} TEXT PRIMARY KEY,
            {cols.TEXT.value} TEXT,
            {cols.VECTORS.value} vector({embedding_size}),
            {cols.METADATA.value} JSONB,
            {cols.CHUNCK_ID.value} TEXT
        );
        """
        
        index_type = PgvectorIndexTypeEnums.HNSW.value
        opclass = self.opclass_map.get("index", "vector_l2_ops")
        
        create_index_sql = f"""
        CREATE INDEX ON {collection_name} USING {index_type} ({cols.VECTORS.value} {opclass});
        """

        with self.engine.connect() as connection:
            with connection.begin():
                connection.execute(text(create_table_sql))
                connection.execute(text(create_index_sql))
        return True

    def insert_one(self, collection_name: str, 
                   text_content: str, vector: list, 
                   metadata: dict = None, 
                   record_id: str = None):
        if not self.engine:
            self.connect()
        
        cols = PgVectorTableSchemeEnums
        if metadata is None:
            metadata = {}
        
        if record_id is None:
             record_id = str(uuid.uuid4())
             
        # Try to extract chunk_id from metadata if present
        # Note: using 'chunk_id' key as convention, or maybe 'chunck_id' to match enum name?
        # I'll check both.
        chunk_id_val = metadata.get("chunk_id") or metadata.get("chunck_id")
             
        sql = text(f"""
            INSERT INTO {collection_name} 
            ({cols.ID.value}, {cols.TEXT.value}, {cols.VECTORS.value}, {cols.METADATA.value}, {cols.CHUNCK_ID.value})
            VALUES (:id, :text, :vector, :metadata, :chunk_id)
        """)
        
        try:
            with self.engine.connect() as connection:
                connection.execute(sql, {
                    "id": record_id,
                    "text": text_content,
                    "vector": str(vector),
                    "metadata": json.dumps(metadata),
                    "chunk_id": chunk_id_val
                })
                connection.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error inserting one record: {e}")
            return False

    def insert_many(self, collection_name: str, 
                    texts: list, vectors: list, 
                    metadata: list = None, 
                    record_ids: list = None, batch_size: int = 50):
        if not self.engine:
            self.connect()
            
        cols = PgVectorTableSchemeEnums
        if metadata is None:
            metadata = [{} for _ in texts]
        if record_ids is None:
            record_ids = [str(uuid.uuid4()) for _ in texts]

        data = []
        for i in range(len(texts)):
            meta = metadata[i] if i < len(metadata) else {}
            chunk_id_val = meta.get("chunk_id") or meta.get("chunck_id")
            
            data.append({
                "id": record_ids[i],
                "text": texts[i],
                "vector": str(vectors[i]),
                "metadata": json.dumps(meta),
                "chunk_id": chunk_id_val
            })
            
        sql = text(f"""
            INSERT INTO {collection_name} 
            ({cols.ID.value}, {cols.TEXT.value}, {cols.VECTORS.value}, {cols.METADATA.value}, {cols.CHUNCK_ID.value})
            VALUES (:id, :text, :vector, :metadata, :chunk_id)
        """)

        try:
            with self.engine.connect() as connection:
                for i in range(0, len(data), batch_size):
                    batch = data[i:i+batch_size]
                    connection.execute(sql, batch)
                connection.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error inserting many records: {e}")
            return False

    def search_by_vector(self, collection_name: str, vector: list, limit: int = 5) -> List[RetrivedDocument]:
        if not self.engine:
            self.connect()
            
        cols = PgVectorTableSchemeEnums
        operator = self.operator_map.get("search", "<->")
        
        sql = text(f"""
            SELECT {cols.TEXT.value}, {cols.VECTORS.value} {operator} :vector as score
            FROM {collection_name}
            ORDER BY score ASC
            LIMIT :limit
        """)
        
        try:
            with self.engine.connect() as connection:
                result = connection.execute(sql, {"vector": str(vector), "limit": limit})
                rows = result.fetchall()
                
            documents = []
            for row in rows:
                txt = row[0]
                score = row[1]
                documents.append(RetrivedDocument(text=txt, score=score))
            return documents
        except Exception as e:
            self.logger.error(f"Error searching by vector: {e}")
            return []
