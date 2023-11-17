from mcore.models import *

from bson import ObjectId

from pydantic import BaseModel

#
# reusable functions
#

def _test_dumped_model(obj, cid, model_type):
    as_dict = obj.model_dump()

    if issubclass(model_type, ContentModel):
        assert as_dict['cid'] == str(cid)

    try:
        assert isinstance(as_dict['payload_cid'], str)
    except KeyError:
        "ignore if model doesn't have payload_cid"
    

    if obj.id is None:
        assert as_dict['id'] is None
    else:
        assert as_dict['id'] == obj.id

    assert '_id' not in as_dict

    assert obj == model_type(**as_dict)     # create model with cid string
    
    if issubclass(model_type, ContentModel):
        as_dict['cid'] = cid

    assert obj == model_type(**as_dict)     # create model with cid object


def _test_model_json_str(obj, cid, model_type):
    as_json = obj.model_dump_json()

    if issubclass(model_type, ContentModel):
        assert str(cid) in as_json

    if obj.id is None:
        assert '"id":null' in as_json
    else:
        assert f'"id":"{obj.id}"' in as_json

    # fod models that have a payload cid, assert that it is not getting dumped as a dict
    assert '"payload_cid":{' not in as_json
    
    assert '"_id"' not in as_json

    assert obj == model_type.model_validate_json(as_json)


def _test_model_examples(model_type:BaseModel):
    try:
        examples = model_type.model_json_schema()['examples']
    except KeyError:
        raise TypeError(f'model {model_type.__name__} does not have examples defined')
    
    assert len(examples) > 0
    
    for example in examples:
        model = model_type(**example)
        assert isinstance(model, model_type)


def _test_model_creator_and_examples(model_type, model_creator_type:ModelCreator):
    try:
        examples = model_creator_type.model_json_schema()['examples']
    except KeyError:
        raise TypeError(f'model {model_creator_type.__name__} does not have examples defined')
    
    assert len(examples) > 0
    
    for example in examples:
        model_creator:ModelCreator = model_creator_type(**example)
        model = model_creator.create_model()
        assert isinstance(model, model_type)


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