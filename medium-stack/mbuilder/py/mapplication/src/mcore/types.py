import os
import re
import json
import base64

from enum import Enum
from pathlib import Path
from hashlib import sha3_256
from dataclasses import dataclass
from typing import Annotated, ClassVar, ClassVar, Union, Dict, List, BinaryIO, Optional
from bson import ObjectId
from bson.errors import InvalidId
from hashlib import sha3_256

from pydantic import (
    PlainValidator,
    BeforeValidator,
    WithJsonSchema,
    PlainSerializer,
    AliasChoices,
    conlist
)

import boto3


__all__ = [
    'ModelIdType',
    
    'ContentId',
    'cid_kwargs',

    'id_schema',
    'MongoId',
    'db_id_kwargs',

    'DataHierarchy',
    'Hierarchy',

    'unique_list_validator',
    'TagList'
]


class ModelIdType(str, Enum):
    id = 'id'
    cid = 'cid'


#
# content id
#

@dataclass
class ContentId:
    hash:str
    size:int
    ext:str = ''

    read_buffer_len: ClassVar[int] = 1024 * 1024 * 256
    cid_version: ClassVar[int] = 0

    # core methods #

    def __str__(self) -> str:
        return self.identifier
    
    @property
    def identifier(self) -> str:
        cid = f'{self.cid_version}{self.hash}{self.size}'
        if self.ext != '':
            cid += f'.{self.ext}'
        return cid
        
    # initilization methods #

    @classmethod
    def validate(cls, content_id:Union[str, 'ContentId']) -> 'ContentId':
        if isinstance(content_id, str):
            return cls.parse(content_id)
        elif isinstance(content_id, dict):
            return cls(**content_id)
        elif isinstance(content_id, cls):
            return content_id
        else:
            raise ValueError(f'Invalid ContentId input type: {type(content_id)}')

    @classmethod
    def parse(cls, content_id:str) -> 'ContentId':
        version = int(content_id[0])
        if version != 0:
            raise ValueError(f'Invalid CID version')
        
        hash = content_id[1:44]
        if not re.match(r'[A-Za-z0-9-_]{43}', hash):
            raise ValueError('Invalid content id hash')

        period_index = content_id.find('.')

        if period_index == -1:
            size = int(content_id[44:])
            ext = ''
        else:
            size = int(content_id[44:period_index])
            ext = content_id[period_index + 1:]

        return cls(hash=hash, size=size, ext=ext)
    
    @staticmethod
    def _hash_from_digest(digest:bytes) -> str:
        return base64.urlsafe_b64encode(digest).decode('utf-8')[0:-1]   # remove final padding (=)
    
    @classmethod
    def from_string(cls:'ContentId', string:str, ext:str) -> 'ContentId':
        hash_obj = sha3_256(string.encode('utf-8'))
        hash = cls._hash_from_digest(hash_obj.digest())
        return cls(hash=hash, size=len(string), ext=ext)

    @classmethod
    def from_dict(cls:'ContentId', data:Dict) -> 'ContentId':
        json_string = json.dumps(data, sort_keys=True)
        return cls.from_string(json_string, 'json')

    @classmethod
    def from_io(cls:'ContentId', stream:BinaryIO, size:int, ext:str) -> 'ContentId':
        hash_obj = sha3_256()
        while True:
                buffer = stream.read(cls.read_buffer_len)
                if not buffer:
                    break
                hash_obj.update(buffer)

        hash = cls._hash_from_digest(hash_obj.digest())

        return cls(hash=hash, size=size, ext=ext)

    @classmethod
    def from_filepath(cls:'ContentId', filepath:Union[str, Path]) -> 'ContentId':
        path:Path = Path(filepath)
        ext = ''.join(path.suffixes)[1:]

        stat = path.stat()
        size = stat.st_size

        with path.open('rb') as stream:
            return cls.from_io(stream, size, ext)
    
    @classmethod
    def from_s3(cls:'ContentId', bucket:str, key:str) -> 'ContentId':
        ext = os.path.splitext(key)[1][1:]

         # stat file for size #

        s3_client = boto3.client('s3')
        stat = s3_client.head_object(Bucket=bucket, Key=key)
        size = stat['ContentLength']

        # calculate hash #

        hash_obj = sha3_256()
        start = 0
        end = cls.read_buffer_len

        while True:
            if start >= size:
                break

            response = s3_client.get_object(
                Bucket=bucket, 
                Key=key, 
                Range=f'bytes {start}-{min(size, end)}/{size}'
            )
            hash_obj.update(response['Body'].read())

            start += cls.read_buffer_len
            end += cls.read_buffer_len
        
        hash = cls._hash_from_digest(hash_obj.digest())

        return cls(hash=hash, size=size, ext=ext)


def id_schema(description):
    return WithJsonSchema({'type': 'string', 'description': description})

ContentIdType = Annotated[
    ContentId, 
    BeforeValidator(lambda cid: ContentId.validate(cid)),
    PlainValidator(lambda cid: ContentId.validate(cid)),
    PlainSerializer(lambda cid: str(cid), when_used='unless-none'),
    id_schema('a string representing a content id')
]


# reusable kwargs for Field definitions on models #
cid_kwargs = {
    'default': None,
    'validate_default': False
}


#
# mongo id
#

def _validate_object_id(_id:Union[ObjectId, str, None]) -> ObjectId:
    if _id is None:
        return None
    
    try:
        return ObjectId(_id)
    except InvalidId as e:
        # reraising InvalidId as ValueError allows pydantic to raise a ValidationError as expected
        raise ValueError(str(e))

MongoId = Annotated[
    ObjectId, 
    PlainValidator(lambda _id: _validate_object_id(_id)),
    PlainSerializer(lambda _id: str(_id), when_used='json-unless-none'),
    id_schema('a string representing a mongo db id')
]

# reusable kwargs for Field definitions on models #
db_id_kwargs = {
    'default': None,
    'validate_default': False,
    'serialization_alias': '_id',
    'validation_alias': AliasChoices('id', '_id')
}
    

UserId = Annotated[MongoId, id_schema('a string representing a user id')]

#
# hierarchy
#

@dataclass
class DataHierarchy:
    string: str
    levels: List[str]

    def __str__(self) -> str:
        return self.string

    @classmethod
    def validate(cls:'DataHierarchy', hierarchy:str) -> 'DataHierarchy':
        try:
            levels = str.split(hierarchy, '/')
        except TypeError:
            raise ValueError(f'Type {type(hierarchy)} cannot be converted into a DataHierarchy')
        
        for level in levels:
            if level == '':
                raise ValueError(f'DataHierarcy level cannot be an empty string')
        
        return cls(string=hierarchy, levels=levels)

Hierarchy = Annotated[
    DataHierarchy,
    PlainValidator(lambda hierarchy: DataHierarchy.validate(hierarchy)),
    PlainSerializer(lambda hierarchy: str(hierarchy), when_used='json-unless-none'),
    id_schema('a string representing a data hierarcy')
]

#
# misc 
#


"""
Custom logic for keeping a list unique, Set is not used because it does not support unhashable objects such as ContentId,
not does it preserve order of elements. Additionally Pydantic's conlist has deprecated the unique item constraint.
"""

def _list_is_unique(input_list:list) -> list:
    new_list = []
    for item in input_list:
        if item in new_list:
            raise ValueError(f'List contains duplicates')
        else:
            new_list.append(item)

    return new_list

unique_list_validator = BeforeValidator(lambda value: _list_is_unique(value) if value is not None else None)

TagList = Annotated[
    Optional[conlist(str, min_length=0, max_length=15)], 
    unique_list_validator, 
    id_schema('a set (list) of strings')
]