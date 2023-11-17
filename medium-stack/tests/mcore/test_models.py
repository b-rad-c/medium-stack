from ..conftest import *

from mcore.models import *


#
# tests
#


def test_user(user, user_cid):
    _test_model_examples(User)
    _test_model_creator_and_examples(User, UserCreator)

    _test_dumped_model(user, user_cid, User)
    _test_model_json_str(user, user_cid, User)
    
    user.id = ObjectId()
    _test_dumped_model(user, user_cid, User)
    _test_model_json_str(user, user_cid, User)


def test_file_uploader(file_uploader):
    _test_model_examples(FileUploader)
    _test_model_creator_and_examples(FileUploader, FileUploaderCreator)

    _test_dumped_model(file_uploader, None, FileUploader)
    _test_model_json_str(file_uploader, None, FileUploader)
    
    file_uploader.id = ObjectId()
    _test_dumped_model(file_uploader, None, FileUploader)
    _test_model_json_str(file_uploader, None, FileUploader)


def test_image_file(image_file, image_file_cid, image_file_payload):
    assert image_file.payload_cid == image_file_payload
    _test_model_examples(ImageFile)

    assert image_file.height == 3584
    assert isinstance(image_file.height, int)
    assert image_file.width == 5376
    assert isinstance(image_file.width, int)

    _test_dumped_model(image_file, image_file_cid, ImageFile) 
    _test_model_json_str(image_file, image_file_cid, ImageFile)

    image_file.id = ObjectId()
    _test_dumped_model(image_file, image_file_cid, ImageFile) 
    _test_model_json_str(image_file, image_file_cid, ImageFile)


def test_audio_file(audio_file, audio_file_cid, audio_file_payload):
    assert audio_file.payload_cid == audio_file_payload
    _test_model_examples(AudioFile)

    assert audio_file.duration == 65.828
    assert audio_file.bit_rate == 320000
    assert isinstance(audio_file.bit_rate, int)

    _test_dumped_model(audio_file, audio_file_cid, AudioFile) 
    _test_model_json_str(audio_file, audio_file_cid, AudioFile)

    audio_file.id = ObjectId()
    _test_dumped_model(audio_file, audio_file_cid, AudioFile) 
    _test_model_json_str(audio_file, audio_file_cid, AudioFile)


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

    _test_dumped_model(video_file, video_file_cid, VideoFile)
    _test_model_json_str(video_file, video_file_cid, VideoFile)

    video_file.id = ObjectId()
    _test_dumped_model(video_file, video_file_cid, VideoFile)
    _test_model_json_str(video_file, video_file_cid, VideoFile)


def test_text_file():
    pass


if __name__ == '__main__':
    test_user()