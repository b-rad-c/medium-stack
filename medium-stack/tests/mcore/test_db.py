from ..conftest import example_model, example_cid

from mcore.db import MongoDB
from mcore.models import *
from mcore.errors import NotFoundError, MStackDBError

import pytest

from bson import ObjectId


db = MongoDB.from_cache()


def _reset_cid(model_type, cid):
    collection = db.get_collection(model_type)
    collection.delete_many({'cid': str(cid)})


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


def _test_model_and_creator(obj_creator, model_type, obj_cid):
    
    if obj_cid is not None:
        _reset_cid(model_type, obj_cid)
    
    # insert into db and verify id #
    obj = db.create(obj_creator)
    assert isinstance(obj.id, ObjectId)

    # verify raw db entry #
    col = db.get_collection(obj)
    db_entry = col.find_one({'_id': obj.id})
    assert db_entry is not None
    assert 'id' not in db_entry
    if obj_cid is not None:
        assert db_entry['cid'] == str(obj_cid)
    assert obj == model_type(**db_entry)

    # db read method (each signature) #
    assert db.read(obj) == obj
    assert db.read(model_type, id=obj.id) == obj
    if obj_cid is not None:
        assert db.read(model_type, cid=obj_cid) == obj
        assert db.read(model_type, id=obj.id, cid=obj_cid) == obj
        assert obj.cid == obj_cid

    with pytest.raises(MStackDBError):
        db.read(model_type)

    # db delete method (instance signature) #
    db.delete(obj)
    _verify_does_not_exist(obj)

    # db delete method (id signature) #
    obj = db.create(obj_creator)
    db.delete(model_type, id=obj.id)
    _verify_does_not_exist(obj)

    # db delete method (cid signature) #
    if obj_cid is not None:
        obj = db.create(obj_creator)
        db.delete(model_type, cid=obj_cid)
        _verify_does_not_exist(obj)

    # db delete method (id + cid signature) #
    if obj_cid is not None:
        obj = db.create(obj_creator)
        db.delete(model_type, id=obj.id, cid=obj_cid)
        _verify_does_not_exist(obj)

    with pytest.raises(MStackDBError):
        db.delete(model_type)

    if obj_cid is not None:
        _reset_cid(model_type, obj_cid)


def _test_model(obj, obj_cid, model_type):
    if obj_cid is not None:
        assert obj.cid == obj_cid
        _reset_cid(model_type, obj_cid)
    
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
        _reset_cid(model_type, obj_cid)


def test_user():
    user_creator:UserCreator = example_model(UserCreator)
    user = user_creator.create_model()
    user_cid = example_cid(User)
    _test_model(user, user_cid, User)


def test_file_uploader():
    creator:FileUploaderCreator = example_model(FileUploaderCreator)
    file_uploader = creator.create_model()
    _test_model(file_uploader, None, FileUploader)


def test_image_file(image_file, image_file_cid):
    _test_model(image_file, image_file_cid, ImageFile)


def test_audio_file(audio_file, audio_file_cid):
    _test_model(audio_file, audio_file_cid, AudioFile)


def test_video_file(video_file, video_file_cid):
    _test_model(video_file, video_file_cid, VideoFile)


def test_text_file():
    pass
