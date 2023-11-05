from mcore.types import ContentId
from mcore.models import User, FileUploader, FileUploadTypes, FileUploadStatus, ImageFile, AudioFile, VideoFile

from pathlib import Path

import pytest


SAMPLE_BIN = Path(__file__).parent / 'samples'


@pytest.fixture(scope='session')
def user():
    return User(email='test@example.com', phone_number='tel:+1-513-555-0123', first_name='Jane', middle_name='C', last_name='Doe')


@pytest.fixture(scope='session')
def user_cid():
    """cids should be hardcoded strings for testing to ensure the cid generation logic doesn't change"""
    return ContentId(hash='qCOVki8sEA_Nt-5dsPc6402H7JIpEN1q3na_e7WzkIE', size=130, ext='json')


@pytest.fixture(scope='session')
def file_uploader():
    return FileUploader(type=FileUploadTypes.image, total_size=100_000, status=FileUploadStatus.uploading, total_uploaded=10_000)


@pytest.fixture(scope='session')
def image_file():
    name = 'Water_reflection_of_stringy_gray_and_white_clouds_in_a_pond_on_a_sand_beach_of_Don_Khon_at_sunrise_in_Laos.jpg'
    path = SAMPLE_BIN / name
    return ImageFile.from_filepath(path)


@pytest.fixture(scope='session')
def image_file_cid():
    return ContentId(hash='VcRfJsAIeMvHFxW2c1FFgk2PFc5S16zFEydoCtKhaSg', size=105, ext='json')


@pytest.fixture(scope='session')
def image_file_payload():
    return ContentId(hash='Wh2aaOSrURBH32Z_Dgg8BgHB_fQllwLo_0arWPH_PQo', size=7103671, ext='jpg')


@pytest.fixture(scope='session')
def audio_file():
    path = SAMPLE_BIN / 'Maarten Schellekens - The 4t of May.mp3'
    return AudioFile.from_filepath(path)


@pytest.fixture(scope='session')
def audio_file_cid():
    return ContentId(hash='qB-A2d1Jt-DTBqAZZgBuTvH4tDbIFpxyfWmkxTZejXo', size=114, ext='json')


@pytest.fixture(scope='session')
def audio_file_payload():
    return ContentId(hash='SOT7ZsLeQYg6MbcabM049T_DKWbLXl6BR724v3xD9fo', size=2633142, ext='mp3')


@pytest.fixture(scope='session')
def video_file():
    path = SAMPLE_BIN / 'big_buck_bunny_trailer_480p.mov'
    return VideoFile.from_filepath(path)


@pytest.fixture(scope='session')
def video_file_cid():
    return ContentId(hash='r62C64HF6Qn5WqjilmNmSlsZjnK52ifR178pPyA8bgI', size=164, ext='json')


@pytest.fixture(scope='session')
def video_file_payload():
    return ContentId(hash='j_d4uuRMK-Q2LIoT-n6oIT_oE-nriwlp_K8_W8oa1r0', size=11061011, ext='mov')
