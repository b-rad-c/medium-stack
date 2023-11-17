from ..conftest import example_model, example_cid

from typing import Type

from mcore.db import MongoDB
from mcore.models import *
from mcore.errors import NotFoundError, MStackDBError

import pytest

from bson import ObjectId
from pydantic import BaseModel


db = MongoDB.from_cache()


def _drop_collection(model_type):
    collection = db.get_collection(model_type)
    collection.drop()


def _verify_does_not_exist(obj):
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


def _test_model(obj, obj_cid, model_type):
    if obj_cid is not None:
        assert obj.cid == obj_cid
        _drop_collection(model_type)
    
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
    _verify_does_not_exist(obj)

    # db delete method (id signature) #
    db.create(obj)
    db.delete(model_type, id=obj.id)
    _verify_does_not_exist(obj)

    if obj_cid is not None:
        # db delete method (cid signature) #
        db.create(obj)
        db.delete(model_type, cid=obj_cid)
        _verify_does_not_exist(obj)

        # db delete method (id + cid signature) #
        db.create(obj)
        db.delete(model_type, id=obj.id, cid=obj_cid)
        _verify_does_not_exist(obj)

    with pytest.raises(MStackDBError):
        db.delete(model_type)

    if obj_cid is not None:
        _drop_collection(model_type)


def _test_pagination(model:BaseModel, model_type:Type):

    _drop_collection(model_type)

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

    _drop_collection(model_type)


def test_user():
    user_creator:UserCreator = example_model(UserCreator)
    user = user_creator.create_model()
    user_cid = example_cid(User)
    _test_model(user, user_cid, User)
    _test_pagination(user, User)


def test_file_uploader():
    creator:FileUploaderCreator = example_model(FileUploaderCreator)
    user_cid = example_cid(User)
    file_uploader = creator.create_model(user_cid=user_cid)
    _test_model(file_uploader, None, FileUploader)
    _test_pagination(file_uploader, FileUploader)


def test_image_file(image_file, image_file_cid):
    _test_model(image_file, image_file_cid, ImageFile)
    _test_pagination(image_file, ImageFile)


def test_audio_file(audio_file, audio_file_cid):
    _test_model(audio_file, audio_file_cid, AudioFile)
    _test_pagination(audio_file, AudioFile)


def test_video_file(video_file, video_file_cid):
    _test_model(video_file, video_file_cid, VideoFile)
    _test_pagination(video_file, VideoFile)


def test_text_file():
    pass
