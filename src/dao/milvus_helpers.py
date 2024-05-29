from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import sys
from config import MILVUS_HOST, MILVUS_PORT, MILVUS_COLLECTION, VECTOR_DIMENSION, METRIC_TYPE
from logs import LOGGER


class MilvusHelper:
    def __init__(self):
        # initialize the milvus connection
        try:
            self.collection = None
            connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
            LOGGER.debug(
                f"Successfully connect to Milvus with IP:{MILVUS_HOST,} and PORT:{MILVUS_PORT}")
        except Exception as e:
            LOGGER.error(f"Failed to connect Milvus: {e}")
            sys.exit(1)

    def create_collection(self, collection_name=MILVUS_COLLECTION, dim=VECTOR_DIMENSION):
        # create milvus' data gather collection
        try:
            if not self.has_collection(collection_name):
                field1 = FieldSchema(
                    name="id", dtype=DataType.INT64, descrition="int64", is_primary=True, auto_id=True)
                field2 = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR,
                                     descrition="float vector", dim=dim, is_primary=False)
                schema = CollectionSchema(
                    fields=[field1, field2], description="collection description")
                self.collection = Collection(
                    name=collection_name, schema=schema)
                LOGGER.debug(f"Create Milvus collection: {self.collection}")
                self.create_index(collection_name)
            return "OK"
        except Exception as e:
            LOGGER.error(f"Failed to create collection: {e}")

    def set_collection(self, collection_name=MILVUS_COLLECTION):
        # get the port of operated collection for the current environment
        try:
            if self.has_collection(collection_name):
                self.collection = Collection(name=collection_name)
            else:
                raise Exception(
                    f"There has no collection named:{collection_name}")
        except Exception as e:
            LOGGER.error(f"Error: {e}")

    def has_collection(self, collection_name=MILVUS_COLLECTION):
        try:
            status = utility.has_collection(collection_name)
            print(",,,,,,,,,,,,", status)
            return status
        except Exception as e:
            LOGGER.error(f"Failed to check collection: {e}")

    def insert(self, vectors, collection_name=MILVUS_COLLECTION):
        # insert the designated collection
        try:
            self.set_collection(collection_name)
            data = [vectors]
            mr = self.collection.insert(data)
            ids = mr.primary_keys
            self.collection.load()
            LOGGER.debug(
                f"Insert vectors to Milvus in collection: {collection_name} with {len(vectors)} rows")
            return ids
        except Exception as e:
            LOGGER.error(f"Failed to insert data into Milvus: {e}")

    def delete_entity_by_id(self, ids, collection_name=MILVUS_COLLECTION):
        try:
            delete_count = len(ids)
            self.set_collection(collection_name)
            expr = 'id in '+str(ids)
            success_count = self.collection.delete(expr)
            LOGGER.debug(f"the number of Deleted entity is {success_count}")
        except Exception as e:
            LOGGER.error(f"Failed to insert data into Milvus: {e}")

    def create_index(self, collection_name=MILVUS_COLLECTION):
        # create index for specific collection's embedding
        try:
            self.set_collection(collection_name)
            default_index = {"index_type": "IVF_SQ8",
                             "metric_type": METRIC_TYPE, "params": {"nlist": 16384}}
            status = self.collection.create_index(
                field_name="embedding", index_params=default_index)
            if not status.code:
                LOGGER.debug(
                    f"Successfully create index in collection:{collection_name} with param:{default_index}")
                return status
            else:
                raise Exception(status.message)
        except Exception as e:
            LOGGER.error(f"Failed to create index: {e}")

    def delete_collection(self, collection_name=MILVUS_COLLECTION):
        # delete the designated collection
        try:
            self.set_collection(collection_name)
            self.collection.drop()
            LOGGER.debug("Successfully drop collection!")
            return "ok"
        except Exception as e:
            LOGGER.error(f"Failed to drop collection: {e}")

    def search_vectors(self, vectors, top_k, collection_name=MILVUS_COLLECTION):
        # search for the most similar top_k vector from designated collection
        # The vectors must be included muti vectors' list
        try:
            self.set_collection(collection_name)
            search_params = {"metric_type":  METRIC_TYPE,
                             "params": {"nprobe": 16}}
            res = self.collection.search(
                vectors, anns_field="embedding", param=search_params, limit=top_k)
            print(res[0])
            LOGGER.debug(f"Successfully search in collection: {res}")
            return res
        except Exception as e:
            LOGGER.error(f"Failed to search in Milvus: {e}")

    def search_vectors_by_mid(self, mid, top_k, collection_name=MILVUS_COLLECTION):
        try:
            self.set_collection(collection_name)
            vector = self.collection.query(
                expr=f"id=={mid}",
                output_fields=["id", "embedding"],
                consistency_level="Strong"
            )[0]['embedding']

            res = self.search_vectors([vector], top_k)
            LOGGER.debug(f"Successfully search in collection: {res}")
            return res
        except Exception as e:
            LOGGER.error(f"Failed to search in Milvus: {e}")

    def count(self, collection_name=MILVUS_COLLECTION):
        # count for specific collection
        try:
            self.set_collection(collection_name)
            num = self.collection.num_entities
            LOGGER.debug(
                f"Successfully get the num:{num} of the collection:{collection_name}")
            return num
        except Exception as e:
            LOGGER.error(f"Failed to count vectors in Milvus: {e}")
            sys.exit(1)
