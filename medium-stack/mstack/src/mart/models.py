from typing import Annotated, ClassVar, Union, Optional, Type, List
from enum import StrEnum
from pydantic import BaseModel, Field, conlist

from mcore.types import TagList, unique_list_validator

from mcore.models import (
    MongoId, 
    ContentModel, 
    ContentIdType, 
    ModelCreator,
    UserCid,

    ImageFile,
    ImageFileCid,
    AudioFile,
    AudioFileCid,
    VideoFile,
    VideoFileCid,
    TextFile,
    TextFileCid,

    db_id_kwargs, 
    cid_kwargs,
    id_schema
)


__all__ = [
    'ArtMedium',
    'ArtMediumList',
    'ArtistId',
    'ArtistCid',
    'Artist',
    'ArtistCreator',
    'ArtistGroupId',
    'ArtistGroupCid',
    'ArtistGroup',
    'ArtistGroupCreator',

    'Credit',
    'CreditList',
    'TitleData',

    'AnyImageFile',
    'StillImageId',
    'StillImageCid',
    'StillImage',
    'StillImageCreator',

    'AnyStillImage',
    'StillImageAlbumId',
    'StillImageAlbumCid',
    'StillImageAlbum',
    'StillImageAlbumCreator'
]

#
# artist, credits, metadata
#


class ArtMedium(StrEnum):
    audio = 'audio'
    podcast = 'podcast'
    still = 'still'
    text = 'text'
    video = 'video'

ArtMediumList = Annotated[
    conlist(ArtMedium, min_length=1, max_length=5), 
    unique_list_validator, 
    id_schema('a unique list of art mediums')
]


ArtistId = Annotated[MongoId, id_schema('a string representing an artist id')]
ArtistCid = Annotated[ContentIdType, id_schema('a string representing an artist content id')]


class Artist(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'artists'

    id: ArtistId = Field(**db_id_kwargs)
    cid: ArtistCid = Field(**cid_kwargs)
    user_cid: UserCid = Field(**cid_kwargs)

    name: str = Field(min_length=1, max_length=300)
    short_name: str = Field(min_length=1, max_length=50)
    abreviated_name: str = Field(max_length=10)

    summary: str = Field(min_length=1, max_length=300)
    description: str = Field(min_length=1, max_length=1500)
    mediums: ArtMediumList
    tags: TagList = None

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '0SXvy_2EV0Pm6YAmfznDb5nwT4l7RfIXN9RNe9v279vk707.json',
                    'user_cid': '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                    'name': 'Frida Kahlo',
                    'short_name': 'Kahlo',
                    'abreviated_name': 'FK',
                    'summary': 'Mexican painter known for her many portraits, self-portraits, and works inspired by the nature and artifacts of Mexico.',
                    'description': 'Frida Kahlo de Rivera was a Mexican artist who painted many portraits, self-portraits, '
                        'and works inspired by the nature and artifacts of Mexico. Her work has been celebrated internationally as emblematic of '
                        'Mexican national and indigenous traditions, and by feminists for its uncompromising depiction of the female experience and form.',
                    'mediums': ['still'],
                    'tags': ['painting', 'mexico', 'feminist', 'surrealism']
                }
            ]
        }
    }


class ArtistCreator(ModelCreator):

    MODEL: ClassVar[Type[Artist]] = Artist

    user_cid: UserCid = Field(**cid_kwargs)

    name: str = Field(min_length=1, max_length=300)
    short_name: str = Field(min_length=1, max_length=50)
    abreviated_name: str = Field(max_length=10)

    summary: str = Field(min_length=1, max_length=300)
    description: str = Field(min_length=1, max_length=1500)
    mediums: ArtMediumList
    tags: TagList = None

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'user_cid': '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                    'name': 'Frida Kahlo',
                    'short_name': 'Kahlo',
                    'abreviated_name': 'FK',
                    'summary': 'Mexican painter known for her many portraits, self-portraits, and works inspired by the nature and artifacts of Mexico.',
                    'description': 'Frida Kahlo de Rivera was a Mexican artist who painted many portraits, self-portraits, '
                        'and works inspired by the nature and artifacts of Mexico. Her work has been celebrated internationally as emblematic of '
                        'Mexican national and indigenous traditions, and by feminists for its uncompromising depiction of the female experience and form.',
                    'mediums': ['still'],
                    'tags': ['painting', 'mexico', 'feminist', 'surrealism']
                }
            ]
        }
    }


ArtistGroupId = Annotated[MongoId, id_schema('a string representing an artist group id')]
ArtistGroupCid = Annotated[ContentIdType, id_schema('a string representing an artist content id')]


class ArtistGroup(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'artist_groups'

    id: ArtistGroupId = Field(**db_id_kwargs)
    cid: ArtistGroupCid = Field(**cid_kwargs)

    name: str = Field(min_length=1, max_length=300)
    short_name: str = Field(min_length=1, max_length=50)
    abreviated_name: str = Field(max_length=10)

    summary: str = Field(min_length=1, max_length=300)
    description: str = Field(min_length=1, max_length=1500)
    mediums: ArtMediumList
    tags: TagList = None

    artists: Annotated[List[ArtistCid], Field(min_length=1, max_length=50), unique_list_validator, id_schema('a unique list of artist cids')]

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '0YWW27Y2VyeUhF0wWV3Ym-hiYsMkXEK2uKeVD7XWQBgg684.json',
                    'name': 'The Beatles',
                    'short_name': 'The Beatles',
                    'abreviated_name': 'TB',
                    'summary': 'English rock band formed in Liverpool in 1960.',
                    'description': 'The Beatles were an English rock band formed in Liverpool in 1960. With a line-up comprising John Lennon, '
                                   'Paul McCartney, George Harrison and Ringo Starr, they are regarded as the most influential band of all time.',
                    'mediums': ['audio', 'video'],
                    'tags': ['rock', 'pop', 'british invasion'],
                    'artists': [
                        '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json', 
                        '0Ve5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                        '0We5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                        '0Xe5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json'
                    ]
                }
            ]
        }
    }


class ArtistGroupCreator(ModelCreator):

    MODEL: ClassVar[Type[ArtistGroup]] = ArtistGroup

    name: str = Field(min_length=1, max_length=300)
    short_name: str = Field(min_length=1, max_length=50)
    abreviated_name: str = Field(max_length=10)

    summary: str = Field(min_length=1, max_length=300)
    description: str = Field(min_length=1, max_length=1500)
    mediums: ArtMediumList
    tags: TagList = None

    artists: Annotated[List[ArtistCid], Field(min_length=1, max_length=50, default_factory=list), unique_list_validator, id_schema('a unique list of artist cids')]

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'name': 'The Beatles',
                    'short_name': 'The Beatles',
                    'abreviated_name': 'TB',
                    'summary': 'English rock band formed in Liverpool in 1960.',
                    'description': 'The Beatles were an English rock band formed in Liverpool in 1960. With a line-up comprising John Lennon, '
                                   'Paul McCartney, George Harrison and Ringo Starr, they are regarded as the most influential band of all time.',
                    'mediums': ['audio', 'video'],
                    'tags': ['rock', 'pop', 'british invasion'],
                    'artists': [
                        '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json', 
                        '0Ve5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                        '0We5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                        '0Xe5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json'
                    ]
                }
            ]
        }
    }


class Credit(BaseModel):

    role: str = Field(max_length=50)
    artist: ArtistCid

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'role': 'vocals',
                    'artist': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json'
                }
            ]
        }
    }


CreditList = Annotated[conlist(Credit, min_length=1, max_length=100), unique_list_validator, id_schema('a unique list of credits')]


class TitleData(BaseModel):

    title: str = Field(min_length=1, max_length=300)
    short_title: Optional[str] = Field(None, max_length=50)
    abreviated_title: Optional[str] = Field(None, max_length=10)

    subtitle: Optional[str] = Field(None, max_length=500)
    summary: Optional[str] = Field(None, min_length=1, max_length=300)
    description: Optional[str] = Field(None, min_length=1, max_length=1500)
    genres: Annotated[List[str], Field(min_length=1, max_length=5), unique_list_validator, id_schema('a unique list of genres')]

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': 'Rubber Soul',
                    'genres': ['rock', 'pop', 'british invasion']
                },
                {
                    'title': 'Rubber Soul',
                    'short_title': 'Rubber Soul',
                    'abreviated_title': 'RS',
                    'subtitle': 'By The Beatles',
                    'summary': 'Sixth studio album by the English rock band the Beatles.',
                    'description': 'Rubber Soul is the sixth studio album by the English rock band the Beatles.',
                    'genres': ['rock', 'pop', 'british invasion']
                }
            ]
        }
    }


#
# still image art
#

AnyImageFile = Union[ImageFile, ImageFileCid]

StillImageId = Annotated[MongoId, id_schema('a string representing a still image id')]
StillImageCid = Annotated[ContentIdType, id_schema('a string representing a still image id')]


class StillImage(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'still_image'

    id: StillImageId = Field(**db_id_kwargs)
    cid: StillImageCid = Field(**cid_kwargs)

    creator_id: Union[ArtistCid, ArtistGroupCid]

    master: AnyImageFile
    alt_formats: Annotated[List[AnyImageFile], Field(min_length=1, max_length=10), unique_list_validator, id_schema('a unique list of image file cids')]

    title: Optional[TitleData]
    credits: Optional[Credit]
    tags: TagList

    alt_text: Optional[str]

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '08Ph2mGKw3mFfvQ9liUNEG-E4ea4Eh1aB8gOJgjmy48o695.json',
                    'creator_id': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'master': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'alt_formats': [
                        '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                        '0Ve5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                        '0We5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json'
                    ],
                    'title': {
                        'title': 'My cool Painting',
                        'genres': ['surrealism', 'painting']
                    },
                    'credits': {
                        'role': 'painter',
                        'artist': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json'
                    },
                    'tags': ['surrealism', 'painting', 'oil painting'],
                    'alt_text': 'a surrealistic oil painting'
                }
            ]
        }
    }


class StillImageCreator(ModelCreator):
    MODEL: ClassVar[Type[StillImage]] = StillImage

    creator_id: Union[ArtistCid, ArtistGroupCid]

    master: AnyImageFile
    alt_formats: Annotated[List[AnyImageFile], Field(min_length=1, max_length=10), unique_list_validator, id_schema('a unique list of image file cids')]

    title: Optional[TitleData]
    credits: Optional[Credit]
    tags: TagList

    alt_text: Optional[str]

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'creator_id': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'master': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'alt_formats': [
                        '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                        '0Ve5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                        '0We5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json'
                    ],
                    'title': {
                        'title': 'My cool Painting',
                        'genres': ['surrealism', 'painting']
                    },
                    'credits': {
                        'role': 'painter',
                        'artist': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json'
                    },
                    'tags': ['surrealism', 'painting', 'oil painting'],
                    'alt_text': 'a surrealistic oil painting'
                }
            ]
        }
    }


AnyStillImage = Union[StillImage, StillImageCid]

StillImageAlbumId = Annotated[MongoId, id_schema('a string representing a still image album id')]
StillImageAlbumCid = Annotated[ContentIdType, id_schema('a string representing a still image album content id')]


class StillImageAlbum(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'still_image_album'

    id: StillImageAlbumId = Field(**db_id_kwargs)
    cid: StillImageAlbumCid = Field(**cid_kwargs)

    creator_id: Union[ArtistCid, ArtistGroupCid]

    images: Annotated[List[AnyStillImage], Field(min_length=1, max_length=500), unique_list_validator, id_schema('a unique list of still image cids')]

    title: TitleData
    credits: Credit
    tags: TagList

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '09BtGzrV-fF3goDdVBL8lHth0kUHpSdIPvazNkkzow74605.json',
                    'creator_id': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'images': [
                        '0SLssRK1xnbYVviyCTMoNVPFh53oTuqvSy7R9GLI9iHk782.json',
                        '0TLssRK1xnbYVviyCTMoNVPFh53oTuqvSy7R9GLI9iHk782.json',
                        '0ULssRK1xnbYVviyCTMoNVPFh53oTuqvSy7R9GLI9iHk782.json'
                    ],
                    'title': {
                        'title': 'Old west photography',
                        'genres': ['photography', 'long exposure']
                    },
                    'credits': {
                        'role': 'photographer',
                        'artist': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json'
                    },
                    'tags': ['black and white', 'long exposure', 'star trails']
                }
            ]
        }
    }


class StillImageAlbumCreator(ModelCreator):
    MODEL: ClassVar[Type[StillImageAlbum]] = StillImageAlbum

    creator_id: Union[ArtistCid, ArtistGroupCid]

    images: Annotated[List[AnyStillImage], Field(min_length=1, max_length=500), unique_list_validator, id_schema('a unique list of still image cids')]

    title: TitleData
    credits: Credit
    tags: TagList

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'creator_id': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'images': [
                        '0SLssRK1xnbYVviyCTMoNVPFh53oTuqvSy7R9GLI9iHk782.json',
                        '0TLssRK1xnbYVviyCTMoNVPFh53oTuqvSy7R9GLI9iHk782.json',
                        '0ULssRK1xnbYVviyCTMoNVPFh53oTuqvSy7R9GLI9iHk782.json'
                    ],
                    'title': {
                        'title': 'Old west photography',
                        'genres': ['photography', 'long exposure']
                    },
                    'credits': {
                        'role': 'photographer',
                        'artist': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json'
                    },
                    'tags': ['black and white', 'long exposure', 'star trails']
                }
            ]
        }
    }


#
# music
#

# SongId = Annotated[MongoId, id_schema('a string representing a song id')]
# SongCid = Annotated[ContentIdType, id_schema('a string representing a song content id')]

# class Song(ContentModel):
#     MONGO_COLLECTION_NAME: ClassVar[str] = 'songs'

#     id: SongId = Field(**db_id_kwargs)
#     cid: SongCid = Field(**cid_kwargs)

#     title: TitleData
#     audio: AnyAudioRelease
#     tags: conset(str, max_length=10)
#     music_video: Optional[AnyVideoRelease]
#     cover_artwork: Optional[AnyImageRelease]
#     other_artwork: Optional[conset(AnyRelease, min_length=0, max_length=25)]
#     lyrics: Optional[AnyTextDocumentRelease]

    
# class AlbumType(StrEnum):
#     album = 'album'
#     ep = 'ep'


# AlbumId = Annotated[MongoId, id_schema('a string representing an album id')]
# AlbumCid = Annotated[ContentIdType, id_schema('a string representing an album content id')]

# class Album(ContentModel):
#     MONGO_COLLECTION_NAME: ClassVar[str] = 'albums'

#     id: AlbumId = Field(**db_id_kwargs)
#     cid: AlbumCid = Field(**cid_kwargs)

#     title: TitleData
#     type: AlbumType
#     tags: conset(str, max_length=10)
#     songs: conset(Song, min_length=2, max_length=50)
#     cover_artwork: Optional[AnyImageRelease]
#     other_artwork: Optional[conset(AnyRelease, min_length=0, max_length=25)]









###########################################



#
# art primatives
#



# # audio #

    
# AudioReleaseId = Annotated[MongoId, id_schema('a string representing an audio release id')]
# AudioReleaseCid = Annotated[ContentIdType, id_schema('a string representing an audio release id')]

# class AudioRelease(ContentModel):
#     MONGO_COLLECTION_NAME: ClassVar[str] = 'audio_release'

#     id: AudioReleaseId = Field(**db_id_kwargs)
#     cid: AudioReleaseCid = Field(**cid_kwargs)

#     title: TitleData
#     creator: Union[ArtistCid, ArtistGroupCid]
#     credits: conset(Credit, max_length=15)
#     tags: conset(str, max_length=10)

#     master: Union[AudioFile, AudioFileCid]
#     alt_formats: conset(Union[AudioFile, AudioFileCid], min_length=1, max_length=10)


# # video #


# VideoReleaseId = Annotated[MongoId, id_schema('a string representing a video release id')]
# VideoReleaseCid = Annotated[ContentIdType, id_schema('a string representing a video release id')]

# class VideoRelease(ContentModel):
#     MONGO_COLLECTION_NAME: ClassVar[str] = 'video_releases'

#     id: VideoReleaseId = Field(**db_id_kwargs)
#     cid: VideoReleaseCid = Field(**cid_kwargs)

#     title: TitleData
#     creator: Union[ArtistCid, ArtistGroupCid]
#     credits: conset(Credit, max_length=15)
#     tags: conset(str, max_length=10)

#     master: Union[VideoFile, VideoFileCid]
#     alt_formats: conset(Union[VideoFile, VideoFileCid], min_length=1, max_length=25)


# # text document #


# TextDocumentReleaseId = Annotated[MongoId, id_schema('a string representing a text document file id')]
# TextDocumentReleaseCid = Annotated[ContentIdType, id_schema('a string representing a text document file id')]

# class TextDocumentRelease(ContentModel):
#     MONGO_COLLECTION_NAME: ClassVar[str] = 'text_document_release'

#     id: TextDocumentReleaseId = Field(**db_id_kwargs)
#     cid: TextDocumentReleaseCid = Field(**cid_kwargs)

#     title: TitleData
#     creator: Union[ArtistCid, ArtistGroupCid]
#     credits: conset(Credit, max_length=15)
#     tags: conset(str, max_length=10)

#     master: Union[TextFile, TextFileCid]





# music #




# # video #

# class VideoProgramType(StrEnum):
#     feature = 'feature'
#     episode = 'episode'
#     short = 'short'


# VideoProgramId = Annotated[MongoId, id_schema('a string representing a video program id')]
# VideoProgramCid = Annotated[ContentIdType, id_schema('a string representing a video program content id')]

# class VideoProgram(ContentModel):
#     MONGO_COLLECTION_NAME: ClassVar[str] = 'video_programs'

#     id: VideoProgramId = Field(**db_id_kwargs)
#     cid: VideoProgramCid = Field(**cid_kwargs)

#     title: TitleData
#     program: AnyVideoRelease
#     type: VideoProgramType
#     tags: conset(str, max_length=10)
#     trailers: conset(Union[AnyAudioRelease, AnyVideoRelease], min_length=0, max_length=10)
#     cover_artwork: Optional[AnyImageRelease]
#     other_artwork: Optional[conset(AnyRelease, min_length=0, max_length=25)]


# VideoMiniSeriesId = Annotated[MongoId, id_schema('a string representing a video mini series id')]
# VideoMiniSeriesCid = Annotated[ContentIdType, id_schema('a string representing a video mini series content id')]

# class VideoMiniSeries(ContentModel):
#     MONGO_COLLECTION_NAME: ClassVar[str] = 'video_mini_series'

#     id: VideoMiniSeriesId = Field(**db_id_kwargs)
#     cid: VideoMiniSeriesCid = Field(**cid_kwargs)

#     title: TitleData
#     episodes: conset(VideoProgram, min_length=2, max_length=42)
#     trailers: conset(Union[AnyAudioRelease, AnyVideoRelease], min_length=0, max_length=10)
#     tags: conset(str, max_length=10)
#     cover_artwork: Optional[AnyImageRelease]
#     other_artwork: Optional[conset(AnyRelease, min_length=0, max_length=25)]


# VideoSeasonId = Annotated[MongoId, id_schema('a string representing a video season id')]
# VideoSeasonCid = Annotated[ContentIdType, id_schema('a string representing a video season content id')]

# class VideoSeason(ContentModel):
#     MONGO_COLLECTION_NAME: ClassVar[str] = 'video_seasons'

#     id: VideoSeasonId = Field(**db_id_kwargs)
#     cid: VideoSeasonCid = Field(**cid_kwargs)

#     title: TitleData
#     episodes: conset(VideoProgram, min_length=2, max_length=42)
#     trailers: conset(Union[AnyAudioRelease, AnyVideoRelease], min_length=0, max_length=10)
#     tags: conset(str, max_length=10)
#     cover_artwork: Optional[AnyImageRelease]
#     other_artwork: Optional[conset(AnyReleaseCid, min_length=0, max_length=25)]


# VideoEpisodicSeriesId = Annotated[MongoId, id_schema('a string representing a video episodic series id')]
# VideoEpisodicSeriesCid = Annotated[ContentIdType, id_schema('a string representing a video episodic series content id')]

# class VideoEpisodicSeries(ContentModel):
#     MONGO_COLLECTION_NAME: ClassVar[str] = 'video_episodic_series'

#     id: VideoEpisodicSeriesId = Field(**db_id_kwargs)
#     cid: VideoEpisodicSeriesCid = Field(**cid_kwargs)

#     title: TitleData
#     seasons: conset(VideoSeason, min_length=1, max_length=50)
#     trailers: conset(Union[AnyAudioRelease, AnyVideoRelease], min_length=0, max_length=10)
#     tags: conset(str, max_length=10)
#     cover_artwork: Optional[AnyImageRelease]
#     other_artwork: Optional[conset(AnyReleaseCid, min_length=0, max_length=25)]


# # podcast #


# PodcastProgramId = Annotated[MongoId, id_schema('a string representing a podcast program id')]
# PodcastProgramCid = Annotated[ContentIdType, id_schema('a string representing a podcast program content id')]

# class PodcastProgram(ContentModel):
#     MONGO_COLLECTION_NAME: ClassVar[str] = 'podcast_program'

#     id: PodcastProgramId = Field(**db_id_kwargs)
#     cid: PodcastProgramCid = Field(**cid_kwargs)

#     title: TitleData
#     program: AnyAudioRelease
#     trailers: conset(AnyAudioRelease, min_length=0, max_length=10)
#     tags: conset(str, max_length=10)
#     cover_artwork: Optional[AnyImageRelease]
#     other_artwork: Optional[conset(AnyReleaseCid, min_length=0, max_length=25)]


# PodcastSeriesId = Annotated[MongoId, id_schema('a string representing a podcast series id')]
# PodcastSeriesCid = Annotated[ContentIdType, id_schema('a string representing a podcast series content id')]

# class PodcastSeries(ContentModel):
#     MONGO_COLLECTION_NAME: ClassVar[str] = 'podcast_series'

#     id: PodcastSeriesId = Field(**db_id_kwargs)
#     cid: PodcastSeriesCid = Field(**cid_kwargs)

#     title: TitleData
#     episodes: conset(PodcastProgram, min_length=2, max_length=42)
#     trailers: conset(AnyAudioRelease, min_length=0, max_length=10)
#     tags: conset(str, max_length=10)
#     cover_artwork: Optional[AnyImageRelease]
#     other_artwork: Optional[conset(AnyReleaseCid, min_length=0, max_length=25)]


# PodcastSeasonId = Annotated[MongoId, id_schema('a string representing a podcast season id')]
# PodcastSeasonCid = Annotated[ContentIdType, id_schema('a string representing a podcast season content id')]

# class PodcastSeason(ContentModel):
#     MONGO_COLLECTION_NAME: ClassVar[str] = 'podcast_season'

#     id: PodcastSeasonId = Field(**db_id_kwargs)
#     cid: PodcastSeasonCid = Field(**cid_kwargs)

#     title: TitleData
#     episodes: conset(PodcastProgram, min_length=2, max_length=42)
#     trailers: conset(AnyAudioRelease, min_length=0, max_length=10)
#     tags: conset(str, max_length=10)
#     cover_artwork: Optional[AnyImageRelease]
#     other_artwork: Optional[conset(AnyReleaseCid, min_length=0, max_length=25)]


# PodcastEpisodicSeriesId = Annotated[MongoId, id_schema('a string representing a podcast episodic series id')]
# PodcastEpisodicSeriesCid = Annotated[ContentIdType, id_schema('a string representing a podcast episodic series content id')]

# class PodcastEpisodicSeries(ContentModel):
#     MONGO_COLLECTION_NAME: ClassVar[str] = 'podcast_episodic_series'

#     id: PodcastEpisodicSeriesId = Field(**db_id_kwargs)
#     cid: PodcastEpisodicSeriesCid = Field(**cid_kwargs)

#     title: TitleData
#     seasons: conset(PodcastProgram, min_length=1, max_length=50)
#     trailers: conset(AnyAudioRelease, min_length=0, max_length=10)
#     tags: conset(str, max_length=10)
#     cover_artwork: Optional[AnyImageRelease]
#     other_artwork: Optional[conset(AnyReleaseCid, min_length=0, max_length=25)]


# # text publication #


# class TextPublicationType(StrEnum):
#     article = 'article'
#     blog = 'blog'
#     essay = 'essay'
#     lyrics = 'lyrics'
#     press_release = 'press_release'
#     poetry = 'poetry'
#     script = 'script'
#     transcript = 'transcript'
#     news = 'news'


# TextEntryId = Annotated[MongoId, id_schema('a string representing a text entry id')]
# TextEntryCid = Annotated[ContentIdType, id_schema('a string representing a text entry content id')]

# class TextEntry(ContentModel):
#     MONGO_COLLECTION_NAME: ClassVar[str] = 'text_entries'

#     id: TextEntryId = Field(**db_id_kwargs)
#     cid: TextEntryCid = Field(**cid_kwargs)

#     title: TitleData
#     type: TextPublicationType
#     document: AnyTextDocumentRelease
#     tags: conset(str, max_length=10)


# TextSeriesId = Annotated[MongoId, id_schema('a string representing a text series id')]
# TextSeriesCid = Annotated[ContentIdType, id_schema('a string representing a text series content id')]

# class TextSeries(ContentModel):
#     MONGO_COLLECTION_NAME: ClassVar[str] = 'text_series'

#     id: TextSeriesId = Field(**db_id_kwargs)
#     cid: TextSeriesCid = Field(**cid_kwargs)

#     title: TitleData
#     type: TextPublicationType
#     documents: conset(TextEntry, min_length=2, max_length=42)
#     tags: conset(str, max_length=10)


# TextPublicationId = Annotated[MongoId, id_schema('a string representing a text publication id')]
# TextPublicationCid = Annotated[ContentIdType, id_schema('a string representing a text publication content id')]

# class TextPublication(ContentModel):
#     MONGO_COLLECTION_NAME: ClassVar[str] = 'blogs'

#     id: TextPublicationId = Field(**db_id_kwargs)
#     cid: TextPublicationCid = Field(**cid_kwargs)

#     title: TitleData
#     type: TextPublicationType
#     series: conset(TextSeries, min_length=1)
#     tags: conset(str, max_length=10)


# if __name__ == '__main__':
#     import inspect

#     for key, value in inspect.get_annotations(VideoRelease).items():
#         try:
#             if issubclass(value.__args__[0].__class__, BaseModel.__class__):
#                 if value.__args__[1].__args__[0] is ContentIdType:
#                     print(key, value.__args__)
#         except (AttributeError, IndexError):
#             pass
