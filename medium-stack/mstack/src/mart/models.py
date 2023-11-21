from typing import Annotated, ClassVar, Union, Optional, Type, List
from enum import StrEnum
from pydantic import BaseModel, Field, conlist, model_validator

from mcore.types import TagList, unique_list_validator
from mcore.util import example_cid

from mcore.models import (
    MongoId, 
    ContentModel, 
    ContentIdType, 
    ModelCreator,
    User,
    UserCid,

    AnyImageRelease,
    AnyAudioFile,
    AnyAudioRelease,
    AnyVideoFile,
    AnyVideoRelease,
    AnyAVRelease,
    AnyTextFile,
    AnyRelease,

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
    'AnyArtist',
    'ArtistCreator',

    'ArtistGroupId',
    'ArtistGroupCid',
    'ArtistList',
    'ArtistGroup',
    'AnyArtistGroup',
    'ArtistGroupCreator',

    'Credit',
    'CreditList',
    'GenreList',
    'TitleData',

    'StillImageId',
    'StillImageCid',
    'StillImage',
    'StillImageCreator',

    'AnyStillImage',
    'StillImageAlbumId',
    'StillImageAlbumCid',
    'StillImageAlbum',
    'StillImageAlbumCreator',

    'SongId',
    'SongCid',
    'Song',
    'SongCreator',

    'MusicAlbumType',
    'AnySong',
    'MusicAlbumId',
    'MusicAlbumCid',
    'MusicAlbumSongList',
    'MusicAlbum',
    'MusicAlbumCreator',

    'PodcastEpisodeId',
    'PodcastEpisodeCid',
    'PodcastEpisode',
    'PodcastEpisodeCreator',
    'AnyPodcastEpisode',

    'PodcastSeasonId',
    'PodcastSeasonCid',
    'PodcastEpisodeList',
    'PodcastSeason',
    'PodcastSeasonCreator',
    'AnyPodcastSeason',

    'PodcastId',
    'PodcastCid',
    'PodcastSeasonList',
    'Podcast',
    'PodcastCreator',
    'AnyPodcast',

    'VideoProgramType',
    'VideoProgramId',
    'VideoProgramCid',
    'VideoProgram',
    'TrailerList',
    'VideoProgramCreator',
    'AnyVideoProgram',

    'VideoSeasonId',
    'VideoSeasonCid',
    'VideoEpisodeList',
    'VideoSeason',
    'VideoSeasonCreator',
    'AnyVideoSeason',

    'VideoMiniSeriesId',
    'VideoMiniSeriesCid',
    'VideoMiniSeries',
    'VideoMiniSeriesCreator',

    'VideoSeriesId',
    'VideoSeriesCid',
    'VideoSeasonList',
    'VideoSeries',
    'VideoSeriesCreator',
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
    API_PREFIX: ClassVar[str] = '/artists'

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
                    'user_cid': str(example_cid(User)),
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


AnyArtist = Union[Artist, ArtistCid]


class ArtistCreator(ModelCreator):

    MODEL: ClassVar[Type[Artist]] = Artist

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

ArtistList = Annotated[
    conlist(AnyArtist, min_length=1, max_length=50),
    unique_list_validator, 
    id_schema('a unique list of artist cids')
]

class ArtistGroup(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'artist_groups'
    API_PREFIX: ClassVar[str] = '/artist-groups'

    id: ArtistGroupId = Field(**db_id_kwargs)
    cid: ArtistGroupCid = Field(**cid_kwargs)
    user_cid: UserCid = Field(**cid_kwargs)

    name: str = Field(min_length=1, max_length=300)
    short_name: str = Field(min_length=1, max_length=50)
    abreviated_name: str = Field(max_length=10)

    summary: str = Field(min_length=1, max_length=300)
    description: str = Field(min_length=1, max_length=1500)
    mediums: ArtMediumList
    tags: TagList = None

    artists: ArtistList

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '0DuHIdrOYrCcHt2WMuBQP7-9xI6mp8sdeWRu8RnBjdTI752.json',
                    'user_cid': str(example_cid(User)),
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


AnyArtistGroup = Union[ArtistGroup, ArtistGroupCid]


class ArtistGroupCreator(ModelCreator):

    MODEL: ClassVar[Type[ArtistGroup]] = ArtistGroup

    name: str = Field(min_length=1, max_length=300)
    short_name: str = Field(min_length=1, max_length=50)
    abreviated_name: str = Field(max_length=10)

    summary: str = Field(min_length=1, max_length=300)
    description: str = Field(min_length=1, max_length=1500)
    mediums: ArtMediumList
    tags: TagList = None

    artists: ArtistList

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
    artist: AnyArtist

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


AnyMedia = Union[
    AnyRelease, 
    'AnyStillImage', 
    'AnyStillImageAlbum',
    'AnySong',
    'AnyMusicAlbum',
    'AnyVideoProgram',
    'AnyPodcastEpisode',
    'AnyPodcastSeason',
    'AnyPodcast',
]

CreditList = Annotated[
    conlist(Credit, min_length=1, max_length=100), 
    unique_list_validator, 
    id_schema('a unique list of credits')
]

GenreList = Annotated[
    conlist(str, min_length=1, max_length=5),
    unique_list_validator, 
    id_schema('a unique list of genres')
]

TrailerList = Annotated[
    None | conlist(AnyAVRelease, min_length=1, max_length=10),
    unique_list_validator,
    id_schema('a unique list of video or audio file cids')
]

OtherArtworkList = Annotated[
    None | conlist(AnyMedia, min_length=1, max_length=25),
    unique_list_validator, 
    id_schema('a unique list of media cids')
]


class TitleData(BaseModel):

    title: str = Field(min_length=1, max_length=300)
    short_title: Optional[str] = Field(None, max_length=50)
    abreviated_title: Optional[str] = Field(None, max_length=10)

    subtitle: Optional[str] = Field(None, max_length=500)
    summary: Optional[str] = Field(None, min_length=1, max_length=300)
    description: Optional[str] = Field(None, min_length=1, max_length=1500)

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': 'Rubber Soul'
                },
                {
                    'title': 'Rubber Soul',
                    'short_title': 'Rubber Soul',
                    'abreviated_title': 'RS',
                    'subtitle': 'By The Beatles',
                    'summary': 'Sixth studio album by the English rock band the Beatles.',
                    'description': 'Rubber Soul is the sixth studio album by the English rock band the Beatles.'
                }
            ]
        }
    }


#
# still image art
#

StillImageId = Annotated[MongoId, id_schema('a string representing a still image id')]
StillImageCid = Annotated[ContentIdType, id_schema('a string representing a still image id')]


class StillImage(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'still_image'

    id: StillImageId = Field(**db_id_kwargs)
    cid: StillImageCid = Field(**cid_kwargs)

    creator_id: AnyArtist

    release: AnyImageRelease

    title: Optional[TitleData]
    credits: Optional[Credit]
    genres: GenreList
    tags: TagList
    album: Optional['AnyStillImageAlbum']

    alt_text: Optional[str]

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '0ajFSQpuyKrubp4oGAhuAVS9LQtJ-TYuTdPkE-vnoaQA576.json',
                    'creator_id': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'release': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'title': {
                        'title': 'My cool Painting'
                    },
                    'credits': {
                        'role': 'painter',
                        'artist': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json'
                    },
                    'genres': ['surrealism', 'painting'],
                    'tags': ['surrealism', 'painting', 'oil painting'],
                    'album': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'alt_text': 'a surrealistic oil painting'
                }
            ]
        }
    }


class StillImageCreator(ModelCreator):
    MODEL: ClassVar[Type[StillImage]] = StillImage

    creator_id: AnyArtist

    release: AnyImageRelease

    title: Optional[TitleData]
    credits: Optional[Credit]
    genres: GenreList
    tags: TagList
    album: Optional['AnyStillImageAlbum']

    alt_text: Optional[str]

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'creator_id': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'release': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'title': {
                        'title': 'My cool Painting'
                    },
                    'credits': {
                        'role': 'painter',
                        'artist': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json'
                    },
                    'genres': ['surrealism', 'painting'],
                    'tags': ['surrealism', 'painting', 'oil painting'],
                    'album': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'alt_text': 'a surrealistic oil painting'
                }
            ]
        }
    }


AnyStillImage = Union[StillImage, StillImageCid]

StillImageAlbumId = Annotated[MongoId, id_schema('a string representing a still image album id')]
StillImageAlbumCid = Annotated[ContentIdType, id_schema('a string representing a still image album content id')]


"""
the StillImage model references the StillImageAlbum model rather than the other way around so that
albums can be arbitrarily large without bloating the StillImage model. This allows for paginating queries.
"""


class StillImageAlbum(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'still_image_album'

    id: StillImageAlbumId = Field(**db_id_kwargs)
    cid: StillImageAlbumCid = Field(**cid_kwargs)

    creator_id: AnyArtist

    title: TitleData
    credits: Credit
    genres: GenreList
    tags: TagList

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '0FmUG7qtOMsnXZmePvg0SeI9ybzHgY2FUhxUFTRBmhw4425.json',
                    'creator_id': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'title': {
                        'title': 'Old west photography'
                    },
                    'credits': {
                        'role': 'photographer',
                        'artist': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json'
                    },
                    'genres': ['photography', 'long exposure'],
                    'tags': ['black and white', 'long exposure', 'star trails']
                }
            ]
        }
    }


AnyStillImageAlbum = Union[StillImageAlbum, StillImageAlbumCid]


class StillImageAlbumCreator(ModelCreator):
    MODEL: ClassVar[Type[StillImageAlbum]] = StillImageAlbum

    creator_id: AnyArtist

    title: TitleData
    credits: Credit
    genres: GenreList
    tags: TagList

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'creator_id': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'title': {
                        'title': 'Old west photography'
                    },
                    'credits': {
                        'role': 'photographer',
                        'artist': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json'
                    },
                    'genres': ['photography', 'long exposure'],
                    'tags': ['black and white', 'long exposure', 'star trails']
                }
            ]
        }
    }


#
# music
#


SongId = Annotated[MongoId, id_schema('a string representing a song id')]
SongCid = Annotated[ContentIdType, id_schema('a string representing a song content id')]

class Song(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'songs'

    id: SongId = Field(**db_id_kwargs)
    cid: SongCid = Field(**cid_kwargs)

    title: TitleData
    release: AnyAudioRelease
    genres: GenreList
    tags: TagList
    music_video: Optional['AnyVideoProgram']
    cover_artwork: Optional[AnyStillImage]
    other_artwork: OtherArtworkList
    lyrics: Optional[AnyTextFile]

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '01iEnTt6YHwLaaKTVu3zTWCvn54gXkWfpuSyDoVn68Nw613.json',
                    'title': {
                        'title': 'My cool Song'
                    },
                    'release': '0kjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json',
                    'genres': ['rock', 'blues'],
                    'tags': ['rock', 'blues', 'guitar'],
                    'music_video': '0kjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json',
                    'cover_artwork': '0kjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json',
                    'other_artwork': [
                        '0kjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json',
                        '0jjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json'
                    ],
                    'lyrics': '0kjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json'
                }
            ]
        }
    }


class SongCreator(ModelCreator):
    MODEL: ClassVar[Type[Song]] = Song

    title: TitleData
    release: AnyAudioRelease
    genres: GenreList
    tags: TagList
    music_video: Optional['AnyVideoProgram']
    cover_artwork: Optional[AnyStillImage]
    other_artwork: OtherArtworkList
    lyrics: Optional[AnyTextFile]

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': {
                        'title': 'My cool Song'
                    },
                    'release': '0kjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json',
                    'genres': ['rock', 'blues'],
                    'tags': ['rock', 'blues', 'guitar'],
                    'music_video': '0kjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json',
                    'cover_artwork': '0kjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json',
                    'other_artwork': [
                        '0kjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json',
                        '0jjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json'
                    ],
                    'lyrics': '0kjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json'
                }
            ]
        }
    }


class MusicAlbumType(StrEnum):
    album = 'album'
    ep = 'ep'

AnySong = Union[Song, SongCid]

MusicAlbumId = Annotated[MongoId, id_schema('a string representing a music album id')]
MusicAlbumCid = Annotated[ContentIdType, id_schema('a string representing a music album content id')]

MusicAlbumSongList = Annotated[
    conlist(AnySong, min_length=1, max_length=50),
    unique_list_validator, 
    id_schema('a unique list of artist cids')
]

class MusicAlbum(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'music_albums'

    id: MusicAlbumId = Field(**db_id_kwargs)
    cid: MusicAlbumCid = Field(**cid_kwargs)

    title: TitleData
    type: MusicAlbumType
    genres: GenreList
    tags: TagList
    songs: MusicAlbumSongList
    cover_artwork: Optional[AnyStillImage]
    other_artwork: OtherArtworkList

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    'title': {
                        'title': 'My cool Album'
                    },
                    'type': 'ep',
                    'genres': ['rock', 'blues'],
                    'tags': ['rock', 'blues', 'guitar'],
                    'songs': [
                        '0kjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json',
                        '0jjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json'
                    ],
                    'cover_artwork': '0kjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json',
                    'other_artwork': [
                        '0kjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json',
                        '0jjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json'
                    ]
                }
            ]
        }
    }

AnyMusicAlbum = Union[MusicAlbum, MusicAlbumCid]


class MusicAlbumCreator(ModelCreator):
    MODEL: ClassVar[Type[MusicAlbum]] = MusicAlbum

    title: TitleData
    type: MusicAlbumType
    genres: GenreList
    tags: TagList
    songs: MusicAlbumSongList
    cover_artwork: Optional[AnyStillImage]
    other_artwork: OtherArtworkList

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': {
                        'title': 'My cool Album'
                    },
                    'type': 'ep',
                    'genres': ['rock', 'blues'],
                    'tags': ['rock', 'blues', 'guitar'],
                    'songs': [
                        '0kjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json',
                        '0jjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json'
                    ],
                    'cover_artwork': '0kjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json',
                    'other_artwork': [
                        '0kjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json',
                        '0jjGMpCpqNxrV10G5CAbz3oXH2fmJBnoP2nsXfuGS7W4576.json'
                    ]
                }
            ]
        }
    }


#
# podcast
#

# podcast episode #

PodcastEpisodeId = Annotated[MongoId, id_schema('a string representing a podcast program id')]
PodcastEpisodeCid = Annotated[ContentIdType, id_schema('a string representing a podcast program content id')]

class PodcastEpisode(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'podcast_episode'

    id: PodcastEpisodeId = Field(**db_id_kwargs)
    cid: PodcastEpisodeCid = Field(**cid_kwargs)

    title: TitleData
    podcast: 'AnyPodcast'

    program_audio: Optional[AnyAudioRelease] = None
    program_video: Optional[AnyVideoRelease] = None

    genres: GenreList
    trailers: TrailerList
    tags: TagList
    cover_artwork: Optional[AnyImageRelease] = None
    other_artwork: OtherArtworkList = None

    @model_validator(mode='after')
    def has_an_episode(self) -> 'PodcastEpisode':
        if self.program_audio is None and self.program_video is None:
            raise ValueError('must provide either an audio or video program')
        return self

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '0hx6NJx4sZqTRra4aaOIvAacQHsHFXYWKd27F3CmXZ_c633.json',
                    'title': {
                        'title': 'My cool Episode'
                    },
                    'podcast': '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    'program_audio': '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    'program_video': '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    'genres': ['politics', 'news'],
                    'trailers': [
                        '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    ],
                    'tags': ['us', 'election'],
                    'cover_artwork': '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    'other_artwork': [
                        '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    ]
                }
            ]
        }
    }

AnyPodcastEpisode = Union[PodcastEpisode, PodcastEpisodeCid]

class PodcastEpisodeCreator(ModelCreator):
    MODEL: ClassVar[Type[PodcastEpisode]] = PodcastEpisode

    title: TitleData
    podcast: 'AnyPodcast'

    program_audio: Optional[AnyAudioRelease] = None
    program_video: Optional[AnyVideoRelease] = None
    
    genres: GenreList
    trailers: TrailerList = None
    tags: TagList
    cover_artwork: Optional[AnyImageRelease] = None
    other_artwork: OtherArtworkList = None

    @model_validator(mode='after')
    def has_an_episode(self) -> 'PodcastEpisodeCreator':
        if self.program_audio is None and self.program_video is None:
            raise ValueError('must provide either an audio or video program')
        return self

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': {
                        'title': 'My cool Episode'
                    },
                    'podcast': '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    'program_audio': '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    'program_video': '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    'genres': ['politics', 'news'],
                    'trailers': [
                        '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    ],
                    'tags': ['us', 'election'],
                    'cover_artwork': '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    'other_artwork': [
                        '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    ]
                }
            ]
        }
    }

PodcastEpisodeList = Annotated[
    None | conlist(AnyPodcastEpisode, min_length=1, max_length=100),
    unique_list_validator, 
    id_schema('a unique list of podcast episode cids')
]

# podcast season #

PodcastSeasonId = Annotated[MongoId, id_schema('a string representing a podcast season id')]
PodcastSeasonCid = Annotated[ContentIdType, id_schema('a string representing a podcast season content id')]

class PodcastSeason(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'podcast_season'

    id: PodcastSeasonId = Field(**db_id_kwargs)
    cid: PodcastSeasonCid = Field(**cid_kwargs)

    title: TitleData
    episodes: PodcastEpisodeList = None
    trailers: TrailerList = None
    tags: TagList
    cover_artwork: Optional[AnyImageRelease] = None
    other_artwork: OtherArtworkList = None

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '0cLJq23m8Vpag8kWVW3CBYF1VfKqbu6Cr94lSEDDCGYw457.json',
                    'title': {
                        'title': 'My cool Season'
                    },
                    'episodes': [
                        '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    ],
                    'trailers': [
                        '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    ],
                    'tags': ['us', 'election'],
                    'cover_artwork': '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    'other_artwork': [
                        '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    ]
                }
            ]
        }
    }

AnyPodcastSeason = Union[PodcastSeason, PodcastSeasonCid]

class PodcastSeasonCreator(ModelCreator):
    MODEL: ClassVar[Type[PodcastSeason]] = PodcastSeason

    title: TitleData
    episodes: PodcastEpisodeList = None
    trailers: TrailerList = None
    tags: TagList
    cover_artwork: Optional[AnyImageRelease] = None
    other_artwork: OtherArtworkList = None

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': {
                        'title': 'My cool Season'
                    },
                    'episodes': [
                        '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    ],
                    'trailers': [
                        '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    ],
                    'tags': ['us', 'election'],
                    'cover_artwork': '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    'other_artwork': [
                        '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    ]
                }
            ]
        }
    }


PodcastSeasonList = Annotated[
    None | conlist(AnyPodcastSeason, min_length=1, max_length=100),
    unique_list_validator, 
    id_schema('a unique list of podcast season cids')
]

# podcast #

PodcastId = Annotated[MongoId, id_schema('a string representing a podcast id')]
PodcastCid = Annotated[ContentIdType, id_schema('a string representing a podcast content id')]

class Podcast(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'podcast'

    id: PodcastId = Field(**db_id_kwargs)
    cid: PodcastCid = Field(**cid_kwargs)

    title: TitleData
    seasons: PodcastSeasonList = None
    trailers: TrailerList = None
    tags: TagList
    cover_artwork: Optional[AnyImageRelease] = None
    other_artwork: OtherArtworkList = None

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '0AZzUOZfdK0gdYoOjfQ2l4EFJ1Q-lLlrCX68-xzD-n_8457.json',
                    'title': {
                        'title': 'My cool Podcast'
                    },
                    'seasons': [
                        '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    ],
                    'trailers': [
                        '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    ],
                    'tags': ['us', 'election'],
                    'cover_artwork': '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    'other_artwork': [
                        '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    ]
                }
            ]
        }
    }

AnyPodcast = Union[Podcast, PodcastCid]


class PodcastCreator(ModelCreator):
    MODEL: ClassVar[Type[Podcast]] = Podcast

    title: TitleData
    seasons: PodcastSeasonList = None
    trailers: TrailerList = None
    tags: TagList
    cover_artwork: Optional[AnyImageRelease] = None
    other_artwork: OtherArtworkList = None

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': {
                        'title': 'My cool Podcast'
                    },
                    'seasons': [
                        '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    ],
                    'trailers': [
                        '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    ],
                    'tags': ['us', 'election'],
                    'cover_artwork': '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    'other_artwork': [
                        '0zL8fq9j_lPNf6xg8Z3V6djjsPtoOnPFqI-FzirbWDCk547.json',
                    ]
                }
            ]
        }
    }


#
# video
#

# video program #

class VideoProgramType(StrEnum):
    feature = 'feature'
    episode = 'episode'
    short = 'short'
    trailer = 'trailer'
    music_Video = 'music_video'

VideoProgramId = Annotated[MongoId, id_schema('a string representing a video program id')]
VideoProgramCid = Annotated[ContentIdType, id_schema('a string representing a video program content id')]

class VideoProgram(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'video_programs'

    id: VideoProgramId = Field(**db_id_kwargs)
    cid: VideoProgramCid = Field(**cid_kwargs)

    title: TitleData
    type: VideoProgramType

    release: AnyVideoRelease
    
    trailers: TrailerList = None
    cover_artwork: Optional[AnyStillImage]
    other_artwork: OtherArtworkList
    genres: GenreList
    tags: TagList

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '03aVCqkWiBKUrvhELCXDYPaZmsptLZ8uGxDGbWDK4SiM639.json',
                    'title': {
                        'title': 'My cool Movie'
                    },
                    'type': 'feature',
                    'release': '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                    'trailers': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json'
                    ],
                    'cover_artwork': '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                    'other_artwork': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json'
                    ],
                    'genres': ['drama', 'thriller'],
                    'tags': ['best actress', 'academy award winner']
                }
            ]
        }
    }


class VideoProgramCreator(ModelCreator):
    MODEL: ClassVar[Type[VideoProgram]] = VideoProgram

    title: TitleData
    type: VideoProgramType

    release: AnyVideoRelease
    
    trailers: TrailerList = None
    cover_artwork: Optional[AnyStillImage]
    other_artwork: OtherArtworkList
    genres: GenreList
    tags: TagList

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': {
                        'title': 'My cool Movie'
                    },
                    'type': 'feature',
                    'release': '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                    'trailers': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json'
                    ],
                    'cover_artwork': '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                    'other_artwork': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json'
                    ],
                    'genres': ['drama', 'thriller'],
                    'tags': ['best actress', 'academy award winner']
                }
            ]
        }
    }


AnyVideoProgram = Union[VideoProgram, VideoProgramCid]

# video season #

VideoSeasonId = Annotated[MongoId, id_schema('a string representing a video season id')]
VideoSeasonCid = Annotated[ContentIdType, id_schema('a string representing a video season content id')]

VideoEpisodeList = Annotated[
    conlist(AnyVideoProgram, min_length=1, max_length=50),
    unique_list_validator, 
    id_schema('a unique list of video program cids')
]

class VideoSeason(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'video_seasons'

    id: VideoSeasonId = Field(**db_id_kwargs)
    cid: VideoSeasonCid = Field(**cid_kwargs)

    title: TitleData
    episodes: VideoEpisodeList
    trailers: TrailerList = None
    genres: GenreList
    tags: TagList
    cover_artwork: Optional[AnyStillImage]
    other_artwork: OtherArtworkList

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '0x7m9XjJQ_xlvhBmmwu2ylYr_3SZTBW4taBsBumhHb6U670.json',
                    'title': {
                        'title': 'My cool Season'
                    },
                    'episodes': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json'
                    ],
                    'trailers': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json'
                    ],
                    'genres': ['drama', 'thriller'],
                    'tags': ['award winner', 'best actor'],
                    'cover_artwork': '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                    'other_artwork': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json'
                    ]
                }
            ]
        }
    }


class VideoSeasonCreator(ModelCreator):
    MODEL: ClassVar[Type[VideoSeason]] = VideoSeason

    title: TitleData
    episodes: VideoEpisodeList
    trailers: TrailerList = None
    genres: GenreList
    tags: TagList
    cover_artwork: Optional[AnyStillImage]
    other_artwork: OtherArtworkList

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': {
                        'title': 'My cool Season'
                    },
                    'episodes': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json'
                    ],
                    'trailers': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json'
                    ],
                    'genres': ['drama', 'thriller'],
                    'tags': ['award winner', 'best actor'],
                    'cover_artwork': '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                    'other_artwork': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json'
                    ]
                }
            ]
        }
    }


AnyVideoSeason = Union[VideoSeason, VideoSeasonCid]

# single season series #

VideoMiniSeriesId = Annotated[MongoId, id_schema('a string representing a video mini series id')]
VideoMiniSeriesCid = Annotated[ContentIdType, id_schema('a string representing a video mini series content id')]

class VideoMiniSeries(VideoSeason):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'video_mini_series'

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '0-UqowlTPqw00LvKaoeFT7kwJiiyzH_0SBZ-FMAqkN1k687.json',
                    'title': {
                        'title': 'My Docuseries'
                    },
                    'episodes': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json'
                    ],
                    'trailers': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json'
                    ],
                    'genres': ['documentary', 'investigative'],
                    'tags': ['crowd funded', 'indy award winner'],
                    'cover_artwork': '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                    'other_artwork': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json'
                    ]
                }
            ]
        }
    }


class VideoMiniSeriesCreator(VideoSeasonCreator):
    MODEL: ClassVar[Type[VideoMiniSeries]] = VideoMiniSeries

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': {
                        'title': 'My Docuseries'
                    },
                    'episodes': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json'
                    ],
                    'trailers': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json'
                    ],
                    'genres': ['documentary', 'investigative'],
                    'tags': ['crowd funded', 'indy award winner'],
                    'cover_artwork': '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                    'other_artwork': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfcs134.json'
                    ]
                }
            ]
        }
    }

# video episodic series #

VideoSeriesId = Annotated[MongoId, id_schema('a string representing a video series id')]
VideoSeriesCid = Annotated[ContentIdType, id_schema('a string representing a video series content id')]

VideoSeasonList = Annotated[
    conlist(AnyVideoSeason, min_length=1, max_length=50),
    unique_list_validator,
    id_schema('a unique list of video season cids')
]

class VideoSeries(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'video_series'

    id: VideoSeriesId = Field(**db_id_kwargs)
    cid: VideoSeriesCid = Field(**cid_kwargs)

    title: TitleData
    seasons: VideoSeasonList
    trailers: TrailerList = None
    genres: GenreList
    tags: TagList
    cover_artwork: Optional[AnyStillImage]
    other_artwork: OtherArtworkList

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '0jJ1CqRH89rLHILbeG_W8GvZ3l4GB7gzEkfnZYHuo97Y546.json',
                    'title': {
                        'title': 'My Sitcom'
                    },
                    'seasons': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfc134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfc134.json'
                    ],
                    'trailers': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfc134.json',
                    ],
                    'genres': ['comedy', 'sitcom'],
                    'tags': ['award winner', 'best actor'],
                    'cover_artwork': '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfc134.json',
                    'other_artwork': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfc134.json',
                    ]
                }
            ]
        }
    }


class VideoSeriesCreator(ModelCreator):
    MODEL: ClassVar[Type[VideoSeries]] = VideoSeries

    title: TitleData
    seasons: VideoSeasonList
    trailers: TrailerList = None
    genres: GenreList
    tags: TagList
    cover_artwork: Optional[AnyStillImage]
    other_artwork: OtherArtworkList

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': {
                        'title': 'My Sitcom'
                    },
                    'seasons': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfc134.json',
                        '0X-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfc134.json'
                    ],
                    'trailers': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfc134.json',
                    ],
                    'genres': ['comedy', 'sitcom'],
                    'tags': ['award winner', 'best actor'],
                    'cover_artwork': '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfc134.json',
                    'other_artwork': [
                        '0W-cnbvjGdsrkMwP-nrFbd3Is3k6rXakqL3vw9h1Hfc134.json',
                    ]
                }
            ]
        }
    }




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
