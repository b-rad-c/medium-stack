import os

from typing import Callable, BinaryIO
from pathlib import Path

from mcore.db import MongoDB
from mcore.errors import MStackUserError
from mcore.auth import create_new_user, delete_user, delete_profile
from mcore.models import *


__all__ = [
    'SDK_DEFAULT_OFFSET',
    'SDK_DEFAULT_SIZE',
    'MCore'
]

SDK_DEFAULT_OFFSET = int(os.environ.get('MSTACK_SDK_DEFAULT_LIST_OFFSET', 0))
SDK_DEFAULT_SIZE = int(os.environ.get('MSTACK_SDK_DEFAULT_LIST_SIZE', 50))

class MCore:

    def __init__(self) -> None:
        self.db = MongoDB.from_cache()

    # users #

    def user_create(user_creator:UserCreator) -> User:
        return create_new_user(user_creator)
    
    def user_list(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[User]:
        return list(self.db.find(User, offset=offset, size=size))
    
    def user_read(self, id:UserId=None, cid: UserCid=None) -> User:
        return self.db.read(User, id=id, cid=cid)
    
    def user_delete(self, user: User) -> None:
        delete_user(user)

    # profiles #
        
    def profile_create(self, creator:ProfileCreator, user_cid:UserCid) -> Profile:
        profile = creator.create_model(user_cid=user_cid)
        self.db.create(profile)
        return profile
    
    def profile_list(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[Profile]:
        return list(self.db.find(Profile, offset=offset, size=size))
    
    def profile_read(self, id:ProfileId=None, cid:ProfileCid=None) -> Profile:
        return self.db.read(Profile, id=id, cid=cid)
    
    def profile_delete(self, profile: Profile, logged_in_user:User) -> None:
        delete_profile(profile, logged_in_user)

    # file uploader #

    def file_uploader_create(self, creator:FileUploaderCreator, user_cid:UserCid) -> FileUploader:
        uploader:FileUploader = creator.create_model(user_cid=user_cid)
        self.db.create(uploader)
        return uploader
    
    def file_uploader_list(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[FileUploader]:
        return list(self.db.find(FileUploader, offset=offset, size=size))
    
    def file_uploader_read(self, id:FileUploaderId) -> FileUploader:
        return self.db.read(FileUploader, id=id)
    
    def file_uploader_delete(self, file_uploader: FileUploader | FileUploaderId) -> None:
        try:
            id = file_uploader.id
        except AttributeError:
            id = file_uploader
        self.db.delete(FileUploader, id=id)

    def upload_chunk(self, uploader: FileUploader, chunk: bytes) -> FileUploader:

        # init upload #
        
        if uploader.status != FileUploadStatus.uploading:
            raise MStackUserError(f'FileUploader {uploader.id} status is not {FileUploadStatus.uploading.value}')
        
        if uploader.total_uploaded >= uploader.total_size:
            raise MStackUserError(f'FileUploader {uploader.id} is already at or over upload size')
        
        # touch / create path if doesn't exist #

        path = uploader.local_path()

        try:
            path.touch()
        except FileNotFoundError:
            os.makedirs(path.parent, exist_ok=True)
            path.touch()
        
        # write chunk to disk #
        
        with path.open('ab') as f:
            written = f.write(chunk)
        
        uploader.total_uploaded += written
        uploader.update_timestamp()
        
        # file upload error #

        if uploader.total_uploaded > uploader.total_size:
            uploader.status = FileUploadStatus.error
            uploader.error = 'file upload is over upload size'
            self.db.update(uploader)
            raise MStackUserError(f'FileUploader {uploader.id} is over upload size')
        
        # file upload finished, update status #

        if uploader.total_uploaded == uploader.total_size:
            uploader.status = FileUploadStatus.process_queue

        self.db.update(uploader)

        return uploader
    
    def upload_file(
            self, 
            file_path:str | Path, 
            type:FileUploadTypes, 
            extension:str=None,
            chunk_size=250_000, 
            on_update:Callable[[], FileUploader]=None
        ) -> FileUploader:
        """if extension is not provided, it will be inferred from the file_path"""
        
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        size = file_path.stat().st_size
        ext = file_path.suffix[1:] if extension is None else extension

        with open(file_path, 'rb') as file:
            return self.upload_file_obj(file, type, size, ext, chunk_size, on_update)
    
    def upload_file_obj(
            self, 
            file_obj:BinaryIO, 
            type:FileUploadTypes, 
            size: int,
            extension:str,
            chunk_size=250_000, 
            on_update:Callable[[], FileUploader]=None, 
        ) -> FileUploader:
        
        uploader = self.file_uploader_create(FileUploaderCreator(total_size=size, type=type, ext=extension))

        while True:
            chunk = file_obj.read(chunk_size)
            if not chunk:
                break

            uploader = self.upload_chunk(uploader, chunk)
            if on_update is not None:
                on_update(uploader)

        return uploader

    # images #

    def image_file_list(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[ImageFile]:
        return list(self.db.find(ImageFile, offset=offset, size=size))
    
    def image_file_read(self, id:ImageFileId, cid:ImageFileCid) -> ImageFile:
        return self.db.read(ImageFile, id=id, cid=cid)
    
    def image_release_create(self, creator:ImageReleaseCreator, user_cid:UserCid) -> ImageRelease:
        image_release = creator.create_model(user_cid=user_cid)
        self.db.create(image_release)
        return image_release
    
    def image_release_list(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[ImageRelease]:
        return list(self.db.find(ImageRelease, offset=offset, size=size))
    
    def image_release_read(self, id:ImageReleaseId, cid:ImageReleaseCid) -> ImageRelease:
        return self.db.read(ImageRelease, id=id, cid=cid)
    
    # audio #

    def audio_file_list(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[AudioFile]:
        return list(self.db.find(AudioFile, offset=offset, size=size))
    
    def audio_file_read(self, id:AudioFileId, cid:AudioFileCid) -> AudioFile:
        return self.db.read(AudioFile, id=id, cid=cid)
    
    def audio_release_create(self, creator:AudioReleaseCreator, user_cid:UserCid) -> AudioRelease:
        audio_release = creator.create_model(user_cid=user_cid)
        self.db.create(audio_release)
        return audio_release
    
    def audio_release_list(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[AudioRelease]:
        return list(self.db.find(AudioRelease, offset=offset, size=size))
    
    def audio_release_read(self, id:AudioReleaseId, cid:AudioReleaseCid) -> AudioRelease:
        return self.db.read(AudioRelease, id=id, cid=cid)
    
    # video #

    def video_file_list(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[VideoFile]:
        return list(self.db.find(VideoFile, offset=offset, size=size))
    
    def video_file_read(self, id:VideoFileId, cid:VideoFileCid) -> VideoFile:
        return self.db.read(VideoFile, id=id, cid=cid)
    
    def video_release_create(self, creator:VideoReleaseCreator, user_cid:UserCid) -> VideoRelease:
        video_release = creator.create_model(user_cid=user_cid)
        self.db.create(video_release)
        return video_release
    
    def video_release_list(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[VideoRelease]:
        return list(self.db.find(VideoRelease, offset=offset, size=size))
    
    def video_release_read(self, id:VideoReleaseId, cid:VideoReleaseCid) -> VideoRelease:
        return self.db.read(VideoRelease, id=id, cid=cid)
