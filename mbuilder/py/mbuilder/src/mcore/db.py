from mcore.errors import MStackDBError, NotFoundError
from mcore.types import ContentId

from os import environ

from typing import Type, Generator, Union
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

    def get_collection(self, model: InstanceOrType) -> Collection:
        try:
            name = model.__class__.DB_NAME
        except AttributeError:
            try:
                name = model.DB_NAME
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

        collection = self.get_collection(model)
        document = collection.find_one(query)

        if document is None:
            item = ' '.join([f'{k}: {v}' for k, v in query.items()]).replace('_', '')
            raise NotFoundError(f'item not found: {collection.name}: {item}')
        else:
            try:
                return model(**document)
            except TypeError:
                return model.__class__(**document)
    
    def update(self, model:BaseModel) -> None:
        dumped_data = model.model_dump(by_alias=True)

        collection = self.get_collection(model)
        result = collection.update_one({'_id': ObjectId(model.id)}, {'$set': dumped_data})
        if result.modified_count != 1:
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

    def find(self, model_type: Type[BaseModel], filter=None, offset:int=0, size:int=50, **kwargs) -> Generator[BaseModel, None, None]:
        collection = self.get_collection(model_type)
        for entry in collection.find(filter=filter, skip=offset, limit=size, **kwargs):
            yield model_type(**entry)

    def find_one(self, model_type: Type[BaseModel], filter=None, **kwargs) -> BaseModel:
        collection = self.get_collection(model_type)
        entry = collection.find_one(filter, **kwargs)
        if entry is None:
            raise NotFoundError(f'Item not found in database')
        else:
            return model_type(**entry)

    @classmethod
    def from_cache(cls) -> 'MongoDB':
        global _MONGO_DB
        if _MONGO_DB is None:
            _MONGO_DB = cls()
            return _MONGO_DB
        else:
            return _MONGO_DB
