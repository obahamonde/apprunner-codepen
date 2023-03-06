from typing import Optional, List
from pydantic import BaseModel, Field
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
from src.config import env
from faunadb.objects import Query


class FaunaModel(BaseModel):
    """Base model for FaunaDB models."""
    @classmethod
    def client(cls) -> FaunaClient:
        """Return a FaunaDB client."""
        return FaunaClient(secret=env.FAUNA_SECRET)

    @classmethod
    def q(cls) -> Query:
        """Return the FaunaDB query object."""
        return cls.client().query

    @classmethod
    def provision(cls):
        """Provisions all the resources to fauna, should be run within the on_startup lifespan event.
            It creates the collections, indexes and unique constraints from the metadata obtained from the pydantic models.
            The metadata is obtained from the __fields__ attribute of the pydantic models.
            The __fields__ attribute is a dictionary of the fields of the model, the key is the name of the field and the value is the FieldInfo object.
            If the FieldInfo object has the extra attribute with the key index and the value True, then the field is indexed.
            If the FieldInfo object has the extra attribute with the key unique and the value True, then the field is unique.
            Also implements the method to creates all the indexes for the fields that have the index attribute set to True.
        """
       
        # We check if the collection exists, if it doesn't we create it.
        
        if not cls.q()(q.exists(q.collection(cls.__name__.lower()))):
            cls.q()(q.create_collection({"name": cls.__name__.lower()}))
        for field in cls.__fields__.values():
            if field.field_info.extra.get("index"):
                data = {
                    "name": f"{cls.__name__.lower()}_by_{field.name}".lower(),
                    "source": q.collection(cls.__name__.lower()),
                    "terms": [{"field": ["data", field.name]}],
                }
                if cls.q()(q.exists(q.index(data["name"]))):
                    continue
                cls.q()(q.create_index(data))
        cls.q()(q.create_index({"name": f"{cls.__name__}_all", "source": q.collection(f"{cls.__name__.lower()}")})) 
        print(f"Provisioned {cls.__name__} collection and indexes.")
    
    def create(self):
        """Creates a new document in the collection."""
        return self.q()(q.create(q.collection(self.__class__.__name__.lower()), {"data": self.dict()}))