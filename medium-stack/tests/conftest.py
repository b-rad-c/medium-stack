from mcore.types import ContentId
from mcore.mongo import MongoDB
from mcore.models import User, FileUploader, FileUploadTypes, FileUploadStatus, ImageFile, AudioFile, VideoFile

from pathlib import Path

import pytest

from pydantic import BaseModel

SAMPLE_BIN = Path(__file__).parent / 'samples'

#
# db fixtures
#

@pytest.fixture(scope='function')
def db():
    return MongoDB.from_cache()


@pytest.fixture(scope='function')
def reset_collection(db):
    return lambda model_type: db.get_collection(model_type).drop()


#
# model fixtures
#

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

@pytest.fixture(scope='function')
def user():
    return example_model(User)


@pytest.fixture(scope='function')
def user_cid():
    return example_cid(User)


@pytest.fixture(scope='function')
def file_uploader():
    return example_model(FileUploader)


@pytest.fixture(scope='function')
def image_file():
    name = 'Water_reflection_of_stringy_gray_and_white_clouds_in_a_pond_on_a_sand_beach_of_Don_Khon_at_sunrise_in_Laos.jpg'
    path = SAMPLE_BIN / name
    return ImageFile.from_filepath(path)


@pytest.fixture(scope='function')
def image_file_cid():
    return ContentId(hash='VcRfJsAIeMvHFxW2c1FFgk2PFc5S16zFEydoCtKhaSg', size=105, ext='json')


@pytest.fixture(scope='function')
def image_file_payload():
    return ContentId(hash='Wh2aaOSrURBH32Z_Dgg8BgHB_fQllwLo_0arWPH_PQo', size=7103671, ext='jpg')


@pytest.fixture(scope='function')
def audio_file():
    path = SAMPLE_BIN / 'Maarten Schellekens - The 4t of May.mp3'
    return AudioFile.from_filepath(path)


@pytest.fixture(scope='function')
def audio_file_cid():
    return ContentId(hash='qB-A2d1Jt-DTBqAZZgBuTvH4tDbIFpxyfWmkxTZejXo', size=114, ext='json')


@pytest.fixture(scope='function')
def audio_file_payload():
    return ContentId(hash='SOT7ZsLeQYg6MbcabM049T_DKWbLXl6BR724v3xD9fo', size=2633142, ext='mp3')


@pytest.fixture(scope='function')
def video_file():
    path = SAMPLE_BIN / 'big_buck_bunny_trailer_480p.mov'
    return VideoFile.from_filepath(path)


@pytest.fixture(scope='function')
def video_file_cid():
    return ContentId(hash='r62C64HF6Qn5WqjilmNmSlsZjnK52ifR178pPyA8bgI', size=164, ext='json')


@pytest.fixture(scope='function')
def video_file_payload():
    return ContentId(hash='j_d4uuRMK-Q2LIoT-n6oIT_oE-nriwlp_K8_W8oa1r0', size=11061011, ext='mov')
