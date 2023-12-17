import os

from mcore.db import MongoDB
from mcore.auth import create_new_user, delete_user, delete_artist
from mcore.models import *
from mart.models import *

DEFAULT_OFFSET = os.environ.get('MSTACK_SDK_DEFAULT_LIST_OFFSET', 0)
DEFAULT_SIZE = os.environ.get('MSTACK_SDK_DEFAULT_LIST_SIZE', 50)

class MCore:

    def __init__(self) -> None:
        self.db = MongoDB.from_cache()

    # users

    def create_user(user_creator:UserCreator) -> User:
        return create_new_user(user_creator)
    
    def list_user(self, offset:int=DEFAULT_OFFSET, size:int=DEFAULT_SIZE) -> list[User]:
        return list(self.db.find(User, offset=offset, size=size))
    
    def read_user(self, cid: UserCid) -> User:
        return self.db.read(User, cid=cid)
    
    def delete_user(self, user: User | UserCid) -> None:
        try:
            user = self.user_read(user.cid)
        except AttributeError:
            pass
        delete_user(user)

    # file uploader

    def create_file_uploader(self, creator:FileUploaderCreator, user_cid:UserCid) -> FileUploader:
        uploader:FileUploader = creator.create_model(user_cid=user_cid)
        self.db.create(uploader)
        return uploader
    
    def list_file_uploader(self, offset:int=DEFAULT_OFFSET, size:int=DEFAULT_SIZE) -> list[FileUploader]:
        return list(self.db.find(FileUploader, offset=offset, size=size))
    
    def read_file_uploader(self, id:FileUploaderId) -> FileUploader:
        return self.db.read(FileUploader, id=id)
    
    def delete_file_uploader(self, file_uploader: FileUploader | FileUploaderId) -> None:
        try:
            id = file_uploader.id
        except AttributeError:
            id = file_uploader
        self.db.delete(FileUploader, id=id)

    # artists
        
    def create_artist(self, creator:ArtistCreator, user_cid:UserCid) -> Artist:
        artist:Artist = creator.create_model(user_cid=user_cid)
        self.db.create(artist)
        return artist
    
    def list_artist(self, offset:int=DEFAULT_OFFSET, size:int=DEFAULT_SIZE) -> list[Artist]:
        return list(self.db.find(Artist, offset=offset, size=size))
    
    def read_artist(self, cid:ArtistCid) -> Artist:
        return self.db.read(Artist, cid=cid)
    
    def delete_artist(self, artist: Artist | ArtistCid) -> None:
        try:
            cid = artist.cid
        except AttributeError:
            cid = artist
        
        return delete_artist(cid)
    # extract start
    # {"model_type": "StillImage", "creator_model_type": "StillImageCreator", "model_cid_type": "StillImageCid", "snake_case": "still_image", "lower_case": "still image"}

    # still image

    def create_still_image(self, creator:StillImageCreator, user_cid:UserCid) -> StillImage:
        still_image:StillImage = creator.create_model(user_cid=user_cid)
        self.db.create(still_image)
        return still_image
    
    def list_still_image(self, offset:int=DEFAULT_OFFSET, size:int=DEFAULT_SIZE) -> list[StillImage]:
        return list(self.db.find(StillImage, offset=offset, size=size))
    
    def read_still_image(self, still_image:StillImage | StillImageCid) -> StillImage:
        try:
            cid = still_image.cid
        except AttributeError:
            cid = still_image
        return self.db.read(StillImage, cid=cid)
    
    def delete_still_image(self, still_image: StillImage | StillImageCid) -> None:
        try:
            cid = still_image.cid
        except AttributeError:
            cid = still_image
        self.db.delete(StillImage, cid=cid)
