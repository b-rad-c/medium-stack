from .errors import MStackDBError, NotFoundError
from .types import ContentId

from os import environ

from typing import Type, List, Union
from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pydantic import BaseModel

__all__ = [
    'DEFAULT_MONGO_URI',
    'MONGO_DB_URI',
    'DEFAULT_MONGO_DB_NAME',
    'MONGO_DB_NAME',
    'MongoDB'
]


DEFAULT_MONGO_URI = 'mongodb://localhost:27017'
MONGO_DB_URI = environ.get('MONGO_DB_URI', DEFAULT_MONGO_URI)

DEFAULT_MONGO_DB_NAME = 'mdev'
MONGO_DB_NAME = environ.get('MONGO_DB_NAME', DEFAULT_MONGO_DB_NAME)

_MONGO_DB = None

InstanceOrType = Union[Type[BaseModel], BaseModel]

class MongoDB:

    def __init__(self):
        self.client:MongoClient = MongoClient(MONGO_DB_URI)
        try:
            self.db:Collection = self.client[MONGO_DB_NAME]
        except TypeError:
            pass

    def get_collection(self, model: InstanceOrType):
        try:
            name = model.__class__.MONGO_COLLECTION_NAME
        except AttributeError:
            try:
                name = model.MONGO_COLLECTION_NAME
            except AttributeError:
                raise MStackDBError(f'Invalid model: does not define a database collection')
        
        return self.db[name]

    def create(self, model:BaseModel) -> BaseModel:
        collection = self.get_collection(model)
        result = collection.insert_one(model.model_dump(by_alias=True, exclude=['id']))
        model.id = result.inserted_id

    def read(self, model:InstanceOrType, id:Union[str, ObjectId]=None, cid: Union[str, ContentId]=None) -> BaseModel:
        query = {}

        try:
            query['_id'] = ObjectId(model.id)
        except AttributeError:
            if id is not None:
                query['_id'] = ObjectId(id)

        try:
            query['cid'] = str(model.cid)
        except AttributeError:
            if cid is not None:
                query['cid'] = str(cid)

        if '_id' not in query and 'cid' not in query:
            raise MStackDBError('must supply id and or cid to read method')

        document = self.get_collection(model).find_one(query)
        if document is None:
            raise NotFoundError(f'Item not found in database')
        else:
            try:
                return model(**document)
            except TypeError:
                return model.__class__(**document)
    
    def update(self, model:BaseModel) -> None:
        query = {'_id': ObjectId(model.id), 'cid': str(model.cid)}
        dumped_data = model.model_dump(by_alias=True)

        collection = self.get_collection(model)
        result = collection.update_one(query, dumped_data)
        if result.matched_count != 1:
            raise NotFoundError(f'Item not found in database')

    def delete(self, model:InstanceOrType, id:Union[str, ObjectId]=None, cid: Union[str, ContentId]=None) -> None:
        query = {}

        try:
            query['_id'] = ObjectId(model.id)
        except AttributeError:
            if id is not None:
                query['_id'] = ObjectId(id)

        try:
            query['cid'] = str(model.cid)
        except AttributeError:
            if cid is not None:
                query['cid'] = str(cid)

        if '_id' not in query and 'cid' not in query:
            raise MStackDBError('must supply id and or cid to delete method')

        collection = self.get_collection(model)
        collection.delete_one(query)

    def find(self, model_type: Type[BaseModel], offset:int=0, size:int=50, **kwargs) -> List[BaseModel]:
        collection = self.get_collection(model_type)
        for entry in collection.find(skip=offset, limit=size, **kwargs):
            yield model_type(**entry)

    @classmethod
    def from_cache(cls) -> 'MongoDB':
        global _MONGO_DB
        if _MONGO_DB is None:
            _MONGO_DB = cls()
            return _MONGO_DB
        else:
            return _MONGO_DB
