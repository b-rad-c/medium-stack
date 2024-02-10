from typing import Type, Callable

from mcore.auth import create_new_user
from mcore.client import *
from mcore.types import ContentId
from mcore.models import *
from mcore.db import MongoDB
from mcore.errors import NotFoundError, MStackDBError
from mcore.util import example_model, example_cid

from pathlib import Path

import pytest

from pydantic import BaseModel
from bson import ObjectId


__all__ = [
    'ObjectId',
    'SAMPLE_BIN',
    'user_cid',

    'reset_collection',
    'example_model',
    'example_cid',

    '_test_model_dump',
    '_test_model_json_str',
    '_test_model_examples',
    '_test_model_creator_and_examples',
    '_test_model_generator',

    '_test_db_does_not_exist',
    '_test_db_crud',
    '_test_db_pagination',

    '_test_client_crud_ops'
]


SAMPLE_BIN = Path(__file__).parent / 'samples'

db = MongoDB.from_cache()

user_cid = example_cid(User)

#
# helpers
#

def reset_collection(model_type):
    db.get_collection(model_type).drop()

#
# reusable model tests
#

def _test_model_dump(obj, cid, model_type):
    as_dict = obj.model_dump()

    if issubclass(model_type, ContentModel):
        assert as_dict['cid'] == str(cid)

    try:
        assert isinstance(as_dict['payload_cid'], str | None)
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

def _test_model_creator_and_examples(model_type:BaseModel, model_creator_type:ModelCreator):
    try:
        examples = model_creator_type.model_json_schema()['examples']
    except KeyError:
        raise TypeError(f'model {model_creator_type.__name__} does not have examples defined')
    
    assert len(examples) > 0
    
    for example in examples:
        model_creator:ModelCreator = model_creator_type(**example)
        model = model_creator.create_model(user_cid=example_cid(User))
        assert isinstance(model, model_type)

def _test_model_generator(model_type:BaseModel, model_creator_type:ModelCreator):
    model_creator:ModelCreator = model_creator_type.generate()
    assert isinstance(model_creator, model_creator_type)

    model = model_creator.generate_model()
    assert isinstance(model, model_type)

#
# reusable db tests
#

def _test_db_does_not_exist(obj):
    with pytest.raises(NotFoundError):
        db.read(obj)
    with pytest.raises(NotFoundError):
        db.read(obj.__class__, id=obj.id)
    try:
        with pytest.raises(NotFoundError):
            db.read(obj.__class__, cid=str(obj.cid))
        with pytest.raises(NotFoundError):
            db.read(obj.__class__, id=obj.id, cid=str(obj.cid))
    except AttributeError:
        pass

def _test_db_crud(obj, obj_cid, model_type):
    reset_collection(model_type)

    if obj_cid is not None:
        assert obj.cid == obj_cid
        
    # insert into db and verify id #
    assert obj.id is None
    db.create(obj)
    assert isinstance(obj.id, ObjectId)

    # verify raw db entry #
    col = db.get_collection(obj)
    db_entry = col.find_one({'_id': obj.id})
    assert db_entry is not None
    assert 'id' not in db_entry
    assert obj == model_type(**db_entry)
    if obj_cid is not None:
        assert db_entry['cid'] == str(obj_cid)

    # db read method (each signature) #
    assert db.read(obj) == obj
    assert db.read(model_type, id=obj.id) == obj
    if obj_cid is not None:
        assert db.read(model_type, cid=obj_cid) == obj
        assert db.read(model_type, id=obj.id, cid=obj_cid) == obj

    with pytest.raises(MStackDBError):
        db.read(model_type)

    # db delete method (instance signature) #
    db.delete(obj)
    _test_db_does_not_exist(obj)

    # db delete method (id signature) #
    db.create(obj)
    db.delete(model_type, id=obj.id)
    _test_db_does_not_exist(obj)

    if obj_cid is not None:
        # db delete method (cid signature) #
        db.create(obj)
        db.delete(model_type, cid=obj_cid)
        _test_db_does_not_exist(obj)

        # db delete method (id + cid signature) #
        db.create(obj)
        db.delete(model_type, id=obj.id, cid=obj_cid)
        _test_db_does_not_exist(obj)

    with pytest.raises(MStackDBError):
        db.delete(model_type)

    reset_collection(model_type)

def _test_db_pagination(model:BaseModel, model_type:Type):

    reset_collection(model_type)

    # create multiple entries

    entries = []

    for _ in range(10):
        new_entry = model.model_copy()
        entries.append(db.create(new_entry))

    # list #

    model_list = db.find(model_type)
    assert len(list(model_list)) == 10
    for entry in model_list:
        assert isinstance(entry, model_type)

    # pagination by 10 #
    model_list = db.find(model_type, offset=0, size=10)
    assert len(list(model_list)) == 10

    # pagination by 5 #

    total = 0
    for offset in range(0, 10, 5):
        for entry in db.find(model_type, offset=offset, size=5):
            assert isinstance(entry, model_type)
            total += 1

    assert total == 10

    # pagination by 3 #

    total = 0
    for offset in range(0, 10, 3):
        for entry in db.find(model_type, offset=offset, size=3):
            assert isinstance(entry, model_type)
            total += 1

    assert total == 10

    reset_collection(model_type)


#
# reusable client tests
#

def _check_client_response_id(mstack:MStackClient):
    data = mstack.response.json()
    if isinstance(data, list):
        for item in data:
            assert '_id' not in item
            assert 'id' in item
    elif isinstance(data, dict):
        assert '_id' not in data
        assert 'id' in data
    else:
        raise Exception('Invalid response type')

def _test_client_crud_ops(
        mstack:MStackClient,
        model_type:ContentModel, 
        model_creator:ModelCreator, 
        create_op:Callable, 
        list_op:Callable,
        read_op:Callable,
        delete_op:Callable
    ):

    # init #

    reset_collection(model_type)

    # create #

    for _ in range(10):
        created_model = create_op(example_model(model_creator))
        assert isinstance(created_model, model_type)
        _check_client_response_id(mstack)

    # list #

    model_list = list_op()
    assert len(model_list) == 10
    for model in model_list:
        assert isinstance(model, model_type)
    
    _check_client_response_id(mstack)

    # pagination by 10 #

    assert len(list_op(offset=0, size=10)) == 10
    _check_client_response_id(mstack)

    # pagination by 5 #

    total = 0
    for offset in range(0, 10, 5):
        for model in list_op(offset=offset, size=5):
            assert isinstance(model, model_type)
            total += 1

    assert total == 10
    _check_client_response_id(mstack)

    # pagination by 3 #

    total = 0
    for offset in range(0, 10, 3):
        for model in list_op(offset=offset, size=3):
            assert isinstance(model, model_type)
            total += 1

    assert total == 10
    _check_client_response_id(mstack)

    # read #

    reset_collection(model_type)

    model = create_op(example_model(model_creator))

    read_by_id = read_op(id=model.id)
    assert read_by_id == model
    _check_client_response_id(mstack)

    read_by_cid = read_op(cid=model.cid)
    assert read_by_cid == model
    _check_client_response_id(mstack)

    # delete by id #

    result = delete_op(id=model.id)
    assert result is None
    assert mstack.response.status_code == 201

    result = delete_op(id=model.id)             # run delete again because the endpoint is designed 
    assert result is None                       # to return the same response if the item was already deleted
    assert mstack.response.status_code == 201

    with pytest.raises(NotFoundError):
        read_op(id=model.id)

    # delete by cid #

    model = create_op(example_model(model_creator))

    result = delete_op(cid=model.cid)
    assert result is None
    assert mstack.response.status_code == 201

    result = delete_op(cid=model.cid)
    assert result is None
    assert mstack.response.status_code == 201

    with pytest.raises(NotFoundError):
        read_op(cid=model.cid)

    reset_collection(model_type)


#
# fixtures
#

@pytest.fixture(scope='session')
def client() -> MStackClient:
    reset_collection(User)
    reset_collection(UserPasswordHash)

    user_creator = UserCreator.generate()
    create_new_user(user_creator)

    mstack = MStackClient()
    mstack.login(user_creator.email, user_creator.password1)

    return mstack



# image #

@pytest.fixture(scope='session')
def image_file_path():
    name = 'Water_reflection_of_stringy_gray_and_white_clouds_in_a_pond_on_a_sand_beach_of_Don_Khon_at_sunrise_in_Laos.jpg'
    return SAMPLE_BIN / name

@pytest.fixture(scope='function')
def image_file(image_file_path):
    return ImageFile.from_filepath(image_file_path, example_cid(User))

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
def audio_file(audio_file_path):
    return AudioFile.from_filepath(audio_file_path, example_cid(User))

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
def video_file(video_file_path):
    return VideoFile.from_filepath(video_file_path, example_cid(User))

@pytest.fixture(scope='function')
def video_file_cid():
    return ContentId(hash='ixiuws1Ouxe9Vw1-IarCNYwvWdUZBhZOaR_IlngkiEk', size=232, ext='json')

@pytest.fixture(scope='function')
def video_file_payload():
    return ContentId(hash='j_d4uuRMK-Q2LIoT-n6oIT_oE-nriwlp_K8_W8oa1r0', size=11061011, ext='mov')
