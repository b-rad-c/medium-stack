import os 

from io import BytesIO
from typing import List, Callable, Tuple
from os.path import join

from mcore.errors import MStackClientError, NotFoundError
from mserve import IndexResponse
from mcore.types import ModelIdType
from mcore.models import (
    User,
    UserCreator,
    FileUploader,
    FileUploaderCreator,
    FileUploadTypes
)

from mart.models import *

import requests
from requests.exceptions import RequestException



__all__ = [
    'MStackClient',
    'MStackClientError'
]


MSTACK_API_HOST = os.environ.get('MSTACK_API_HOST', 'http://localhost:8000')
MSTACK_API_PREFIX = 'api/v0'


class MStackClient:

    #
    # internal
    #

    def __init__(self):
        self.session = requests.Session()
        self.url_base = join(MSTACK_API_HOST, MSTACK_API_PREFIX)
        self.response = None

    def _call(self, method:str, endpoint:str, *args, **kwargs) -> dict:
        url = join(self.url_base, endpoint)
        try:
            self.response = self.session.request(method, url, *args, **kwargs)
        except RequestException as e:
            raise MStackClientError(str(e), url, e)
        
        if self.response.status_code == 404:
            raise NotFoundError(f'Not Found: {url}')
        
        try:
            self.response.raise_for_status()
            return self.response.json()
        except RequestException as e:
            raise MStackClientError(str(e), url, e, self.response)
        
    def _get(self, endpoint: str, *args, **kwargs) -> dict:
        return self._call('GET', endpoint, *args, **kwargs)

    def _post(self, endpoint: str, *args, **kwargs) -> dict:
        return self._call('POST', endpoint, *args, **kwargs)

    def _put(self, endpoint: str, *args, **kwargs) -> dict:
        return self._call('PUT', endpoint, *args, **kwargs)

    def _patch(self, endpoint: str, *args, **kwargs) -> dict:
        return self._call('PATCH', endpoint, *args, **kwargs)

    def _delete(self, endpoint: str, *args, **kwargs) -> dict:
        return self._call('DELETE', endpoint, *args, **kwargs)
    
    @staticmethod
    def _model_id_type_url(endpoint, id:str = None, cid:str = None) -> str:
        if id is not None:
            return join(endpoint, f'{ModelIdType.id.value}/{id}')
        
        elif cid is not None:
            return join(endpoint, f'{ModelIdType.cid.value}/{cid}')
        
        else:
            raise MStackClientError(f'must provide cid or id')

    #
    # main
    #

    def index(self) -> IndexResponse:
        return IndexResponse(**self._get(''))

    #
    # core
    #

    # users #

    def create_user(self, user_creator: UserCreator) -> User:
        data = self._post('core/users', json=user_creator.model_dump())
        return User(**data)

    def read_user(self, id:str = None, cid:str = None) -> User:
        url = self._model_id_type_url('core/users', id, cid)
        data = self._get(url)
        return User(**data)

    def delete_user(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url('core/users', id, cid))

    def list_users(self, offset:int=0, size:int=50) -> List[User]:
        data = self._get('core/users', params={'offset': offset, 'size': size})
        return [User(**user) for user in data]

    # file upload #

    def create_file_uploader(self, file_upload_creator: FileUploaderCreator) -> FileUploader:
        data = self._post('core/file-uploader', json=file_upload_creator.model_dump())
        return FileUploader(**data)

    def read_file_uploader(self, id: str) -> FileUploader:
        data = self._get(f'core/file-uploader/{id}')
        return FileUploader(**data)

    def delete_file_uploader(self, id:str = None) -> None:
        self._delete(f'core/file-uploader/{id}')

    def list_file_uploaders(self, offset:int=0, size:int=50) -> List[FileUploader]:
        data = self._get('core/file-uploader', params={'offset': offset, 'size': size})
        return [FileUploader(**uploader) for uploader in data]
    
    def upload_chunk(self, id:str, chunk:bytes) -> FileUploader:
        data = self._post(f'core/file-uploader/{id}', files={'chunk': BytesIO(chunk)})
        return FileUploader(**data)

    def upload_file(self, file_path:str, type:FileUploadTypes, chunk_size=250_000, on_update=Callable[[], FileUploader]) -> FileUploader:
        size = os.path.getsize(file_path)
        uploader = self.create_file_uploader(FileUploaderCreator(total_size=size, type=type))

        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break

                uploader = self.upload_chunk(uploader.id, chunk)
                if on_update is not None:
                    on_update(uploader)

        return uploader

    #
    # mart
    #

    # mart - artists #

    def create_artist(self, artist_creator: ArtistCreator) -> Artist:
        data = self._post(f'mart{Artist.API_PREFIX}', json=artist_creator.model_dump())
        return Artist(**data)
    
    def read_artist(self, id:str = None, cid:str = None) -> Artist:
        url = self._model_id_type_url(f'mart{Artist.API_PREFIX}', id, cid)
        data = self._get(url)
        return Artist(**data)

    def delete_artist(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url(f'mart{Artist.API_PREFIX}', id, cid))
    
    def list_artists(self, offset:int=0, size:int=50) -> List[Artist]:
        data = self._get(f'mart{Artist.API_PREFIX}', params={'offset': offset, 'size': size})
        return [Artist(**artist) for artist in data]

    def create_artist_group(self, artist_group_creator: ArtistGroupCreator) -> ArtistGroup:
        data = self._post(f'mart{ArtistGroup.API_PREFIX}', json=artist_group_creator.model_dump())
        return ArtistGroup(**data)
    
    def read_artist_group(self, id:str = None, cid:str = None) -> ArtistGroup:
        url = self._model_id_type_url(f'mart{ArtistGroup.API_PREFIX}', id, cid)
        data = self._get(url)
        return ArtistGroup(**data)
    
    def delete_artist_group(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url(f'mart{ArtistGroup.API_PREFIX}', id, cid))
    
    def list_artist_groups(self, offset:int=0, size:int=50) -> List[ArtistGroup]:
        data = self._get(f'mart{ArtistGroup.API_PREFIX}', params={'offset': offset, 'size': size})
        return [ArtistGroup(**artist_group) for artist_group in data]

    # mart - still images #

    def create_still_image(self, still_image_creator: StillImageCreator) -> StillImage:
        data = self._post(f'mart{StillImage.API_PREFIX}', json=still_image_creator.model_dump())
        return StillImage(**data)
    
    def read_still_image(self, id:str = None, cid:str = None) -> StillImage:
        url = self._model_id_type_url(f'mart{StillImage.API_PREFIX}', id, cid)
        data = self._get(url)
        return StillImage(**data)
    
    def delete_still_image(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url(f'mart{StillImage.API_PREFIX}', id, cid))
    
    def list_still_images(self, offset:int=0, size:int=50) -> List[StillImage]:
        data = self._get(f'mart{StillImage.API_PREFIX}', params={'offset': offset, 'size': size})
        return [StillImage(**still_image) for still_image in data]
    
    def create_still_image_album(self, still_image_album_creator: StillImageAlbumCreator) -> StillImageAlbum:
        data = self._post(f'mart{StillImageAlbum.API_PREFIX}', json=still_image_album_creator.model_dump())
        return StillImageAlbum(**data)
    
    def read_still_image_album(self, id:str = None, cid:str = None) -> StillImageAlbum:
        url = self._model_id_type_url(f'mart{StillImageAlbum.API_PREFIX}', id, cid)
        data = self._get(url)
        return StillImageAlbum(**data)
    
    def delete_still_image_album(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url(f'mart{StillImageAlbum.API_PREFIX}', id, cid))
    
    def list_still_image_albums(self, offset:int=0, size:int=50) -> List[StillImageAlbum]:
        data = self._get(f'mart{StillImageAlbum.API_PREFIX}', params={'offset': offset, 'size': size})
        return [StillImageAlbum(**still_image_album) for still_image_album in data]

    # mart - videos #

    def create_video_program(self, video_program_creator: VideoProgramCreator) -> VideoProgram:
        data = self._post(f'mart{VideoProgram.API_PREFIX}', json=video_program_creator.model_dump())
        return VideoProgram(**data)
    
    def read_video_program(self, id:str = None, cid:str = None) -> VideoProgram:
        url = self._model_id_type_url(f'mart{VideoProgram.API_PREFIX}', id, cid)
        data = self._get(url)
        return VideoProgram(**data)

    def delete_video_program(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url(f'mart{VideoProgram.API_PREFIX}', id, cid))

    def list_video_programs(self, offset:int=0, size:int=50) -> List[VideoProgram]:
        data = self._get(f'mart{VideoProgram.API_PREFIX}', params={'offset': offset, 'size': size})
        return [VideoProgram(**video_program) for video_program in data]

    def create_video_season(self, video_season_creator: VideoSeasonCreator) -> VideoSeason:
        data = self._post(f'mart{VideoSeason.API_PREFIX}', json=video_season_creator.model_dump())
        return VideoSeason(**data)
    
    def read_video_season(self, id:str = None, cid:str = None) -> VideoSeason:
        url = self._model_id_type_url(f'mart{VideoSeason.API_PREFIX}', id, cid)
        data = self._get(url)
        return VideoSeason(**data)
    
    def delete_video_season(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url(f'mart{VideoSeason.API_PREFIX}', id, cid))
    
    def list_video_seasons(self, offset:int=0, size:int=50) -> List[VideoSeason]:
        data = self._get(f'mart{VideoSeason.API_PREFIX}', params={'offset': offset, 'size': size})
        return [VideoSeason(**video_season) for video_season in data]
    
    def create_video_mini_series(self, video_mini_series_creator: VideoMiniSeriesCreator) -> VideoMiniSeries:
        data = self._post(f'mart{VideoMiniSeries.API_PREFIX}', json=video_mini_series_creator.model_dump())
        return VideoMiniSeries(**data)
    
    def read_video_mini_series(self, id:str = None, cid:str = None) -> VideoMiniSeries:
        url = self._model_id_type_url(f'mart{VideoMiniSeries.API_PREFIX}', id, cid)
        data = self._get(url)
        return VideoMiniSeries(**data)
    
    def delete_video_mini_series(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url(f'mart{VideoMiniSeries.API_PREFIX}', id, cid))
    
    def list_video_mini_series(self, offset:int=0, size:int=50) -> List[VideoMiniSeries]:
        data = self._get(f'mart{VideoMiniSeries.API_PREFIX}', params={'offset': offset, 'size': size})
        return [VideoMiniSeries(**video_mini_series) for video_mini_series in data]
    
    def create_video_series(self, video_series_creator: VideoSeriesCreator) -> VideoSeries:
        data = self._post(f'mart{VideoSeries.API_PREFIX}', json=video_series_creator.model_dump())
        return VideoSeries(**data)
    
    def read_video_series(self, id:str = None, cid:str = None) -> VideoSeries:
        url = self._model_id_type_url(f'mart{VideoSeries.API_PREFIX}', id, cid)
        data = self._get(url)
        return VideoSeries(**data)
    
    def delete_video_series(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url(f'mart{VideoSeries.API_PREFIX}', id, cid))

    def list_video_series(self, offset:int=0, size:int=50) -> List[VideoSeries]:
        data = self._get(f'mart{VideoSeries.API_PREFIX}', params={'offset': offset, 'size': size})
        return [VideoSeries(**video_series) for video_series in data]
    
    # mart - music #

    def create_song(self, song_creator: SongCreator) -> Song:
        data = self._post(f'mart{Song.API_PREFIX}', json=song_creator.model_dump())
        return Song(**data)
    
    def read_song(self, id:str = None, cid:str = None) -> Song:
        url = self._model_id_type_url(f'mart{Song.API_PREFIX}', id, cid)
        data = self._get(url)
        return Song(**data)
    
    def delete_song(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url(f'mart{Song.API_PREFIX}', id, cid))
    
    def list_songs(self, offset:int=0, size:int=50) -> List[Song]:
        data = self._get(f'mart{Song.API_PREFIX}', params={'offset': offset, 'size': size})
        return [Song(**song) for song in data]
    
    def create_music_album(self, music_album_creator: MusicAlbumCreator) -> MusicAlbum:
        data = self._post(f'mart{MusicAlbum.API_PREFIX}', json=music_album_creator.model_dump())
        return MusicAlbum(**data)
    
    def read_music_album(self, id:str = None, cid:str = None) -> MusicAlbum:
        url = self._model_id_type_url(f'mart{MusicAlbum.API_PREFIX}', id, cid)
        data = self._get(url)
        return MusicAlbum(**data)
    
    def delete_music_album(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url(f'mart{MusicAlbum.API_PREFIX}', id, cid))

    def list_music_albums(self, offset:int=0, size:int=50) -> List[MusicAlbum]:
        data = self._get(f'mart{MusicAlbum.API_PREFIX}', params={'offset': offset, 'size': size})
        return [MusicAlbum(**music_album) for music_album in data]

    # mart - podcasts #

    def create_podcast_episode(self, podcast_episode_creator: PodcastEpisodeCreator) -> PodcastEpisode:
        data = self._post(f'mart{PodcastEpisode.API_PREFIX}', json=podcast_episode_creator.model_dump())
        return PodcastEpisode(**data)
    
    def read_podcast_episode(self, id:str = None, cid:str = None) -> PodcastEpisode:
        url = self._model_id_type_url(f'mart{PodcastEpisode.API_PREFIX}', id, cid)
        data = self._get(url)
        return PodcastEpisode(**data)
    
    def delete_podcast_episode(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url(f'mart{PodcastEpisode.API_PREFIX}', id, cid))

    def list_podcast_episodes(self, offset:int=0, size:int=50) -> List[PodcastEpisode]:
        data = self._get(f'mart{PodcastEpisode.API_PREFIX}', params={'offset': offset, 'size': size})
        return [PodcastEpisode(**podcast_episode) for podcast_episode in data]
    
    def create_podcast_season(self, podcast_season_creator: PodcastSeasonCreator) -> PodcastSeason:
        data = self._post(f'mart{PodcastSeason.API_PREFIX}', json=podcast_season_creator.model_dump())
        return PodcastSeason(**data)
    
    def read_podcast_season(self, id:str = None, cid:str = None) -> PodcastSeason:
        url = self._model_id_type_url(f'mart{PodcastSeason.API_PREFIX}', id, cid)
        data = self._get(url)
        return PodcastSeason(**data)
    
    def delete_podcast_season(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url(f'mart{PodcastSeason.API_PREFIX}', id, cid))
    
    def list_podcast_seasons(self, offset:int=0, size:int=50) -> List[PodcastSeason]:
        data = self._get(f'mart{PodcastSeason.API_PREFIX}', params={'offset': offset, 'size': size})
        return [PodcastSeason(**podcast_season) for podcast_season in data]
    
    def create_podcast(self, podcast_creator: PodcastCreator) -> Podcast:
        data = self._post(f'mart{Podcast.API_PREFIX}', json=podcast_creator.model_dump())
        return Podcast(**data)
    
    def read_podcast(self, id:str = None, cid:str = None) -> Podcast:
        url = self._model_id_type_url(f'mart{Podcast.API_PREFIX}', id, cid)
        data = self._get(url)
        return Podcast(**data)
    
    def delete_podcast(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url(f'mart{Podcast.API_PREFIX}', id, cid))

    def list_podcasts(self, offset:int=0, size:int=50) -> List[Podcast]:
        data = self._get(f'mart{Podcast.API_PREFIX}', params={'offset': offset, 'size': size})
        return [Podcast(**podcast) for podcast in data]
