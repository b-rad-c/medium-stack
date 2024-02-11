import os

from mcore.db import MongoDB
from mcore.errors import MStackUserError
from mcore.auth import create_new_user, delete_user
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

    # users

    def create_user(user_creator:UserCreator) -> User:
        return create_new_user(user_creator)
    
    def list_user(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[User]:
        return list(self.db.find(User, offset=offset, size=size))
    
    def read_user(self, id:UserId=None, cid: UserCid=None) -> User:
        return self.db.read(User, id=id, cid=cid)
    
    def delete_user(self, user: User | UserCid) -> None:
        try:
            user = self.read_user(user.cid)
        except AttributeError:
            pass
        delete_user(user)

    # file uploader

    def create_file_uploader(self, creator:FileUploaderCreator, user_cid:UserCid) -> FileUploader:
        uploader:FileUploader = creator.create_model(user_cid=user_cid)
        self.db.create(uploader)
        return uploader
    
    def list_file_uploader(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[FileUploader]:
        return list(self.db.find(FileUploader, offset=offset, size=size))
    
    def read_file_uploader(self, id:FileUploaderId) -> FileUploader:
        return self.db.read(FileUploader, id=id)
    
    def delete_file_uploader(self, file_uploader: FileUploader | FileUploaderId) -> None:
        try:
            id = file_uploader.id
        except AttributeError:
            id = file_uploader
        self.db.delete(FileUploader, id=id)

    def upload_file(self, uploader: FileUploader, chunk: bytes) -> FileUploader:

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