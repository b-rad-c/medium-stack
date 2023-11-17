from mcore.types import ContentId
from mcore.db import MongoDB
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
