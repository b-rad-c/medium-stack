from typing import Annotated, ClassVar, Union
from pathlib import Path
from os import environ

from .errors import MediumFilePayloadError

from pymediainfo import MediaInfo
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    model_validator
)

from .types import ContentId, MongoId, id_schema, db_id_kwargs, cid_kwargs, ContentIdType

__all__ = [
    'id_schema',
    'MongoId',
    'db_id_kwargs',
    'cid_kwargs',
    
    'UserId',
    'UserCid',
    'User',

    'ImageFile',
    'ImageFileId',
    'ImageFileCid',
    'AudioFile',
    'AudioFileId',
    'AudioFileCid',
    'VideoFile',
    'VideoFileId',
    'VideoFileCid',
    'TextFile',
    'TextFileId',
    'TextFileCid'
]

# MEDIAINFO_LIB_PATH = environ.get('MEDIAINFO_LIB_PATH', '/opt/homebrew/Cellar/libmediainfo/23.09/lib/libmediainfo.dylib')
MEDIAINFO_LIB_PATH = environ.get('MEDIAINFO_LIB_PATH', '')


#
# base models
#


class ContentModel(BaseModel):

    @model_validator(mode='after')
    def generate_cid(self) -> 'ContentModel':
        data = self.model_dump(exclude={'id', 'cid'})
        self.cid = ContentId.from_dict(data)
        return self


#
# user
#


UserId = Annotated[MongoId, id_schema('a string representing a user id')]
UserCid = Annotated[ContentIdType, id_schema('a string representing a user content id')]


class User(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'users'

    id: UserId = Field(**db_id_kwargs)
    cid: UserCid = Field(**cid_kwargs)

    email: EmailStr
    phone_number: PhoneNumber
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    middle_name: str = Field(min_length=1, max_length=100, default=None, validate_default=False)    


#
# media / file primatives
#

def mediainfo(path: Union[str, Path]) -> MediaInfo:
    library_file = None if MEDIAINFO_LIB_PATH == '' else MEDIAINFO_LIB_PATH
    return MediaInfo.parse(path, library_file=library_file)


ImageFileId = Annotated[MongoId, id_schema('a string representing an image file id')]
ImageFileCid = Annotated[ContentIdType, id_schema('a string representing an image file cid')]
ImageFilePayloadCid = Annotated[ContentIdType, id_schema('a string representing an image file payload cid')]

class ImageFile(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'image_files'

    id: ImageFileId = Field(**db_id_kwargs)
    cid: ImageFileCid = Field(**cid_kwargs)

    payload_cid: ImageFilePayloadCid = Field(**cid_kwargs)

    height: int
    width: int

    @classmethod
    def from_filepath(cls:'ImageFile', filepath:Union[str, Path]) -> 'ImageFile':
        payload_cid = ContentId.from_filepath(filepath)
        info = mediainfo(filepath)
        try:
            height = info.image_tracks[0].height
            width = info.image_tracks[0].width
        except IndexError:
            raise MediumFilePayloadError(f'Does not contain image data: {filepath}')
        except AttributeError:
            raise MediumFilePayloadError(f'Unknown error getting media info: {filepath}')

        return cls(payload_cid=payload_cid, height=height, width=width)



AudioFileId = Annotated[MongoId, id_schema('a string representing an audio file id')]
AudioFileCid = Annotated[ContentIdType, id_schema('a string representing an audio file cid')]

class AudioFile(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'audio_files'

    id: AudioFileId = Field(**db_id_kwargs)
    cid: AudioFileCid = Field(**cid_kwargs)
    
    payload_cid: ContentId

    duration: float   # number of seconds
    bit_rate: int

    @classmethod
    def from_filepath(cls:'AudioFile', filepath:Union[str, Path]) -> 'AudioFile':
        payload_cid = ContentId.from_filepath(filepath)
        info = mediainfo(filepath)
        if len(info.audio_tracks) == 0:
            raise MediumFilePayloadError(f'Does not contain audio track(s): {filepath}')
        if len(info.video_tracks) > 0:
            raise MediumFilePayloadError(f'Audio file contains video track(s): {filepath}')
        
        try:
            duration = info.general_tracks[0].duration / 1000
            bit_rate = info.general_tracks[0].overall_bit_rate
        except (AttributeError, IndexError):
            raise MediumFilePayloadError(f'Unknown error getting media info: {filepath}')

        return cls(payload_cid=payload_cid, duration=duration, bit_rate=bit_rate)


VideoFileId = Annotated[MongoId, id_schema('a string representing a video file id')]
VideoFileCid = Annotated[ContentIdType, id_schema('a string representing a video file cid')]


class VideoFile(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'video_files'

    id: VideoFileId = Field(**db_id_kwargs)
    cid: VideoFileCid = Field(**cid_kwargs)
    
    payload_cid: ContentId

    height: int
    width: int
    duration: float
    bit_rate: int
    has_audio: bool

    @classmethod
    def from_filepath(cls:'VideoFile', filepath:Union[str, Path]) -> 'VideoFile':
        payload_cid = ContentId.from_filepath(filepath)
        info = mediainfo(filepath)

        if len(info.video_tracks) == 0:
            raise MediumFilePayloadError(f'Does not contain video track: {filepath}')
        
        height = info.video_tracks[0].height
        width = info.video_tracks[0].width
        
        try:
            duration = info.general_tracks[0].duration / 1000
            bit_rate = info.general_tracks[0].overall_bit_rate
        except (AttributeError, IndexError):
            raise MediumFilePayloadError(f'Unknown error getting media info: {filepath}')
        
        has_audio = len(info.audio_tracks) > 0

        return cls(payload_cid=payload_cid, height=height, width=width, duration=duration, bit_rate=bit_rate, has_audio=has_audio)


TextFileId = Annotated[MongoId, id_schema('a string representing a text file id')]
TextFileCid = Annotated[ContentIdType, id_schema('a string representing a text file cid')]


class TextFile(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'text_files'

    id: TextFileId = Field(**db_id_kwargs)
    cid: TextFileCid = Field(**cid_kwargs)
    
    payload_cid: ContentId
