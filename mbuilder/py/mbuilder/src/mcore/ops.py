import os
import logging

from typing import Callable, BinaryIO, List
from pathlib import Path

from mcore.db import MongoDB
from mcore.errors import MStackUserError, NotFoundError
from mcore.auth import create_new_user, delete_user, delete_profile
from mcore.models import *

"""
Note on file deletions:

Delete processes for files and releases delete the db entry first, then the file on disk.

If the db delete succeeds but the file delete fails, the errors will be logged as a warning but the method will still return success.
It will leave dangling file(s) which will be cleaned up by a background process. 

In the case of releases, if files are requested to be deleted, all of the db entries will be deleted in a transaction and then the 
files will be deleted.

Doing it this way allows us to maintain a consistent user experience while also ensuring that we don't have dangling files in the system
while keeping the code application logic simple.
"""


__all__ = [
    'SDK_DEFAULT_OFFSET',
    'SDK_DEFAULT_SIZE',
    'MCoreOps'
]

SDK_DEFAULT_OFFSET = int(os.environ.get('MSTACK_SDK_DEFAULT_LIST_OFFSET', 0))
SDK_DEFAULT_SIZE = int(os.environ.get('MSTACK_SDK_DEFAULT_LIST_SIZE', 50))

class MCoreOps:

    def __init__(self) -> None:
        self.db = MongoDB.from_cache()

    # users #

    def user_create(user_creator:UserCreator) -> User:
        return create_new_user(user_creator)
    
    def user_list(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[User]:
        return list(self.db.find(User, offset=offset, size=size))
    
    def user_read(self, id:UserId=None, cid: UserCid=None) -> User:
        return self.db.read(User, id=id, cid=cid)
    
    def user_delete(self, logged_in_user: User) -> None:
        delete_user(logged_in_user)

    # profiles #
        
    def profile_create(self, creator:ProfileCreator, logged_in_user:User) -> Profile:
        profile = creator.create_model(user_cid=logged_in_user.cid)
        self.db.create(profile)
        return profile
    
    def profile_list(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[Profile]:
        return list(self.db.find(Profile, offset=offset, size=size))
    
    def profile_read(self, id:ProfileId=None, cid:ProfileCid=None) -> Profile:
        return self.db.read(Profile, id=id, cid=cid)
    
    def profile_delete(self, logged_in_user:User, id:ProfileId=None, cid:ProfileCid=None) -> None:
        try:
            profile = self.profile_read(id, cid)
            delete_profile(profile, logged_in_user)
        except NotFoundError:
            return

    # file uploader #

    def file_uploader_create(self, creator:FileUploaderCreator, logged_in_user:User) -> FileUploader:
        uploader:FileUploader = creator.create_model(user_cid=logged_in_user.cid)
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
    
    def image_file_read(self, id:ImageFileId=None, cid:ImageFileCid=None) -> ImageFile:
        return self.db.read(ImageFile, id=id, cid=cid)
    
    def image_file_delete(self, logged_in_user:User, id:ImageFileId=None, cid:ImageFileCid=None) -> None:

        # see note on file deletions at the top of this file

        try:
            image_file = self.image_file_read(id, cid)
        except NotFoundError:
            return

        if image_file.user_cid != logged_in_user.cid:
            raise MStackUserError(f'User {logged_in_user.cid} does not have permission to delete image file {image_file.cid}')

        logging.info(f'deleting image file {image_file.cid}')

        self.db.delete(ImageFile, id=id, cid=cid)

        try:
            image_file.local_path.unlink()
        except FileNotFoundError:
            pass
        except Exception as e:
            logging.warning(f'error deleting image file cid={image_file.cid} path={image_file.local_path.as_posix()}: {e}', exc_info=True)

        logging.info(f'deleted image file {image_file.cid}')
    
    def image_release_create(self, creator:ImageReleaseCreator, logged_in_user:User) -> ImageRelease:
        
        try:
            master = self.image_file_read(cid=creator.master)
            alt_formats = [self.image_file_read(cid=cid) for cid in creator.alt_formats]
        except NotFoundError as e:
            raise MStackUserError(f'Error creating image release: {e}')

        for image_file in [master] + alt_formats:
            if image_file.user_cid != logged_in_user.cid:
                raise MStackUserError(f'User {logged_in_user.cid} does not have permission to create image release with file {image_file.cid}')

        image_release = creator.create_model(user_cid=logged_in_user.cid)
        self.db.create(image_release)
        return image_release
    
    def image_release_list(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[ImageRelease]:
        return list(self.db.find(ImageRelease, offset=offset, size=size))
    
    def image_release_read(self, id:ImageReleaseId=None, cid:ImageReleaseCid=None) -> ImageRelease:
        return self.db.read(ImageRelease, id=id, cid=cid)
    
    def image_release_delete(self, logged_in_user:User, id:ImageReleaseId=None, cid:ImageReleaseCid=None, delete_files:bool = False) -> None:

        # see note on file deletions at the top of this file

        try:
            image_release = self.image_release_read(id, cid)
        except NotFoundError:
            return

        if image_release.user_cid != logged_in_user.cid:
            raise MStackUserError(f'User {logged_in_user.cid} does not have permission to delete image release {image_release.cid}')

        logging.info(f'deleting image release {image_release.cid} delete_files={delete_files}')
        
        if delete_files:
            
            # get files from db - ignoring not found errors #

            image_files:List[ImageFile] = []
            
            for cid in image_release.alt_formats:
                try:
                    image_files.append(self.image_file_read(cid=cid))
                except NotFoundError:
                    pass

            try:
                image_files.append(self.image_file_read(cid=image_release.master))
            except NotFoundError:
                pass

            # delete files and release in transaction #

            img_file_collection = self.db.get_collection(ImageFile)
            img_release_collection = self.db.get_collection(ImageRelease)

            with self.db.start_session() as session:
                with session.start_transaction():
                    img_file_collection.delete_many({'cid': {'$in': [img.cid for img in image_files]}}, session=session)
                    img_release_collection.delete_one({'cid': image_release.cid}, session=session)

            # delete files from disk #
                    
            for img_file in image_files:
                try:
                    img_file.local_path.unlink()
                except FileNotFoundError:
                    pass
                except Exception as e:
                    logging.warning(f'error deleting image file cid={img_file.cid} path={img_file.local_path.as_posix()}: {e}', exc_info=True)

        else:
            self.db.delete(ImageRelease, cid=image_release.cid)

        logging.info(f'deleted image release {image_release.cid} delete_files={delete_files}')
    
    # audio #

    def audio_file_list(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[AudioFile]:
        return list(self.db.find(AudioFile, offset=offset, size=size))
    
    def audio_file_read(self, id:AudioFileId=None, cid:AudioFileCid=None) -> AudioFile:
        return self.db.read(AudioFile, id=id, cid=cid)
    
    def audio_file_delete(self, logged_in_user:User, id:AudioFileId=None, cid:AudioFileCid=None) -> None:

        # see note on file deletions at the top of this file

        try:
            audio_file = self.audio_file_read(id, cid)
        except NotFoundError:
            return

        if audio_file.user_cid != logged_in_user.cid:
            raise MStackUserError(f'User {logged_in_user.cid} does not have permission to delete audio file {audio_file.cid}')

        logging.info(f'deleting audio file {audio_file.cid}')

        self.db.delete(AudioFile, id=id, cid=cid)

        try:
            audio_file.local_path.unlink()
        except FileNotFoundError:
            pass
        except Exception as e:
            logging.warning(f'error deleting audio file cid={audio_file.cid} path={audio_file.local_path.as_posix()}: {e}', exc_info=True)

        logging.info(f'deleted audio file {audio_file.cid}')
    
    def audio_release_create(self, creator:AudioReleaseCreator, logged_in_user:User) -> AudioRelease:
        
        try:
            master = self.audio_file_read(cid=creator.master)
            alt_formats = [self.audio_file_read(cid=cid) for cid in creator.alt_formats]
        except NotFoundError as e:
            raise MStackUserError(f'Error creating audio release: {e}')

        for audio_file in [master] + alt_formats:
            if audio_file.user_cid != logged_in_user.cid:
                raise MStackUserError(f'User {logged_in_user.cid} does not have permission to create audio release with file {audio_file.cid}')

        audio_release = creator.create_model(user_cid=logged_in_user.cid)
        self.db.create(audio_release)
        return audio_release
    
    def audio_release_list(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[AudioRelease]:
        return list(self.db.find(AudioRelease, offset=offset, size=size))
    
    def audio_release_read(self, id:AudioReleaseId=None, cid:AudioReleaseCid=None) -> AudioRelease:
        return self.db.read(AudioRelease, id=id, cid=cid)
    
    def audio_release_delete(self, logged_in_user:User, id:AudioReleaseId=None, cid:AudioReleaseCid=None, delete_files:bool = False) -> None:
            
        # see note on file deletions at the top of this file

        try:
            audio_release = self.audio_release_read(id, cid)
        except NotFoundError:
            return
        
        if audio_release.user_cid != logged_in_user.cid:
            raise MStackUserError(f'User {logged_in_user.cid} does not have permission to delete audio release {audio_release.cid}')

        logging.info(f'deleting audio release {audio_release.cid} delete_files={delete_files}')
        
        if delete_files:
            
            # get files from db - ignoring not found errors #

            audio_files:List[AudioFile] = []

            for cid in audio_release.alt_formats:
                try:
                    audio_files.append(self.audio_file_read(cid=cid))
                except NotFoundError:
                    pass

            try:
                audio_files.append(self.audio_file_read(cid=audio_release.master))
            except NotFoundError:
                pass

            # delete files and release in transaction #

            audio_file_collection = self.db.get_collection(AudioFile)
            audio_release_collection = self.db.get_collection(AudioRelease)

            with self.db.start_session() as session:
                with session.start_transaction():
                    audio_file_collection.delete_many({'cid': {'$in': [audio.cid for audio in audio_files]}}, session=session)
                    audio_release_collection.delete_one({'cid': audio_release.cid}, session=session)

            # delete files from disk #
                    
            for audio_file in audio_files:
                try:
                    audio_file.local_path.unlink()
                except FileNotFoundError:
                    pass
                except Exception as e:
                    logging.warning(f'error deleting audio file cid={audio_file.cid} path={audio_file.local_path.as_posix()}: {e}', exc_info=True)

        else:
            self.db.delete(AudioRelease, cid=audio_release.cid)

        logging.info(f'deleted audio release {audio_release.cid} delete_files={delete_files}')

    # video #

    def video_file_list(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[VideoFile]:
        return list(self.db.find(VideoFile, offset=offset, size=size))
    
    def video_file_read(self, id:VideoFileId=None, cid:VideoFileCid=None) -> VideoFile:
        return self.db.read(VideoFile, id=id, cid=cid)
    
    def video_file_delete(self, logged_in_user:User, id:VideoFileId=None, cid:VideoFileCid=None) -> None:
            
        # see note on file deletions at the top of this file

        try:
            video_file = self.video_file_read(id, cid)
        except NotFoundError:
            return
        
        if video_file.user_cid != logged_in_user.cid:
            raise MStackUserError(f'User {logged_in_user.cid} does not have permission to delete video file {video_file.cid}')
        
        logging.info(f'deleting video file {video_file.cid}')

        self.db.delete(VideoFile, id=id, cid=cid)

        try:
            video_file.local_path.unlink()
        except FileNotFoundError:
            pass
        except Exception as e:
            logging.warning(f'error deleting video file cid={video_file.cid} path={video_file.local_path.as_posix()}: {e}', exc_info=True)

        logging.info(f'deleted video file {video_file.cid}')

    def video_release_create(self, creator:VideoReleaseCreator, logged_in_user:User) -> VideoRelease:

        try:
            master = self.video_file_read(cid=creator.master)
            alt_formats = [self.video_file_read(cid=cid) for cid in creator.alt_formats]
        except NotFoundError as e:
            raise MStackUserError(f'Error creating video release: {e}')
        
        for video_file in [master] + alt_formats:
            if video_file.user_cid != logged_in_user.cid:
                raise MStackUserError(f'User {logged_in_user.cid} does not have permission to create video release with file {video_file.cid}')

        video_release = creator.create_model(user_cid=logged_in_user.cid)
        self.db.create(video_release)
        return video_release
    
    def video_release_list(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[VideoRelease]:
        return list(self.db.find(VideoRelease, offset=offset, size=size))
    
    def video_release_read(self, id:VideoReleaseId=None, cid:VideoReleaseCid=None) -> VideoRelease:
        return self.db.read(VideoRelease, id=id, cid=cid)

    def video_release_delete(self, logged_in_user:User, id:VideoReleaseId=None, cid:VideoReleaseCid=None, delete_files:bool = False) -> None:
            
        # see note on file deletions at the top of this file

        try:
            video_release = self.video_release_read(id, cid)
        except NotFoundError:
            return
        
        if video_release.user_cid != logged_in_user.cid:
            raise MStackUserError(f'User {logged_in_user.cid} does not have permission to delete video release {video_release.cid}')

        logging.info(f'deleting video release {video_release.cid} delete_files={delete_files}')
        
        if delete_files:
            
            # get files from db #

            video_files:List[VideoFile] = []
            for cid in video_release.alt_formats:
                try:
                    video_files.append(self.video_file_read(cid=cid))
                except NotFoundError:
                    pass
            
            try:
                video_files.append(self.video_file_read(cid=video_release.master))
            except NotFoundError:
                pass

            # delete files and release in transaction #

            video_file_collection = self.db.get_collection(VideoFile)
            video_release_collection = self.db.get_collection(VideoRelease)

            with self.db.start_session() as session:
                with session.start_transaction():
                    video_file_collection.delete_many({'cid': {'$in': [video.cid for video in video_files]}}, session=session)
                    video_release_collection.delete_one({'cid': video_release.cid}, session=session)

            # delete files from disk #
                    
            for video_file in video_files:
                try:
                    video_file.local_path.unlink()
                except FileNotFoundError:
                    pass
                except Exception as e:
                    logging.warning(f'error deleting video file cid={video_file.cid} path={video_file.local_path.as_posix()}: {e}', exc_info=True)

        else:
            self.db.delete(VideoRelease, cid=video_release.cid)

        logging.info(f'deleted video release {video_release.cid} delete_files={delete_files}')