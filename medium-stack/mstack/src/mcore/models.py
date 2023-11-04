from typing import Annotated, ClassVar, Union, Optional
from pathlib import Path
from os import environ
from enum import Enum

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
MSERVE_UPLOAD_DIRECTORY = environ.get('MSERVE_UPLOAD_DIRECTORY', '/tmp/mserver/uploads')
MSERVE_LOCAL_STORAGE_DIRECTORY = environ.get('MSERVE_LOCAL_STORAGE_DIRECTORY', '/mstack/files')

#
# base models
#


class ContentModel(BaseModel):

    @model_validator(mode='after')
    def generate_cid(self) -> 'ContentModel':
        data = self.model_dump(exclude={'id', 'cid'})
        self.cid = ContentId.from_dict(data)
        return self


class ContentModelCreator(BaseModel):

    def create_content_model(self) -> 'ContentModel':
        return self.CONTENT_MODEL(**self.model_dump())


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


class UserCreator(ContentModelCreator):
    CONTENT_MODEL: ClassVar[str] = User

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
    pending = 'pending'
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

    total_size: int

    status: FileUploadStatus = FileUploadStatus.uploading
    total_uploaded: int = 0
    error: Optional[str] = None

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'type': 'image',
                    'total_size': 100_000,
                    'status': 'uploading',
                    'total_uploaded': 10_000
                }
            ]
        }
    }

    def upload_path(self) -> Path:
        if self.id is None:
            raise ValueError(f'FileUploader must have an id to get an upload path')
        
        return Path(MSERVE_UPLOAD_DIRECTORY) / str(self.id)
    
    def local_storage_path(self) -> Path:
        if self.id is None:
            raise ValueError(f'FileUploader must have an id to get a local file path')
        
        return Path(MSERVE_LOCAL_STORAGE_DIRECTORY) / str(self.id)


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

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441', 
                    'cid': '0VcRfJsAIeMvHFxW2c1FFgk2PFc5S16zFEydoCtKhaSg105.json', 
                    'payload_cid': '0Wh2aaOSrURBH32Z_Dgg8BgHB_fQllwLo_0arWPH_PQo7103671.jpg', 
                    'height': 3584, 
                    'width': 5376
                }
            ]
        }
    }

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
AudioFilePayloadCid = Annotated[ContentIdType, id_schema('a string representing an audio file payload cid')]

class AudioFile(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'audio_files'

    id: AudioFileId = Field(**db_id_kwargs)
    cid: AudioFileCid = Field(**cid_kwargs)
    
    payload_cid: AudioFilePayloadCid = Field(**cid_kwargs)

    duration: float   # number of seconds
    bit_rate: int

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441', 
                    'cid': '0qB-A2d1Jt-DTBqAZZgBuTvH4tDbIFpxyfWmkxTZejXo114.json', 
                    'payload_cid': '0SOT7ZsLeQYg6MbcabM049T_DKWbLXl6BR724v3xD9fo2633142.mp3', 
                    'duration': 65.828, 
                    'bit_rate': 320000
                }
            ]
        }
    }

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
VideoFilePayloadCid = Annotated[ContentIdType, id_schema('a string representing a video file payload cid')]

class VideoFile(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'video_files'

    id: VideoFileId = Field(**db_id_kwargs)
    cid: VideoFileCid = Field(**cid_kwargs)
    
    payload_cid: VideoFilePayloadCid = Field(**cid_kwargs)

    height: int
    width: int
    duration: float
    bit_rate: int
    has_audio: bool

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441', 
                    'cid': '0r62C64HF6Qn5WqjilmNmSlsZjnK52ifR178pPyA8bgI164.json', 
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
TextFilePayloadCid = Annotated[ContentIdType, id_schema('a string representing a text file payload cid')]

class TextFile(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'text_files'

    id: TextFileId = Field(**db_id_kwargs)
    cid: TextFileCid = Field(**cid_kwargs)
    
    payload_cid: TextFilePayloadCid = Field(**cid_kwargs)
