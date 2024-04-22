from ..conftest import example_model, example_cid, _test_db_crud, _test_db_pagination

from mcore.models import *


def test_user():
    user_creator:UserCreator = example_model(UserCreator)
    user = user_creator.create_model()
    _test_db_crud(user, example_cid(User), User)
    _test_db_pagination(user, User)

def test_profile():
    profile_creator:ProfileCreator = example_model(ProfileCreator)
    profile_cid = example_cid(Profile)
    profile = profile_creator.create_model(user_cid=example_cid(User))
    _test_db_crud(profile, profile_cid, Profile)
    _test_db_pagination(profile, Profile)


def test_file_uploader():
    creator:FileUploaderCreator = example_model(FileUploaderCreator)
    file_uploader = creator.create_model(user_cid=example_cid(User))
    _test_db_crud(file_uploader, None, FileUploader)
    _test_db_pagination(file_uploader, FileUploader)


def test_image_file(image_file, image_file_cid):
    _test_db_crud(image_file, image_file_cid, ImageFile)
    _test_db_pagination(image_file, ImageFile)


def test_image_release():
    creator:ImageReleaseCreator = example_model(ImageReleaseCreator)
    image_release = creator.create_model(user_cid=example_cid(User))
    _test_db_crud(image_release, example_cid(ImageRelease), ImageRelease)
    _test_db_pagination(image_release, ImageRelease)


def test_audio_file(audio_file, audio_file_cid):
    _test_db_crud(audio_file, audio_file_cid, AudioFile)
    _test_db_pagination(audio_file, AudioFile)

def test_audio_release():
    creator:AudioReleaseCreator = example_model(AudioReleaseCreator)
    audio_release = creator.create_model(user_cid=example_cid(User))
    _test_db_crud(audio_release, example_cid(AudioRelease), AudioRelease)
    _test_db_pagination(audio_release, AudioRelease)


def test_video_file(video_file, video_file_cid):
    _test_db_crud(video_file, video_file_cid, VideoFile)
    _test_db_pagination(video_file, VideoFile)

def test_video_release():
    creator:VideoReleaseCreator = example_model(VideoReleaseCreator)
    video_release = creator.create_model(user_cid=example_cid(User))
    _test_db_crud(video_release, example_cid(VideoRelease), VideoRelease)
    _test_db_pagination(video_release, VideoRelease)


def test_text_file():
    pass
