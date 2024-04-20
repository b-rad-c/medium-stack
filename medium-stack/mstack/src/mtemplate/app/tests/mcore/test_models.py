from ..conftest import *

from mcore.models import *


#
# tests
#


def test_user():
    user = example_model(User)
    user_cid = example_cid(User)

    _test_model_examples(User)
    _test_model_creator_and_examples(User, UserCreator)
    _test_model_generator(User, UserCreator)

    _test_model_dump(user, user_cid, User)
    _test_model_json_str(user, user_cid, User)
    
    user.id = ObjectId()
    _test_model_dump(user, user_cid, User)
    _test_model_json_str(user, user_cid, User)


def test_profile():
    profile = example_model(Profile)
    profile_cid = example_cid(Profile)

    _test_model_examples(Profile)
    _test_model_creator_and_examples(Profile, ProfileCreator)
    _test_model_generator(Profile, ProfileCreator)

    _test_model_dump(profile, profile_cid, Profile)
    _test_model_json_str(profile, profile_cid, Profile)
    
    profile.id = ObjectId()
    _test_model_dump(profile, profile_cid, Profile)
    _test_model_json_str(profile, profile_cid, Profile)


def test_file_uploader():
    file_uploader = example_model(FileUploader)

    _test_model_examples(FileUploader)
    _test_model_creator_and_examples(FileUploader, FileUploaderCreator)

    _test_model_dump(file_uploader, None, FileUploader)
    _test_model_json_str(file_uploader, None, FileUploader)
    
    file_uploader.id = ObjectId()
    _test_model_dump(file_uploader, None, FileUploader)
    _test_model_json_str(file_uploader, None, FileUploader)


def test_image_file(image_file, image_file_cid, image_file_payload):
    assert image_file.payload_cid == image_file_payload
    _test_model_examples(ImageFile)

    assert image_file.height == 3584
    assert isinstance(image_file.height, int)
    assert image_file.width == 5376
    assert isinstance(image_file.width, int)

    _test_model_dump(image_file, image_file_cid, ImageFile) 
    _test_model_json_str(image_file, image_file_cid, ImageFile)

    image_file.id = ObjectId()
    _test_model_dump(image_file, image_file_cid, ImageFile) 
    _test_model_json_str(image_file, image_file_cid, ImageFile)


def test_image_release(image_release_cid):
    _test_model_examples(ImageRelease)
    _test_model_creator_and_examples(ImageRelease, ImageReleaseCreator)

    image_release = example_model(ImageRelease)

    _test_model_dump(image_release, image_release_cid, ImageRelease)
    _test_model_json_str(image_release, image_release_cid, ImageRelease)

    image_release.id = ObjectId()
    _test_model_dump(image_release, image_release_cid, ImageRelease)
    _test_model_json_str(image_release, image_release_cid, ImageRelease)


def test_audio_file(audio_file, audio_file_cid, audio_file_payload):
    assert audio_file.payload_cid == audio_file_payload
    _test_model_examples(AudioFile)

    assert audio_file.duration == 65.828
    assert audio_file.bit_rate == 320000
    assert isinstance(audio_file.bit_rate, int)

    _test_model_dump(audio_file, audio_file_cid, AudioFile) 
    _test_model_json_str(audio_file, audio_file_cid, AudioFile)

    audio_file.id = ObjectId()
    _test_model_dump(audio_file, audio_file_cid, AudioFile) 
    _test_model_json_str(audio_file, audio_file_cid, AudioFile)


def test_audio_release(audio_release_cid):
    _test_model_examples(AudioRelease)
    _test_model_creator_and_examples(AudioRelease, AudioReleaseCreator)

    audio_release = example_model(AudioRelease)

    _test_model_dump(audio_release, audio_release_cid, AudioRelease)
    _test_model_json_str(audio_release, audio_release_cid, AudioRelease)

    audio_release.id = ObjectId()
    _test_model_dump(audio_release, audio_release_cid, AudioRelease)
    _test_model_json_str(audio_release, audio_release_cid, AudioRelease)


def test_video_file(video_file, video_file_cid, video_file_payload):
    _test_model_examples(VideoFile)

    assert video_file.payload_cid == video_file_payload
    assert video_file.height == 480
    assert isinstance(video_file.height, int)
    assert video_file.width == 853
    assert isinstance(video_file.width, int)
    assert video_file.duration == 32.995
    assert video_file.bit_rate == 2681864
    assert isinstance(video_file.bit_rate, int)
    assert video_file.has_audio is True

    _test_model_dump(video_file, video_file_cid, VideoFile)
    _test_model_json_str(video_file, video_file_cid, VideoFile)

    video_file.id = ObjectId()
    _test_model_dump(video_file, video_file_cid, VideoFile)
    _test_model_json_str(video_file, video_file_cid, VideoFile)


def test_video_release(video_release_cid):
    _test_model_examples(VideoRelease)
    _test_model_creator_and_examples(VideoRelease, VideoReleaseCreator)

    video_release = example_model(VideoRelease)

    _test_model_dump(video_release, video_release_cid, VideoRelease)
    _test_model_json_str(video_release, video_release_cid, VideoRelease)

    video_release.id = ObjectId()
    _test_model_dump(video_release, video_release_cid, VideoRelease)
    _test_model_json_str(video_release, video_release_cid, VideoRelease)


def test_text_file():
    pass


if __name__ == '__main__':
    test_user()