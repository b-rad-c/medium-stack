from ..conftest import example_model, example_cid, _test_db_crud, _test_db_pagination

from mcore.models import *


def test_user():
    user_creator:UserCreator = example_model(UserCreator)
    user = user_creator.create_model()
    user_cid = example_cid(User)
    _test_db_crud(user, user_cid, User)
    _test_db_pagination(user, User)


def test_file_uploader():
    creator:FileUploaderCreator = example_model(FileUploaderCreator)
    user_cid = example_cid(User)
    file_uploader = creator.create_model(user_cid=user_cid)
    _test_db_crud(file_uploader, None, FileUploader)
    _test_db_pagination(file_uploader, FileUploader)


def test_image_file(image_file, image_file_cid):
    _test_db_crud(image_file, image_file_cid, ImageFile)
    _test_db_pagination(image_file, ImageFile)


def test_audio_file(audio_file, audio_file_cid):
    _test_db_crud(audio_file, audio_file_cid, AudioFile)
    _test_db_pagination(audio_file, AudioFile)


def test_video_file(video_file, video_file_cid):
    _test_db_crud(video_file, video_file_cid, VideoFile)
    _test_db_pagination(video_file, VideoFile)


def test_text_file():
    pass
