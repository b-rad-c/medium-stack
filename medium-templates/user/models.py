from typing import Annotated, ClassVar, Union, Optional, Type
from enum import StrEnum
import random

from pydantic import BaseModel, Field, conlist, model_validator
from lorem_text import lorem

from mcore.types import TagList, unique_list_validator
from mcore.util import example_cid, adjectives, nouns, art_genres

from mcore.models import (
    MongoId, 
    ContentModel, 
    ContentIdType, 
    ModelCreator,
    User,
    UserCreator,
    UserCid,
    
    ImageReleaseCid,
    AudioReleaseCid,
    VideoReleaseCid,
    TextFileCid,
    AnyAVReleaseCid,

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
    'ArtistList',
    'ArtistGroup',
    'ArtistGroupCreator',

    'Credit',
    'CreditList',
    'GenreList',
    'TitleData',

    'StillImageId',
    'StillImageCid',
    'StillImage',
    'StillImageCreator',

    'StillImageAlbumId',
    'StillImageAlbumCid',
    'StillImageAlbum',
    'StillImageAlbumCreator',

    'VideoProgramType',
    'VideoProgramId',
    'VideoProgramCid',
    'VideoProgram',
    'TrailerList',
    'VideoProgramCreator',

    'VideoSeasonId',
    'VideoSeasonCid',
    'VideoEpisodeList',
    'VideoSeason',
    'VideoSeasonCreator',

    'VideoMiniSeriesId',
    'VideoMiniSeriesCid',
    'VideoMiniSeries',
    'VideoMiniSeriesCreator',

    'VideoSeriesId',
    'VideoSeriesCid',
    'VideoSeasonList',
    'VideoSeries',
    'VideoSeriesCreator',

    'SongId',
    'SongCid',
    'Song',
    'SongCreator',

    'MusicAlbumType',
    'MusicAlbumId',
    'MusicAlbumCid',
    'MusicAlbumSongList',
    'MusicAlbum',
    'MusicAlbumCreator',

    'PodcastEpisodeId',
    'PodcastEpisodeCid',
    'PodcastEpisode',
    'PodcastEpisodeCreator',

    'PodcastSeasonId',
    'PodcastSeasonCid',
    'PodcastEpisodeList',
    'PodcastSeason',
    'PodcastSeasonCreator',

    'PodcastId',
    'PodcastCid',
    'PodcastSeasonList',
    'Podcast',
    'PodcastCreator'
]

#
# ids
#

ArtistId = Annotated[MongoId, id_schema('a string representing an artist id')]
ArtistCid = Annotated[ContentIdType, id_schema('a string representing an artist content id')]
ArtistGroupId = Annotated[MongoId, id_schema('a string representing an artist group id')]
ArtistGroupCid = Annotated[ContentIdType, id_schema('a string representing an artist content id')]
AnyArtistCid = ArtistCid | ArtistGroupCid

StillImageId = Annotated[MongoId, id_schema('a string representing a still image id')]
StillImageCid = Annotated[ContentIdType, id_schema('a string representing a still image id')]
StillImageAlbumId = Annotated[MongoId, id_schema('a string representing a still image album id')]
StillImageAlbumCid = Annotated[ContentIdType, id_schema('a string representing a still image album content id')]

PodcastEpisodeId = Annotated[MongoId, id_schema('a string representing a podcast program id')]
PodcastEpisodeCid = Annotated[ContentIdType, id_schema('a string representing a podcast program content id')]
PodcastSeasonId = Annotated[MongoId, id_schema('a string representing a podcast season id')]
PodcastSeasonCid = Annotated[ContentIdType, id_schema('a string representing a podcast season content id')]
PodcastId = Annotated[MongoId, id_schema('a string representing a podcast id')]
PodcastCid = Annotated[ContentIdType, id_schema('a string representing a podcast content id')]

VideoProgramId = Annotated[MongoId, id_schema('a string representing a video program id')]
VideoProgramCid = Annotated[ContentIdType, id_schema('a string representing a video program content id')]
VideoSeasonId = Annotated[MongoId, id_schema('a string representing a video season id')]
VideoSeasonCid = Annotated[ContentIdType, id_schema('a string representing a video season content id')]
VideoMiniSeriesId = Annotated[MongoId, id_schema('a string representing a video mini series id')]
VideoMiniSeriesCid = Annotated[ContentIdType, id_schema('a string representing a video mini series content id')]
VideoSeriesId = Annotated[MongoId, id_schema('a string representing a video series id')]
VideoSeriesCid = Annotated[ContentIdType, id_schema('a string representing a video series content id')]

SongId = Annotated[MongoId, id_schema('a string representing a song id')]
SongCid = Annotated[ContentIdType, id_schema('a string representing a song content id')]
MusicAlbumId = Annotated[MongoId, id_schema('a string representing a music album id')]
MusicAlbumCid = Annotated[ContentIdType, id_schema('a string representing a music album content id')]

AnyMediaCid = Union[
    AudioReleaseCid,
    VideoReleaseCid,
    ImageReleaseCid,
    TextFileCid,
    StillImageCid,
    StillImageAlbumCid,
    PodcastEpisodeCid,
    PodcastSeasonCid,
    PodcastCid,
    VideoProgramCid,
    VideoSeasonCid,
    VideoMiniSeriesCid,
    VideoSeriesCid,
    SongCid,
    MusicAlbumCid
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


class Artist(ContentModel):
    SNAKE_CASE: ClassVar[str] = 'artist'
    DB_NAME: ClassVar[str] = 'artists'
    ENDPOINT: ClassVar[str] = '/artists'

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


class ArtistCreator(ModelCreator):
    """
    This class is used to create an Artist model, user_cid is not exposed because this model represents user input,
    the user_cid is added by the controller which uses the cid of the authenticated user.
    """

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

    @classmethod
    def generate(cls, user:User=None, mediums:ArtMediumList=None) -> 'ArtistCreator':
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

        if mediums is None:
            mediums = random.choices(list(ArtMedium), k=random.randint(1, 3))
            mediums = list(set(mediums))    # ensure is unique

        tags = random.choices(art_genres, k=random.randint(2, 7))
        tags = list(set(tags))

        return cls(
            name=name,
            short_name=short,
            abreviated_name=abreviated,
            summary=lorem.sentence()[0:300],
            description=lorem.paragraph()[0:1500],
            mediums=mediums,
            tags=tags
        )
            

ArtistList = Annotated[
    conlist(AnyArtistCid, min_length=1, max_length=50),
    unique_list_validator, 
    id_schema('a unique list of artist cids')
]

class ArtistGroup(ContentModel):
    SNAKE_CASE: ClassVar[str] = 'artist_group'
    DB_NAME: ClassVar[str] = 'artist_groups'
    ENDPOINT: ClassVar[str] = '/artist-groups'

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

    @classmethod
    def generate(cls, artist=None, **kwargs):
        # a list of various roles for artists in filmaking, photography, music and more
        if artist is None:
            artist = ArtistCreator.generate_model()

        roles = [
            'actor',
            'director',
            'camera op',
            'lighting technician',
            'musician',
            'assistant',
            'grip',
            'producer'
        ]
        return cls(role=random.choice(roles), artist=artist.cid, **kwargs)

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
    None | conlist(AnyAVReleaseCid, min_length=1, max_length=10),
    unique_list_validator,
    id_schema('a unique list of video or audio file cids')
]

OtherArtworkList = Annotated[
    None | conlist(AnyMediaCid, min_length=1, max_length=25),
    unique_list_validator, 
    id_schema('a unique list of media cids')
]


class TitleData(BaseModel):

    title: str = Field(min_length=1, max_length=300)                        # rename to TitleData.full
    short_title: Optional[str] = Field(None, max_length=50)                 # rename to TitleData.short
    abreviated_title: Optional[str] = Field(None, max_length=10)

    subtitle: Optional[str] = Field(None, max_length=500)
    summary: Optional[str] = Field(None, min_length=1, max_length=300)
    description: Optional[str] = Field(None, min_length=1, max_length=2500)

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

    @classmethod
    def generate(cls, **kwargs):
        title = lorem.words(random.randint(1, 8))[0:300]
        title_words = title.split(' ')
        short_title = f'{title_words[0]} {title_words[-1]}'
        abreviated_title = ''.join([word[0].capitalize() for word in title.split(' ')][0:10])
        return cls(
            title=title,
            short_title=short_title,
            abreviated_title=abreviated_title,
            subtitle=lorem.sentence()[0:500],
            summary=lorem.sentence()[0:300],
            description=lorem.paragraph()[0:1500],
            **kwargs
        )


#
# still image art
#


"""
the StillImage model references the StillImageAlbum model rather than the other way around so that
albums can be arbitrarily large without bloating the StillImage model. This allows for paginating queries.
"""


class StillImageAlbum(ContentModel):
    SNAKE_CASE: ClassVar[str] = 'still_image_album'
    DB_NAME: ClassVar[str] = 'still_image_album'
    ENDPOINT: ClassVar[str] = '/still-image-albums'

    id: StillImageAlbumId = Field(**db_id_kwargs)
    cid: StillImageAlbumCid = Field(**cid_kwargs)

    creator_id: AnyArtistCid

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


class StillImageAlbumCreator(ModelCreator):
    MODEL: ClassVar[Type[StillImageAlbum]] = StillImageAlbum

    creator_id: AnyArtistCid

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


class StillImage(ContentModel):
    SNAKE_CASE: ClassVar[str] = 'still_image'
    DB_NAME: ClassVar[str] = 'still_image'
    ENDPOINT: ClassVar[str] = '/still-images'

    id: StillImageId = Field(**db_id_kwargs)
    cid: StillImageCid = Field(**cid_kwargs)

    creator_id: ArtistCid

    release: ImageReleaseCid

    title: Optional[TitleData] = None
    credits: Optional[CreditList] = None
    genres: GenreList
    tags: TagList
    album: Optional[StillImageAlbumCid] = None

    alt_text: Optional[str]

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '6546a5cd1a209851b7136441',
                    'cid': '0VWImoAL2-xX9uHQtRrV6mr715UxoQxcgwMbfIWqeFK0578.json',
                    'creator_id': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'release': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'title': {
                        'title': 'My cool Painting'
                    },
                    'credits': [
                        {
                            'role': 'painter',
                            'artist': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json'
                        }
                    ],
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

    creator_id: ArtistCid

    release: ImageReleaseCid

    title: Optional[TitleData] = None
    credits: Optional[CreditList] = None
    genres: GenreList
    tags: TagList
    album: Optional[StillImageAlbumCid] = None

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
                    'credits': [
                        {
                            'role': 'painter',
                            'artist': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json'
                        }
                    ],
                    'genres': ['surrealism', 'painting'],
                    'tags': ['surrealism', 'painting', 'oil painting'],
                    'album': '0Ue5vZVoC3uxXZD3MTx1x9QbddAHNSqM25scwxG3RlAs707.json',
                    'alt_text': 'a surrealistic oil painting'
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


class VideoProgram(ContentModel):
    SNAKE_CASE: ClassVar[str] = 'video_program'
    DB_NAME: ClassVar[str] = 'video_programs'
    ENDPOINT: ClassVar[str] = '/video-programs'

    id: VideoProgramId = Field(**db_id_kwargs)
    cid: VideoProgramCid = Field(**cid_kwargs)

    title: TitleData
    type: VideoProgramType

    release: VideoReleaseCid
    
    trailers: TrailerList = None
    cover_artwork: Optional[StillImageCid] = None
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

    release: VideoReleaseCid
    
    trailers: TrailerList = None
    cover_artwork: Optional[StillImageCid] = None
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

# video season #

VideoEpisodeList = Annotated[
    conlist(VideoProgramCid, min_length=1, max_length=50),
    unique_list_validator, 
    id_schema('a unique list of video program cids')
]

class VideoSeason(ContentModel):
    SNAKE_CASE: ClassVar[str] = 'video_season'
    DB_NAME: ClassVar[str] = 'video_seasons'
    ENDPOINT: ClassVar[str] = '/video-seasons'

    id: VideoSeasonId = Field(**db_id_kwargs)
    cid: VideoSeasonCid = Field(**cid_kwargs)

    title: TitleData
    episodes: VideoEpisodeList
    trailers: TrailerList = None
    genres: GenreList
    tags: TagList
    cover_artwork: Optional[StillImageCid] = None
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
    cover_artwork: Optional[StillImageCid] = None
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

# single season series #

class VideoMiniSeries(VideoSeason):
    SNAKE_CASE: ClassVar[str] = 'video_mini_series'
    DB_NAME: ClassVar[str] = 'video_mini_series'
    ENDPOINT: ClassVar[str] = '/video-mini-series'

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

VideoSeasonList = Annotated[
    conlist(VideoSeasonCid, min_length=1, max_length=50),
    unique_list_validator,
    id_schema('a unique list of video season cids')
]

class VideoSeries(ContentModel):
    SNAKE_CASE: ClassVar[str] = 'video_series'
    DB_NAME: ClassVar[str] = 'video_series'
    ENDPOINT: ClassVar[str] = '/video-series'

    id: VideoSeriesId = Field(**db_id_kwargs)
    cid: VideoSeriesCid = Field(**cid_kwargs)

    title: TitleData
    seasons: VideoSeasonList
    trailers: TrailerList = None
    genres: GenreList
    tags: TagList
    cover_artwork: Optional[StillImageCid] = None
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
    cover_artwork: Optional[StillImageCid] = None
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


#
# music
#


class Song(ContentModel):
    SNAKE_CASE: ClassVar[str] = 'song'
    DB_NAME: ClassVar[str] = 'songs'
    ENDPOINT: ClassVar[str] = '/songs'

    id: SongId = Field(**db_id_kwargs)
    cid: SongCid = Field(**cid_kwargs)

    title: TitleData
    release: AudioReleaseCid
    genres: GenreList
    tags: TagList
    music_video: Optional[VideoProgramCid] = None
    cover_artwork: Optional[StillImageCid] = None
    other_artwork: OtherArtworkList
    lyrics: Optional[TextFileCid] = None

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
    release: AudioReleaseCid
    genres: GenreList
    tags: TagList
    music_video: Optional[VideoProgramCid] = None
    cover_artwork: Optional[StillImageCid] = None
    other_artwork: OtherArtworkList
    lyrics: Optional[TextFileCid] = None

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

MusicAlbumSongList = Annotated[
    conlist(SongCid, min_length=1, max_length=50),
    unique_list_validator, 
    id_schema('a unique list of artist cids')
]

class MusicAlbum(ContentModel):
    SNAKE_CASE: ClassVar[str] = 'music_album'
    DB_NAME: ClassVar[str] = 'music_albums'
    ENDPOINT: ClassVar[str] = '/music-albums'

    id: MusicAlbumId = Field(**db_id_kwargs)
    cid: MusicAlbumCid = Field(**cid_kwargs)

    title: TitleData
    type: MusicAlbumType
    genres: GenreList
    tags: TagList
    songs: MusicAlbumSongList
    cover_artwork: Optional[StillImageCid] = None
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


class MusicAlbumCreator(ModelCreator):
    MODEL: ClassVar[Type[MusicAlbum]] = MusicAlbum

    title: TitleData
    type: MusicAlbumType
    genres: GenreList
    tags: TagList
    songs: MusicAlbumSongList
    cover_artwork: Optional[StillImageCid] = None
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


class PodcastEpisode(ContentModel):
    SNAKE_CASE: ClassVar[str] = 'podcast_episode'
    DB_NAME: ClassVar[str] = 'podcast_episode'
    ENDPOINT: ClassVar[str] = '/podcast-episodes'

    id: PodcastEpisodeId = Field(**db_id_kwargs)
    cid: PodcastEpisodeCid = Field(**cid_kwargs)

    title: TitleData
    podcast: PodcastCid

    program_audio: Optional[AudioReleaseCid] = None
    program_video: Optional[VideoReleaseCid] = None

    genres: GenreList
    trailers: TrailerList
    tags: TagList
    cover_artwork: Optional[ImageReleaseCid] = None
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


class PodcastEpisodeCreator(ModelCreator):
    MODEL: ClassVar[Type[PodcastEpisode]] = PodcastEpisode

    title: TitleData
    podcast: PodcastCid

    program_audio: Optional[AudioReleaseCid] = None
    program_video: Optional[VideoReleaseCid] = None
    
    genres: GenreList
    trailers: TrailerList = None
    tags: TagList
    cover_artwork: Optional[ImageReleaseCid] = None
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
    None | conlist(PodcastEpisodeCid, min_length=1, max_length=100),
    unique_list_validator, 
    id_schema('a unique list of podcast episode cids')
]

# podcast season #

class PodcastSeason(ContentModel):
    SNAKE_CASE: ClassVar[str] = 'podcast_season'
    DB_NAME: ClassVar[str] = 'podcast_season'
    ENDPOINT: ClassVar[str] = '/podcast-seasons'

    id: PodcastSeasonId = Field(**db_id_kwargs)
    cid: PodcastSeasonCid = Field(**cid_kwargs)

    title: TitleData
    episodes: PodcastEpisodeList = None
    trailers: TrailerList = None
    tags: TagList
    cover_artwork: Optional[ImageReleaseCid] = None
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

class PodcastSeasonCreator(ModelCreator):
    MODEL: ClassVar[Type[PodcastSeason]] = PodcastSeason

    title: TitleData
    episodes: PodcastEpisodeList = None
    trailers: TrailerList = None
    tags: TagList
    cover_artwork: Optional[ImageReleaseCid] = None
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
    None | conlist(PodcastSeasonCid, min_length=1, max_length=100),
    unique_list_validator, 
    id_schema('a unique list of podcast season cids')
]

# podcast #

class Podcast(ContentModel):
    SNAKE_CASE: ClassVar[str] = 'podcast'
    DB_NAME: ClassVar[str] = 'podcast'
    ENDPOINT: ClassVar[str] = '/podcasts'

    id: PodcastId = Field(**db_id_kwargs)
    cid: PodcastCid = Field(**cid_kwargs)

    title: TitleData
    seasons: PodcastSeasonList = None
    trailers: TrailerList = None
    tags: TagList
    cover_artwork: Optional[ImageReleaseCid] = None
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


class PodcastCreator(ModelCreator):
    MODEL: ClassVar[Type[Podcast]] = Podcast

    title: TitleData
    seasons: PodcastSeasonList = None
    trailers: TrailerList = None
    tags: TagList
    cover_artwork: Optional[ImageReleaseCid] = None
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
