from mcore.types import ContentId
from mcore.models import *
from mcore.db import MongoDB
from pathlib import Path

import pytest

from pydantic import BaseModel
from bson import ObjectId


__all__ = [
    'ObjectId',
    'SAMPLE_BIN',

    'reset_collection',
    'example_model',
    'example_cid',

    '_test_dumped_model',
    '_test_model_json_str',
    '_test_model_examples',
    '_test_model_creator_and_examples'
]




SAMPLE_BIN = Path(__file__).parent / 'samples'


#
# helpers
#


def reset_collection(model_type):
    db = MongoDB.from_cache()
    db.get_collection(model_type).drop()


def example_model(model_type:BaseModel, index=0):
    try:
        example = model_type.model_json_schema()['examples'][index]
    except KeyError:
        raise AssertionError(f'model {model_type.__class__.__name__} does not have examples defined')
    except IndexError:
        raise AssertionError(f'model {model_type.__class__.__name__} does not define example at index: {index}')
    
    return model_type(**example)


def example_cid(model_type:BaseModel, index=0):
    try:
        example = model_type.model_json_schema()['examples'][index]
    except KeyError:
        raise AssertionError(f'model {model_type.__class__.__name__} does not have examples defined')
    except IndexError:
        raise AssertionError(f'model {model_type.__class__.__name__} does not define example at index: {index}')
    
    try:
        cid = example['cid']
    except KeyError:
        raise AssertionError(f'model {model_type.__class__.__name__} does not define a cid in the example at index: {index}')
    
    return ContentId.parse(cid)


#
# reusable model tests
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
        try:
            assert str(model.cid) == example['cid']
        except (AttributeError, KeyError):
            """ignore if model doesn't have cid"""


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
# model fixtures
#


@pytest.fixture(scope='function')
def user():
    return example_model(User)


@pytest.fixture(scope='function')
def user_cid():
    return example_cid(User)


@pytest.fixture(scope='function')
def file_uploader():
    return example_model(FileUploader)

# image #

@pytest.fixture(scope='session')
def image_file_path():
    name = 'Water_reflection_of_stringy_gray_and_white_clouds_in_a_pond_on_a_sand_beach_of_Don_Khon_at_sunrise_in_Laos.jpg'
    return SAMPLE_BIN / name

@pytest.fixture(scope='function')
def image_file(image_file_path, user_cid):
    return ImageFile.from_filepath(image_file_path, user_cid)


@pytest.fixture(scope='function')
def image_file_cid():
    return ContentId(hash='tm9SzLy7lq1usQtHfGiJhznM95YSg9-NEF15WmnBobA', size=173, ext='json')


@pytest.fixture(scope='function')
def image_file_payload():
    return ContentId(hash='Wh2aaOSrURBH32Z_Dgg8BgHB_fQllwLo_0arWPH_PQo', size=7103671, ext='jpg')

# audio #

@pytest.fixture(scope='session')
def audio_file_path():
    name = 'Maarten Schellekens - The 4t of May.mp3'
    return SAMPLE_BIN / name

@pytest.fixture(scope='function')
def audio_file(audio_file_path, user_cid):
    return AudioFile.from_filepath(audio_file_path, user_cid)


@pytest.fixture(scope='function')
def audio_file_cid():
    return ContentId(hash='7BD1o8gwFLTaqr0S_QKk93iYcuFG1ZzCOKafaaPYiI4', size=182, ext='json')


@pytest.fixture(scope='function')
def audio_file_payload():
    return ContentId(hash='SOT7ZsLeQYg6MbcabM049T_DKWbLXl6BR724v3xD9fo', size=2633142, ext='mp3')

# video #

@pytest.fixture(scope='session')
def video_file_path():
    name = 'big_buck_bunny_trailer_480p.mov'
    return SAMPLE_BIN / name


@pytest.fixture(scope='function')
def video_file(video_file_path, user_cid):
    return VideoFile.from_filepath(video_file_path, user_cid)


@pytest.fixture(scope='function')
def video_file_cid():
    return ContentId(hash='ixiuws1Ouxe9Vw1-IarCNYwvWdUZBhZOaR_IlngkiEk', size=232, ext='json')


@pytest.fixture(scope='function')
def video_file_payload():
    return ContentId(hash='j_d4uuRMK-Q2LIoT-n6oIT_oE-nriwlp_K8_W8oa1r0', size=11061011, ext='mov')
