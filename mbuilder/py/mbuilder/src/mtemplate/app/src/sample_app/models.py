from typing import Annotated, ClassVar, Type
import random

from pydantic import Field
from lorem_text import lorem

from mcore.models import (
    MongoId, 
    ContentModel, 
    ContentIdType, 
    ModelCreator,
    UserCid,

    db_id_kwargs, 
    cid_kwargs,
    id_schema
)

__all__ = [
    'SampleItemId',
    'SampleItemCid',
    'SampleItem',
    'SampleItemCreator'
]

SampleItemId = Annotated[MongoId, id_schema('a string representing a sample item id')]
SampleItemCid = Annotated[ContentIdType, id_schema('a string representing a sample item content id')]


class SampleItem(ContentModel):
    LOWER_CASE: ClassVar[str] = 'sample item'
    DB_NAME: ClassVar[str] = 'profiles'
    ENDPOINT: ClassVar[bool] = True

    id: SampleItemId = Field(**db_id_kwargs)
    cid: SampleItemCid = Field(**cid_kwargs)
    user_cid: UserCid = Field(**cid_kwargs)

    message: str = Field(default='hello.world', min_length=1, max_length=300)
    num: int = Field(default=42, ge=0, le=100)

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '0bWjvPsoa7b236p5w2pUF2GUuE1kYtgEbYDh72jB7RZk106.json',
                    'user_cid': '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                    'message': 'Hello World!',
                    'num': 33
                }
            ]
        }
    }


class SampleItemCreator(ModelCreator):
    MODEL: ClassVar[Type[SampleItem]] = SampleItem

    message: str = Field(default='hello.world', min_length=1, max_length=300)
    num: int = Field(default=42, ge=0, le=100)

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'message': 'Hello World!',
                    'num': 33
                }
            ]
        }
    }

    @classmethod
    def generate(self) -> 'SampleItemCreator':
        return SampleItemCreator(
            message=lorem.words(random.randint(1, 10)),
            num=random.randint(0, 100)
        )