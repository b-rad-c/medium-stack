import os

from mcore.db import MongoDB
from mcore.auth import create_new_user, delete_user, delete_artist
from mcore.models import *


__all__ = [
    'SDK_DEFAULT_OFFSET',
    'SDK_DEFAULT_SIZE',
    'MCore'
]

SDK_DEFAULT_OFFSET = os.environ.get('MSTACK_SDK_DEFAULT_LIST_OFFSET', 0)
SDK_DEFAULT_SIZE = os.environ.get('MSTACK_SDK_DEFAULT_LIST_SIZE', 50)

class MCore:

    def __init__(self) -> None:
        self.db = MongoDB.from_cache()

    # users

    def create_user(user_creator:UserCreator) -> User:
        return create_new_user(user_creator)
    
    def list_user(self, offset:int=SDK_DEFAULT_OFFSET, size:int=SDK_DEFAULT_SIZE) -> list[User]:
        return list(self.db.find(User, offset=offset, size=size))
    
    def read_user(self, cid: UserCid) -> User:
        return self.db.read(User, cid=cid)
    
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

