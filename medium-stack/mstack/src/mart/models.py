from typing import Annotated, ClassVar, Union, Optional, Type
from enum import StrEnum
from pydantic import BaseModel, Field, conlist, conset

from mcore.models import (
    MongoId, 
    ContentModel, 
    ContentId, 

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
    id_schema, 
    
)


#
# artist, credits, metadata
#


class ArtType(StrEnum):
    audio = 'audio'
    podcast = 'podcast'
    still = 'still'
    text = 'text'
    video = 'video'


ArtistId = Annotated[MongoId, id_schema('a string representing an artist id')]
ArtistCid = Annotated[ContentId, id_schema('a string representing an artist content id')]

class Artist(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'artists'

    id: ArtistId = Field(**db_id_kwargs)
    cid: ArtistCid = Field(**cid_kwargs)

    name: str = Field(min_length=1, max_length=300)
    short_name: str = Field(min_length=1, max_length=50)
    abreviated_name: str = Field(max_length=10)

    summary: str = Field(min_length=1, max_length=300)
    description: str = Field(min_length=1, max_length=1500)
    types: conset(ArtType)

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '',
                    'cid': '',
                    'name': 'Frida Kahlo',
                    'short_name': 'Kahlo',
                    'abreviated_name': 'FK',
                    'summary': 'Mexican painter known for her many portraits, self-portraits, and works inspired by the nature and artifacts of Mexico.',
                    'description': 'Frida Kahlo de Rivera was a Mexican artist who painted many portraits, self-portraits, and works inspired by the nature and artifacts of Mexico. Her work has been celebrated internationally as emblematic of Mexican national and indigenous traditions, and by feminists for its uncompromising depiction of the female experience and form.',
                    'types': ['still']
                }
            ]
        }
    }


class ArtistCreator(BaseModel):

    MODEL: ClassVar[Type[Artist]] = Artist

    name: str = Field(min_length=1, max_length=300)
    short_name: str = Field(min_length=1, max_length=50)
    abreviated_name: str = Field(max_length=10)
    summary: str = Field(min_length=1, max_length=300)
    description: str = Field(min_length=1, max_length=1500)
    types: conset(ArtType)

    MODEL = Artist  # This references the model that this Creator is for

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'name': 'Frida Kahlo',
                    'short_name': 'Kahlo',
                    'abreviated_name': 'FK',
                    'summary': 'Mexican painter known for her many portraits, self-portraits, and works inspired by the nature and artifacts of Mexico.',
                    'description': 'Frida Kahlo de Rivera was a Mexican artist who painted many portraits, self-portraits, and works inspired by the nature and artifacts of Mexico. Her work has been celebrated internationally as emblematic of Mexican national and indigenous traditions, and by feminists for its uncompromising depiction of the female experience and form.',
                    'types': ['still']
                }
            ]
        }
    }


ArtistGroupId = Annotated[MongoId, id_schema('a string representing an artist group id')]
ArtistGroupCid = Annotated[ContentId, id_schema('a string representing an artist content id')]

class ArtistGroup(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'artist_groups'

    id: ArtistGroupId = Field(**db_id_kwargs)
    cid: ArtistGroupCid = Field(**cid_kwargs)

    name: str = Field(min_length=1, max_length=300)
    short_name: str = Field(min_length=1, max_length=50)
    abreviated_name: str = Field(max_length=10)

    summary: str = Field(min_length=1, max_length=300)
    description: str = Field(min_length=1, max_length=1500)
    types: conset(ArtType)

    artists: conlist(Union[ArtistCid, ArtistGroupCid], min_length=1, max_length=50)


CreditId = Annotated[MongoId, id_schema('a string representing a credit id')]
CreditCid = Annotated[ContentId, id_schema('a string representing a credit content id')]

class Credit(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'credits'

    id: CreditId = Field(**db_id_kwargs)
    cid: CreditCid = Field(**cid_kwargs)

    job: str
    artist: ArtistCid


TitleDataId = Annotated[MongoId, id_schema('a string representing a title data id')]
TitleDataCid = Annotated[ContentId, id_schema('a string representing a title data content id')]

class TitleData(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'title_data'

    id: TitleDataId = Field(**db_id_kwargs)
    cid: TitleDataCid = Field(**cid_kwargs)

    title: str = Field(min_length=1, max_length=300)
    short_title: str = Field(max_length=50)
    abreviated_title: str = Field(max_length=10)

    subtitle: str = Field(str, max_length=500)
    summary: str = Field(str, min_length=1, max_length=300)
    description: str = Field(str, min_length=1, max_length=1500)
    genres: conset(str, min_length=1, max_length=4)


#
# art primatives
#


# image #


ImageReleaseId = Annotated[MongoId, id_schema('a string representing an image release id')]
ImageReleaseCid = Annotated[ContentId, id_schema('a string representing an image release id')]

class ImageRelease(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'image_release'

    id: ImageReleaseId = Field(**db_id_kwargs)
    cid: ImageReleaseCid = Field(**cid_kwargs)

    title: Optional[TitleData]
    creator: Union[ArtistCid, ArtistGroupCid]
    credits: conset(Credit, max_length=15)
    tags: conset(str, max_length=10)

    alt_text: Optional[str]

    master: Union[ImageFile, ImageFileCid]
    alt_formats: conlist(Union[ImageFile, ImageFileCid], min_length=1, max_length=10)


# audio #

    
AudioReleaseId = Annotated[MongoId, id_schema('a string representing an audio release id')]
AudioReleaseCid = Annotated[ContentId, id_schema('a string representing an audio release id')]

class AudioRelease(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'audio_release'

    id: AudioReleaseId = Field(**db_id_kwargs)
    cid: AudioReleaseCid = Field(**cid_kwargs)

    title: Optional[TitleData]
    creator: Union[ArtistCid, ArtistGroupCid]
    credits: conset(Credit, max_length=15)
    tags: conset(str, max_length=10)

    master: Union[AudioFile, AudioFileCid]
    alt_formats: conlist(Union[AudioFile, AudioFileCid], min_length=1, max_length=10)


# video #


VideoReleaseId = Annotated[MongoId, id_schema('a string representing a video release id')]
VideoReleaseCid = Annotated[ContentId, id_schema('a string representing a video release id')]

class VideoRelease(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'video_releases'

    id: VideoReleaseId = Field(**db_id_kwargs)
    cid: VideoReleaseCid = Field(**cid_kwargs)

    title: Optional[TitleData]
    creator: Union[ArtistCid, ArtistGroupCid]
    credits: conset(Credit, max_length=15)
    tags: conset(str, max_length=10)

    master: Union[VideoFile, VideoFileCid]
    alt_formats: conlist(Union[VideoFile, VideoFileCid], min_length=1, max_length=25)


# text document #


TextDocumentReleaseId = Annotated[MongoId, id_schema('a string representing a text document file id')]
TextDocumentReleaseCid = Annotated[ContentId, id_schema('a string representing a text document file id')]

class TextDocumentRelease(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'text_document_release'

    id: TextDocumentReleaseId = Field(**db_id_kwargs)
    cid: TextDocumentReleaseCid = Field(**cid_kwargs)

    title: Optional[TitleData]
    creator: Union[ArtistCid, ArtistGroupCid]
    credits: conset(Credit, max_length=15)
    tags: conset(str, max_length=10)

    master: Union[TextFile, TextFileCid]

AnyImageRelease = Union[ImageReleaseCid, ImageRelease]
AnyAudioRelease = Union[AudioReleaseCid, AudioRelease]
AnyVideoRelease = Union[VideoReleaseCid, VideoRelease]
AnyTextDocumentRelease = Union[TextDocumentReleaseCid, TextDocumentRelease]

AnyReleaseModel = Union[AudioRelease, ImageRelease, VideoRelease, TextDocumentRelease]
AnyReleaseCid = Union[AudioReleaseCid, ImageReleaseCid, VideoReleaseCid, TextDocumentReleaseCid]
AnyRelease = Union[AnyReleaseCid, AnyReleaseModel]


# still artwork #


StillArtworkId = Annotated[MongoId, id_schema('a string representing a still artwork id')]
StillArtworkCid = Annotated[ContentId, id_schema('a string representing a still artwork content id')]

class StillArtwork(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'still_artwork'

    id: StillArtworkId = Field(**db_id_kwargs)
    cid: StillArtworkCid = Field(**cid_kwargs)

    title: TitleData
    image: AnyImageRelease
    tags: conset(str, max_length=10)


StillArtworkAlbumId = Annotated[MongoId, id_schema('a string representing a still artwork album id')]
StillArtworkAlbumCid = Annotated[ContentId, id_schema('a string representing a still artwork album content id')]

class StillArtworkAlbum(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'still_artwork_album'

    id: StillArtworkAlbumId = Field(**db_id_kwargs)
    cid: StillArtworkAlbumCid = Field(**cid_kwargs)

    title: TitleData
    images: conlist(StillArtwork, min_length=1, max_length=1000)
    tags: conset(str, max_length=10)


# music #


SongId = Annotated[MongoId, id_schema('a string representing a song id')]
SongCid = Annotated[ContentId, id_schema('a string representing a song content id')]

class Song(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'songs'

    id: SongId = Field(**db_id_kwargs)
    cid: SongCid = Field(**cid_kwargs)

    title: TitleData
    audio: AnyAudioRelease
    tags: conset(str, max_length=10)
    music_video: Optional[AnyVideoRelease]
    cover_artwork: Optional[AnyImageRelease]
    other_artwork: Optional[conlist(AnyRelease, min_length=0, max_length=25)]
    lyrics: Optional[AnyTextDocumentRelease]

    
class AlbumType(StrEnum):
    album = 'album'
    ep = 'ep'


AlbumId = Annotated[MongoId, id_schema('a string representing an album id')]
AlbumCid = Annotated[ContentId, id_schema('a string representing an album content id')]

class Album(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'albums'

    id: AlbumId = Field(**db_id_kwargs)
    cid: AlbumCid = Field(**cid_kwargs)

    title: TitleData
    type: AlbumType
    tags: conset(str, max_length=10)
    songs: conlist(Song, min_length=2, max_length=50)
    cover_artwork: Optional[AnyImageRelease]
    other_artwork: Optional[conlist(AnyRelease, min_length=0, max_length=25)]


# video #

class VideoProgramType(StrEnum):
    feature = 'feature'
    episode = 'episode'
    short = 'short'


VideoProgramId = Annotated[MongoId, id_schema('a string representing a video program id')]
VideoProgramCid = Annotated[ContentId, id_schema('a string representing a video program content id')]

class VideoProgram(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'video_programs'

    id: VideoProgramId = Field(**db_id_kwargs)
    cid: VideoProgramCid = Field(**cid_kwargs)

    title: TitleData
    program: AnyVideoRelease
    type: VideoProgramType
    tags: conset(str, max_length=10)
    trailers: conlist(Union[AnyAudioRelease, AnyVideoRelease], min_length=0, max_length=10)
    cover_artwork: Optional[AnyImageRelease]
    other_artwork: Optional[conlist(AnyRelease, min_length=0, max_length=25)]


VideoMiniSeriesId = Annotated[MongoId, id_schema('a string representing a video mini series id')]
VideoMiniSeriesCid = Annotated[ContentId, id_schema('a string representing a video mini series content id')]

class VideoMiniSeries(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'video_mini_series'

    id: VideoMiniSeriesId = Field(**db_id_kwargs)
    cid: VideoMiniSeriesCid = Field(**cid_kwargs)

    title: TitleData
    episodes: conlist(VideoProgram, min_length=2, max_length=42)
    trailers: conlist(Union[AnyAudioRelease, AnyVideoRelease], min_length=0, max_length=10)
    tags: conset(str, max_length=10)
    cover_artwork: Optional[AnyImageRelease]
    other_artwork: Optional[conlist(AnyRelease, min_length=0, max_length=25)]


VideoSeasonId = Annotated[MongoId, id_schema('a string representing a video season id')]
VideoSeasonCid = Annotated[ContentId, id_schema('a string representing a video season content id')]

class VideoSeason(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'video_seasons'

    id: VideoSeasonId = Field(**db_id_kwargs)
    cid: VideoSeasonCid = Field(**cid_kwargs)

    title: TitleData
    episodes: conlist(VideoProgram, min_length=2, max_length=42)
    trailers: conlist(Union[AnyAudioRelease, AnyVideoRelease], min_length=0, max_length=10)
    tags: conset(str, max_length=10)
    cover_artwork: Optional[AnyImageRelease]
    other_artwork: Optional[conlist(AnyReleaseCid, min_length=0, max_length=25)]


VideoEpisodicSeriesId = Annotated[MongoId, id_schema('a string representing a video episodic series id')]
VideoEpisodicSeriesCid = Annotated[ContentId, id_schema('a string representing a video episodic series content id')]

class VideoEpisodicSeries(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'video_episodic_series'

    id: VideoEpisodicSeriesId = Field(**db_id_kwargs)
    cid: VideoEpisodicSeriesCid = Field(**cid_kwargs)

    title: TitleData
    seasons: conlist(VideoSeason, min_length=1, max_length=50)
    trailers: conlist(Union[AnyAudioRelease, AnyVideoRelease], min_length=0, max_length=10)
    tags: conset(str, max_length=10)
    cover_artwork: Optional[AnyImageRelease]
    other_artwork: Optional[conlist(AnyReleaseCid, min_length=0, max_length=25)]


# podcast #


PodcastProgramId = Annotated[MongoId, id_schema('a string representing a podcast program id')]
PodcastProgramCid = Annotated[ContentId, id_schema('a string representing a podcast program content id')]

class PodcastProgram(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'podcast_program'

    id: PodcastProgramId = Field(**db_id_kwargs)
    cid: PodcastProgramCid = Field(**cid_kwargs)

    title: TitleData
    program: AnyAudioRelease
    trailers: conlist(AnyAudioRelease, min_length=0, max_length=10)
    tags: conset(str, max_length=10)
    cover_artwork: Optional[AnyImageRelease]
    other_artwork: Optional[conlist(AnyReleaseCid, min_length=0, max_length=25)]


PodcastSeriesId = Annotated[MongoId, id_schema('a string representing a podcast series id')]
PodcastSeriesCid = Annotated[ContentId, id_schema('a string representing a podcast series content id')]

class PodcastSeries(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'podcast_series'

    id: PodcastSeriesId = Field(**db_id_kwargs)
    cid: PodcastSeriesCid = Field(**cid_kwargs)

    title: TitleData
    episodes: conlist(PodcastProgram, min_length=2, max_length=42)
    trailers: conlist(AnyAudioRelease, min_length=0, max_length=10)
    tags: conset(str, max_length=10)
    cover_artwork: Optional[AnyImageRelease]
    other_artwork: Optional[conlist(AnyReleaseCid, min_length=0, max_length=25)]


PodcastSeasonId = Annotated[MongoId, id_schema('a string representing a podcast season id')]
PodcastSeasonCid = Annotated[ContentId, id_schema('a string representing a podcast season content id')]

class PodcastSeason(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'podcast_season'

    id: PodcastSeasonId = Field(**db_id_kwargs)
    cid: PodcastSeasonCid = Field(**cid_kwargs)

    title: TitleData
    episodes: conlist(PodcastProgram, min_length=2, max_length=42)
    trailers: conlist(AnyAudioRelease, min_length=0, max_length=10)
    tags: conset(str, max_length=10)
    cover_artwork: Optional[AnyImageRelease]
    other_artwork: Optional[conlist(AnyReleaseCid, min_length=0, max_length=25)]


PodcastEpisodicSeriesId = Annotated[MongoId, id_schema('a string representing a podcast episodic series id')]
PodcastEpisodicSeriesCid = Annotated[ContentId, id_schema('a string representing a podcast episodic series content id')]

class PodcastEpisodicSeries(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'podcast_episodic_series'

    id: PodcastEpisodicSeriesId = Field(**db_id_kwargs)
    cid: PodcastEpisodicSeriesCid = Field(**cid_kwargs)

    title: TitleData
    seasons: conlist(PodcastProgram, min_length=1, max_length=50)
    trailers: conlist(AnyAudioRelease, min_length=0, max_length=10)
    tags: conset(str, max_length=10)
    cover_artwork: Optional[AnyImageRelease]
    other_artwork: Optional[conlist(AnyReleaseCid, min_length=0, max_length=25)]


# text publication #


class TextPublicationType(StrEnum):
    article = 'article'
    blog = 'blog'
    essay = 'essay'
    lyrics = 'lyrics'
    press_release = 'press_release'
    poetry = 'poetry'
    script = 'script'
    transcript = 'transcript'
    news = 'news'


TextEntryId = Annotated[MongoId, id_schema('a string representing a text entry id')]
TextEntryCid = Annotated[ContentId, id_schema('a string representing a text entry content id')]

class TextEntry(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'text_entries'

    id: TextEntryId = Field(**db_id_kwargs)
    cid: TextEntryCid = Field(**cid_kwargs)

    title: TitleData
    type: TextPublicationType
    document: AnyTextDocumentRelease
    tags: conset(str, max_length=10)


TextSeriesId = Annotated[MongoId, id_schema('a string representing a text series id')]
TextSeriesCid = Annotated[ContentId, id_schema('a string representing a text series content id')]

class TextSeries(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'text_series'

    id: TextSeriesId = Field(**db_id_kwargs)
    cid: TextSeriesCid = Field(**cid_kwargs)

    title: TitleData
    type: TextPublicationType
    documents: conlist(TextEntry, min_length=2, max_length=42)
    tags: conset(str, max_length=10)


TextPublicationId = Annotated[MongoId, id_schema('a string representing a text publication id')]
TextPublicationCid = Annotated[ContentId, id_schema('a string representing a text publication content id')]

class TextPublication(ContentModel):
    MONGO_COLLECTION_NAME: ClassVar[str] = 'blogs'

    id: TextPublicationId = Field(**db_id_kwargs)
    cid: TextPublicationCid = Field(**cid_kwargs)

    title: TitleData
    type: TextPublicationType
    series: conlist(TextSeries, min_length=1)
    tags: conset(str, max_length=10)


if __name__ == '__main__':
    import inspect

    for key, value in inspect.get_annotations(VideoRelease).items():
        try:
            if issubclass(value.__args__[0].__class__, BaseModel.__class__):
                if value.__args__[1].__args__[0] is ContentId:
                    print(key, value.__args__)
        except (AttributeError, IndexError):
            pass
