import os
import shutil
import random

from enum import Enum

from typing import Annotated, ClassVar, Union, Optional, Type
from pathlib import Path
from datetime import datetime

from mcore.errors import MStackFilePayloadError
from mcore.types import unique_list_validator, TagList
from mcore.util import utc_now, random_name, random_email, random_phone_number, example_cid, adjectives, nouns

from lorem_text import lorem
from pymediainfo import MediaInfo
from bson import ObjectId
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    model_validator,
    conlist
)

from mcore.types import ContentId, MongoId, id_schema, db_id_kwargs, cid_kwargs, ContentIdType

__all__ = [
    'mediainfo',

    'ContentModel',
    'ModelCreator',
    
    'UserId',
    'UserCid',
    'User',
    'UserCreator',

    'FileUploaderId',
    'FileUploadStatus',
    'FileUploadTypes',
    'FileUploader',
    'FileUploaderCreator',

    'ImageFileId',
    'ImageFileCid',
    'ImageFilePayloadCid',
    'ImageFile',

    'AltImageFormatList',
    'ImageReleaseId',
    'ImageReleaseCid',
    'ImageRelease',
    'ImageReleaseCreator',
    
    'AudioFileId',
    'AudioFileCid',
    'AudioFilePayloadCid',
    'AudioFile',

    'AltAudioFormatList',
    'AudioReleaseId',
    'AudioReleaseCid',
    'AudioRelease',

    'VideoFileId',
    'VideoFileCid',
    'VideoFilePayloadCid',
    'VideoFile',

    'AltVideoFormatList',
    'VideoReleaseId',
    'VideoReleaseCid',
    'VideoRelease',
    
    'TextFileId',
    'TextFileCid',
    'TextFilePayloadCid',
    'TextFile',

    'AnyAVReleaseCid',
    'AnyMediaReleaseCid',
    'AnyReleaseCid'
]

# ids --- moved these to types.py

UserId = Annotated[MongoId, id_schema('a string representing a user id')]
UserCid = Annotated[ContentIdType, id_schema('a string representing a user content id')]
ProfileId = Annotated[MongoId, id_schema('a string representing a profile id')]
ProfileCid = Annotated[ContentIdType, id_schema('a string representing a profile content id')]  
ProfileGroupId = Annotated[MongoId, id_schema('a string representing a profile group id')]
ProfileGroupCid = Annotated[ContentIdType, id_schema('a string representing a profile groups content id')]
AnyProfileCid = ProfileCid | ProfileGroupCid

ProfileList = Annotated[
    conlist(AnyProfileCid, min_length=1, max_length=50),
    unique_list_validator, 
    id_schema('a unique list of profile or profile group cids')
]

#
# media info
#


MEDIAINFO_LIB_PATH = os.environ.get('MEDIAINFO_LIB_PATH', '')   # '/opt/homebrew/Cellar/libmediainfo/23.09/lib/libmediainfo.dylib'
MSERVE_LOCAL_STORAGE_DIRECTORY = os.environ.get('MSERVE_LOCAL_STORAGE_DIRECTORY', '/app/data/files')
MSERVE_LOCAL_UPLOAD_DIRECTORY = os.environ.get('MSERVE_LOCAL_UPLOAD_DIRECTORY', '/app/data/uploads')

def mediainfo(path: Union[str, Path]) -> MediaInfo:
    library_file = None if MEDIAINFO_LIB_PATH == '' else MEDIAINFO_LIB_PATH
    return MediaInfo.parse(path, library_file=library_file)

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
    
    @classmethod
    def generate(cls, **kwargs) -> 'ContentModel':
        raise NotImplementedError('generate must be implemented by subclasses')
    
    @classmethod
    def generate_model(cls, with_id:bool = None, gen_kwargs:dict = None, create_kwargs:dict = None) -> 'ContentModel':
        """
        if with_id is True, generate a UserCreator with a random id
        if with_id is False, generate a UserCreator without an id
        if with_id is None, randomize whether or not to generate an id
        """
        if gen_kwargs is None:
            gen_kwargs = {}
        if create_kwargs is None:
            create_kwargs = {}

        model = cls.generate(**gen_kwargs).create_model(**create_kwargs)
        if with_id is None:
            with_id = random.choice([True, False])
        
        if with_id:
            model.id = ObjectId()
        
        return model


#
# user
#


class User(ContentModel):
    DB_NAME: ClassVar[str] = 'users'

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


UserPasswordHashId = Annotated[MongoId, id_schema('a string representing a user password hash id')]

class UserPasswordHash(BaseModel):
    DB_NAME: ClassVar[str] = 'user_password_hashes'
    id: UserPasswordHashId = Field(**db_id_kwargs)
    user_id: UserId
    hashed_password: str


class UserCreator(ModelCreator):
    MODEL: ClassVar[Type[User]] = User

    email: EmailStr
    phone_number: PhoneNumber
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    middle_name: str = Field(min_length=1, max_length=100, default=None, validate_default=False)    
    password1: str = Field(min_length=8, max_length=64)
    password2: str = Field(min_length=8, max_length=64)

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'email': 'email@example.com',
                    'phone_number': 'tel:+1-513-555-0123',
                    'first_name': 'Alice',
                    'last_name': 'Smith',
                    'middle_name': 'C',
                    'password1': 'password',
                    'password2': 'password'
                }
            ]
        }
    }

    def create_model(self, **kwargs) -> 'User':
        params = self.model_dump()
        del params['password1']
        del params['password2']

        params.update(kwargs)
        return User(**params)

    @model_validator(mode='after')
    def validate_passwords(self) -> 'UserCreator':
        if self.password1 != self.password2:
            raise ValueError('passwords do not match')
        return self

    @classmethod
    def generate(cls, **kwargs) -> 'UserCreator':
        name = random_name()
        pw = str(random.randint(10_000_000, 999_999_999))
        return cls(
            email=random_email(name),
            phone_number=random_phone_number(),
            first_name=name.first,
            last_name=name.last,
            middle_name=name.middle,
            password1=pw,
            password2=pw
        )

#
# profiles
#
    
class Profile(ContentModel):
    SNAKE_CASE: ClassVar[str] = 'profile'
    DB_NAME: ClassVar[str] = True
    ENDPOINT: ClassVar[str] = True

    id: ProfileId = Field(**db_id_kwargs)
    cid: ProfileCid = Field(**cid_kwargs)
    user_cid: UserCid = Field(**cid_kwargs)

    name: str = Field(min_length=1, max_length=300)
    short_name: str = Field(min_length=1, max_length=50)
    abreviated_name: str = Field(max_length=10)

    tag_line: str = Field(min_length=1, max_length=300)
    bio: str = Field(min_length=1, max_length=1500)
    tags: TagList = None

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '0SXvy_2EV0Pm6YAmfznDb5nwT4l7RfIXN9RNe9v279vk707.json',
                    'user_cid': str(example_cid(User)),
                    'name': 'Blue Giant Footballer',
                    'short_name': 'Blue Giant',
                    'abreviated_name': 'BGF',
                    'tag_line': 'woke up like dis',
                    'bio': 'Just another dude who loves football',
                    'tags': ['football', 'soccer', 'uk']
                }
            ]
        }
    }


class ProfileCreator(ModelCreator):
    """
    This class is used to create a Profile model, user_cid is not exposed because this model represents user input,
    the user_cid is added by the controller which uses the cid of the authenticated user.
    """

    MODEL: ClassVar[Type[Profile]] = Profile

    name: str = Field(min_length=1, max_length=300)
    short_name: str = Field(min_length=1, max_length=50)
    abreviated_name: str = Field(max_length=10)

    tag_line: str = Field(min_length=1, max_length=300)
    bio: str = Field(min_length=1, max_length=1500)
    tags: TagList = None

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'name': 'Blue Giant Footballer',
                    'short_name': 'Blue Giant',
                    'abreviated_name': 'BGF',
                    'tag_line': 'woke up like dis',
                    'bio': 'Just another dude who loves football',
                    'tags': ['football', 'soccer', 'uk']
                }
            ]
        }
    }

    @classmethod
    def generate(cls, user:User=None) -> 'ProfileCreator':
        if user is None:
            user = UserCreator.generate_model()
        
        # name #

        name_seed = random.randint(0, 5)

        if name_seed == 1:
            seed_words = [user.first_name, user.last_name]
        elif name_seed == 2:
            seed_words = [user.first_name[0], user.last_name]
        elif name_seed == 3:
            seed_words = [user.first_name[0], user.last_name, random.choice(adjectives)]
        elif name_seed == 4:
            seed_words = [random.choice(adjectives), user.first_name[0], user.last_name]
        else:
            seed_words = [random.choice(adjectives), random.choice(adjectives), random.choice(nouns)]
        
        if random.randint(0, 3) < 3:
            seed_words = [seed_word.capitalize() for seed_word in seed_words]
        
        name = ' '.join(seed_words)

        # short name #

        short_name_seed = random.randint(0, 5)

        if short_name_seed in [0, 1]:
            short = f'{seed_words[0]} {seed_words[-1]}'
        elif short_name_seed in [2, 3]:
            short = f'{seed_words[0][0]}. {seed_words[-1]}'
        else:
            short = f'{seed_words[0]} {seed_words[-1][0]}.'
        
        # abreviated name #

        abreviated = ''.join([seed_word[0].capitalize() for seed_word in seed_words])

        return cls(
            name=name,
            short_name=short,
            abreviated_name=abreviated,
            tag_line=lorem.sentence()[0:300],
            bio=lorem.paragraph()[0:1500],
            tags=list(set(lorem.words(random.randint(2, 7))))
        )


#
# file classes
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
    DB_NAME: ClassVar[str] = 'file_uploads'

    id: FileUploaderId = Field(**db_id_kwargs)
    type: FileUploadTypes
    user_cid: UserCid = Field(**cid_kwargs)

    result_cid: Optional[ContentIdType] = Field(**cid_kwargs)

    total_size: int
    ext: str

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
                    'ext': 'jpg',
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

    
    def local_path(self) -> Path:
        if self.id is None:
            raise ValueError('FileUploader must have an id to get a local file path')
        
        ext = self.ext if self.ext.startswith('.') else f'.{self.ext}'
        
        return Path(MSERVE_LOCAL_UPLOAD_DIRECTORY) / f'{self.id}{ext}'


class FileUploaderCreator(ModelCreator):
    MODEL: ClassVar[Type[FileUploader]] = FileUploader

    type: FileUploadTypes
    total_size: int
    ext: str

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'type': 'image',
                    'total_size': 100_000,
                    'ext': 'jpg'
                }
            ]
        }
    }


class BaseFile(ContentModel):

    @property
    def local_path(self) -> Path:
        if self.payload_cid is None:
            raise ValueError('File must have a cid to get a local path')
        return Path(MSERVE_LOCAL_STORAGE_DIRECTORY) / str(self.payload_cid)
    
    @classmethod
    def from_filepath(cls:'BaseFile', filepath:Union[str, Path], user_cid: UserCid) -> 'BaseFile':
        raise NotImplementedError('from_filepath must be implemented by subclasses')

    @classmethod
    def ingest(cls:'BaseFile', filepath:Union[str, Path], user_cid: UserCid, leave_original:bool = False) -> 'BaseFile':
        item = cls.from_filepath(filepath, user_cid)
        if leave_original:
            shutil.copyfile(filepath, item.local_path)
        else:
            os.rename(filepath, item.local_path)
        
        return item


#
#  image files
#


ImageFileId = Annotated[MongoId, id_schema('a string representing an image file id')]
ImageFileCid = Annotated[ContentIdType, id_schema('a string representing an image file cid')]
ImageFilePayloadCid = Annotated[ContentIdType, id_schema('a string representing an image file payload cid')]


class ImageFile(BaseFile):
    DB_NAME: ClassVar[str] = 'image_files'

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


AltImageFormatList = Annotated[
    None | conlist(ImageFileCid, min_length=1, max_length=10),
    unique_list_validator,
    id_schema('a unique list of image files or image file cids')
]

ImageReleaseId = Annotated[MongoId, id_schema('a string representing an image release id')]
ImageReleaseCid = Annotated[ContentIdType, id_schema('a string representing an image release cid')]

class ImageRelease(ContentModel):
    DB_NAME: ClassVar[str] = 'image_release'

    id: ImageReleaseId = Field(**db_id_kwargs)
    cid: ImageReleaseCid = Field(**cid_kwargs)
    user_cid: UserCid = Field(**cid_kwargs)

    master: ImageFileCid
    alt_formats: AltImageFormatList = None


class ImageReleaseCreator(ModelCreator):
    MODEL: ClassVar[Type[ImageRelease]] = ImageRelease

    master: ImageFileCid
    alt_formats: AltImageFormatList = None

#
# audio files
#


AudioFileId = Annotated[MongoId, id_schema('a string representing an audio file id')]
AudioFileCid = Annotated[ContentIdType, id_schema('a string representing an audio file cid')]
AudioFilePayloadCid = Annotated[ContentIdType, id_schema('a string representing an audio file payload cid')]


class AudioFile(BaseFile):
    DB_NAME: ClassVar[str] = 'audio_files'

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


AltAudioFormatList = Annotated[
    None | conlist(AudioFileCid, min_length=1, max_length=10),
    unique_list_validator,
    id_schema('a unique list of audio files or audio file cids')
]

AudioReleaseId = Annotated[MongoId, id_schema('a string representing an audio release id')]
AudioReleaseCid = Annotated[ContentIdType, id_schema('a string representing an audio release id')]

class AudioRelease(ContentModel):
    DB_NAME: ClassVar[str] = 'audio_release'

    id: AudioReleaseId = Field(**db_id_kwargs)
    cid: AudioReleaseCid = Field(**cid_kwargs)

    master: AudioFileCid
    alt_formats: AltAudioFormatList = None

VideoFileId = Annotated[MongoId, id_schema('a string representing a video file id')]
VideoFileCid = Annotated[ContentIdType, id_schema('a string representing a video file cid')]
VideoFilePayloadCid = Annotated[ContentIdType, id_schema('a string representing a video file payload cid')]

class VideoFile(BaseFile):
    DB_NAME: ClassVar[str] = 'video_files'

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


AltVideoFormatList = Annotated[
    None | conlist(VideoFileCid, min_length=1, max_length=10),
    unique_list_validator,
    id_schema('a unique list of video files or video file cids')
]

VideoReleaseId = Annotated[MongoId, id_schema('a string representing a video release id')]
VideoReleaseCid = Annotated[ContentIdType, id_schema('a string representing a video release cid')]

class VideoRelease(ContentModel):
    DB_NAME: ClassVar[str] = 'video_release'

    id: VideoReleaseId = Field(**db_id_kwargs)
    cid: VideoReleaseCid = Field(**cid_kwargs)

    master: VideoFileCid
    alt_formats: AltVideoFormatList = None

#
# text files
#

TextFileId = Annotated[MongoId, id_schema('a string representing a text file id')]
TextFileCid = Annotated[ContentIdType, id_schema('a string representing a text file cid')]
TextFilePayloadCid = Annotated[ContentIdType, id_schema('a string representing a text file payload cid')]

class TextFile(ContentModel):
    DB_NAME: ClassVar[str] = 'text_files'

    id: TextFileId = Field(**db_id_kwargs)
    cid: TextFileCid = Field(**cid_kwargs)
    user_cid: UserCid = Field(**cid_kwargs)
    
    payload_cid: TextFilePayloadCid = Field(**cid_kwargs)


#
# misc
#

AnyAVReleaseCid = Union[AudioReleaseCid, VideoReleaseCid]
AnyMediaReleaseCid = Union[AudioReleaseCid, VideoReleaseCid, ImageReleaseCid]
AnyReleaseCid = Union[AudioReleaseCid, VideoReleaseCid, ImageReleaseCid, TextFileCid]