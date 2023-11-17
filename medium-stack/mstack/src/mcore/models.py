import os 

from enum import Enum

from typing import Annotated, ClassVar, Union, Optional, Type
from pathlib import Path
from datetime import datetime

from mcore.errors import MStackFilePayloadError
from mcore.util import utc_now

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

    'ContentModel',
    'ModelCreator',
    
    'UserId',
    'UserCid',
    'User',
    'UserCreator',

    'FileUploadStatus',
    'FileUploadTypes',
    'FileUploader',
    'FileUploaderCreator',

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
MEDIAINFO_LIB_PATH = os.environ.get('MEDIAINFO_LIB_PATH', '')
MSERVE_LOCAL_STORAGE_DIRECTORY = os.environ.get('MSERVE_LOCAL_STORAGE_DIRECTORY', '/mstack/files')


#
# base models
#


class ContentModel(BaseModel):

    @model_validator(mode='after')
    def generate_cid(self) -> 'ContentModel':
        data = self.model_dump(exclude={'id', 'cid'})
        self.cid = ContentId.from_dict(data)
        return self


class ModelCreator(BaseModel):

    MODEL: ClassVar[str] = None

    def create_model(self, **kwargs) -> 'ContentModel':
        params = self.model_dump()
        params.update(kwargs)
        return self.MODEL(**params)


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

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                    'email': 'email@example.com',
                    'phone_number': 'tel:+1-513-555-0123',
                    'first_name': 'Alice',
                    'last_name': 'Smith',
                    'middle_name': 'C'
                }
            ]
        }
    }


class UserCreator(ModelCreator):
    MODEL: ClassVar[Type[User]] = User

    email: EmailStr
    phone_number: PhoneNumber
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    middle_name: str = Field(min_length=1, max_length=100, default=None, validate_default=False)    

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'email': 'email@example.com',
                    'phone_number': 'tel:+1-513-555-0123',
                    'first_name': 'Alice',
                    'last_name': 'Smith',
                    'middle_name': 'C'
                }
            ]
        }
    }


#
# media / file primatives
#



FileUploaderId = Annotated[MongoId, id_schema('a string representing a file uploader id')]

class FileUploadStatus(str, Enum):
    uploading = 'uploading'
    error = 'error'
    processing = 'processing'
    process_queue = 'process_queue'
    complete = 'complete'


class FileUploadTypes(str, Enum):
    audio = 'audio'
    image = 'image'
    text = 'text'
    video = 'video'


class FileUploader(BaseModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'file_uploads'

    id: FileUploaderId = Field(**db_id_kwargs)
    type: FileUploadTypes
    user_cid: UserCid = Field(**cid_kwargs)

    total_size: int

    created: datetime = Field(default_factory=utc_now)
    modifed: Optional[datetime] = None

    status: FileUploadStatus = FileUploadStatus.uploading
    total_uploaded: int = 0
    error: Optional[str] = None

    lock: Optional[str] = None

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'user_cid': '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                    'type': 'image',
                    'total_size': 100_000,
                    'created': '2023-11-04T22:21:02.185694Z',
                    'modified': None,
                    'status': 'uploading',
                    'total_uploaded': 10_000
                }
            ]
        }
    }
        

    def update_timestamp(self) -> None:
        self.modifed = utc_now()

    
    def local_storage_path(self) -> Path:
        if self.id is None:
            raise ValueError(f'FileUploader must have an id to get a local file path')
        
        return Path(MSERVE_LOCAL_STORAGE_DIRECTORY) / str(self.id)


class FileUploaderCreator(ModelCreator):
    MODEL: ClassVar[Type[FileUploader]] = FileUploader

    type: FileUploadTypes
    total_size: int

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'type': 'image',
                    'total_size': 100_000
                }
            ]
        }
    }


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
    user_cid: UserCid = Field(**cid_kwargs)

    payload_cid: ImageFilePayloadCid = Field(**cid_kwargs)

    height: int = Field(gt=0)
    width: int = Field(gt=0)

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441', 
                    'cid': '0O6Q2voNc_yv7ETIlqrLcni9C1BtYYIHSyq4g1AlS8FQ123.json', 
                    'payload_cid': '0Wh2aaOSrURBH32Z_Dgg8BgHB_fQllwLo_0arWPH_PQo7103671.jpg', 
                    'height': 3584, 
                    'width': 5376
                }
            ]
        }
    }

    @classmethod
    def from_filepath(cls:'ImageFile', filepath:Union[str, Path], user_cid: UserCid) -> 'ImageFile':
        payload_cid = ContentId.from_filepath(filepath)
        info = mediainfo(filepath)
        try:
            height = info.image_tracks[0].height
            width = info.image_tracks[0].width
        except IndexError:
            raise MStackFilePayloadError(f'Does not contain image data: {filepath}')
        except AttributeError:
            raise MStackFilePayloadError(f'Unknown error getting media info: {filepath}')

        return cls(user_cid=user_cid, payload_cid=payload_cid, height=height, width=width)


# class ImageFileCreator(ModelCreator):
#     MODEL: ClassVar[Type[ImageFile]] = ImageFile

#     height: int = Field(gt=0)
#     width: int = Field(gt=0)

#     model_config = {
#         'json_schema_extra': {
#             'examples': [
#                 {
#                     'height': 3584, 
#                     'width': 5376
#                 }
#             ]
#         }
#     }


AudioFileId = Annotated[MongoId, id_schema('a string representing an audio file id')]
AudioFileCid = Annotated[ContentIdType, id_schema('a string representing an audio file cid')]
AudioFilePayloadCid = Annotated[ContentIdType, id_schema('a string representing an audio file payload cid')]


class AudioFile(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'audio_files'

    id: AudioFileId = Field(**db_id_kwargs)
    cid: AudioFileCid = Field(**cid_kwargs)
    user_cid: UserCid = Field(**cid_kwargs)
    
    payload_cid: AudioFilePayloadCid = Field(**cid_kwargs)

    duration: float = Field(gt=0) # numer of seconds
    bit_rate: int = Field(gt=0)

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441', 
                    'cid': '0LDHxLDdQ-4eZd0CiuftNik-8nhUEuzHdo6VV0dmnaQw132.json', 
                    'payload_cid': '0SOT7ZsLeQYg6MbcabM049T_DKWbLXl6BR724v3xD9fo2633142.mp3', 
                    'duration': 65.828, 
                    'bit_rate': 320000
                }
            ]
        }
    }

    @classmethod
    def from_filepath(cls:'AudioFile', filepath:Union[str, Path], user_cid: UserCid) -> 'AudioFile':
        payload_cid = ContentId.from_filepath(filepath)
        info = mediainfo(filepath)
        if len(info.audio_tracks) == 0:
            raise MStackFilePayloadError(f'Does not contain audio track(s): {filepath}')
        if len(info.video_tracks) > 0:
            raise MStackFilePayloadError(f'Audio file contains video track(s): {filepath}')
        
        try:
            duration = info.general_tracks[0].duration / 1000
            bit_rate = info.general_tracks[0].overall_bit_rate
        except (AttributeError, IndexError):
            raise MStackFilePayloadError(f'Unknown error getting media info: {filepath}')

        return cls(user_cid=user_cid, payload_cid=payload_cid, duration=duration, bit_rate=bit_rate)


# class AudioFileCreator(ModelCreator):
#     MODEL: ClassVar[Type[AudioFile]] = AudioFile

#     duration: float = Field(gt=0)
#     bit_rate: int = Field(gt=0)

#     model_config = {
#         'json_schema_extra': {
#             'examples': [
#                 {
#                     'duration': 65.828,
#                     'bit_rate': 320000
#                 }
#             ]
#         }
#     }


VideoFileId = Annotated[MongoId, id_schema('a string representing a video file id')]
VideoFileCid = Annotated[ContentIdType, id_schema('a string representing a video file cid')]
VideoFilePayloadCid = Annotated[ContentIdType, id_schema('a string representing a video file payload cid')]

class VideoFile(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'video_files'

    id: VideoFileId = Field(**db_id_kwargs)
    cid: VideoFileCid = Field(**cid_kwargs)
    user_cid: UserCid = Field(**cid_kwargs)
    
    payload_cid: VideoFilePayloadCid = Field(**cid_kwargs)

    height: int = Field(gt=0)
    width: int = Field(gt=0)
    duration: float = Field(gt=0) 
    bit_rate: int = Field(gt=0)
    has_audio: bool

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441', 
                    'cid': '0onyDuzj4DGrq4uIbipGKkS51gACr4z9WYW_-Np_9bgI182.json', 
                    'payload_cid': '0j_d4uuRMK-Q2LIoT-n6oIT_oE-nriwlp_K8_W8oa1r011061011.mov', 
                    'height': 480, 
                    'width': 853, 
                    'duration': 32.995, 
                    'bit_rate': 2681864, 
                    'has_audio': True
                }
            ]
        }
    }

    @classmethod
    def from_filepath(cls:'VideoFile', filepath:Union[str, Path], user_cid: UserCid) -> 'VideoFile':
        payload_cid = ContentId.from_filepath(filepath)
        info = mediainfo(filepath)

        if len(info.video_tracks) == 0:
            raise MStackFilePayloadError(f'Does not contain video track: {filepath}')
        
        height = info.video_tracks[0].height
        width = info.video_tracks[0].width
        
        try:
            duration = info.general_tracks[0].duration / 1000
            bit_rate = info.general_tracks[0].overall_bit_rate
        except (AttributeError, IndexError):
            raise MStackFilePayloadError(f'Unknown error getting media info: {filepath}')
        
        has_audio = len(info.audio_tracks) > 0

        return cls(user_cid=user_cid, payload_cid=payload_cid, height=height, width=width, duration=duration, bit_rate=bit_rate, has_audio=has_audio)


# class VideoFileCreator(ModelCreator):
#     MODEL: ClassVar[Type[VideoFile]] = VideoFile

#     height: int = Field(gt=0)
#     width: int = Field(gt=0)
#     duration: float = Field(gt=0) 
#     bit_rate: int = Field(gt=0)
#     has_audio: bool

#     model_config = {
#         'json_schema_extra': {
#             'examples': [
#                 {
#                     'height': 480,
#                     'width': 853,
#                     'duration': 32.995,
#                     'bit_rate': 2681864,
#                     'has_audio': True
#                 }
#             ]
#         }
#     }


TextFileId = Annotated[MongoId, id_schema('a string representing a text file id')]
TextFileCid = Annotated[ContentIdType, id_schema('a string representing a text file cid')]
TextFilePayloadCid = Annotated[ContentIdType, id_schema('a string representing a text file payload cid')]

class TextFile(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'text_files'

    id: TextFileId = Field(**db_id_kwargs)
    cid: TextFileCid = Field(**cid_kwargs)
    user_cid: UserCid = Field(**cid_kwargs)
    
    payload_cid: TextFilePayloadCid = Field(**cid_kwargs)
