from mcore.mongo import MongoDB
from mcore.models import User, ImageFile, AudioFile, VideoFile
from mcore.errors import NotFoundError, MStackDBError
from bson import ObjectId
import pytest


db = MongoDB.from_cache()


def _reset_cid(obj):
    user_collection = db.get_collection(obj)
    user_collection.delete_many({'cid': str(obj.cid)})


def _verify_does_not_exist(obj):
    with pytest.raises(NotFoundError):
        db.read(obj)
    with pytest.raises(NotFoundError):
        db.read(obj.__class__, id=obj.id)
    with pytest.raises(NotFoundError):
        db.read(obj.__class__, cid=str(obj.cid))
    with pytest.raises(NotFoundError):
        db.read(obj.__class__, id=obj.id, cid=str(obj.cid))


def _test_model(obj, obj_cid, model_type):
    assert obj.cid == obj_cid
    _reset_cid(obj)
    
    # insert into db and verify id #
    db.create(obj)
    assert isinstance(obj.id, ObjectId)

    # verify raw db entry #
    col = db.get_collection(obj)
    db_entry = col.find_one({'_id': obj.id})
    assert db_entry is not None
    assert 'id' not in db_entry
    assert db_entry['cid'] == str(obj_cid)
    assert obj == model_type(**db_entry)

    # db read method (each signature) #
    assert db.read(obj) == obj
    assert db.read(model_type, id=obj.id) == obj
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

    _reset_cid(obj)


def test_user(user, user_cid):
    _test_model(user, user_cid, User)


def test_image_file(image_file, image_file_cid):
    _test_model(image_file, image_file_cid, ImageFile)


def test_audio_file(audio_file, audio_file_cid):
    _test_model(audio_file, audio_file_cid, AudioFile)


def test_video_file(video_file, video_file_cid):
    _test_model(video_file, video_file_cid, VideoFile)


def test_text_file():
    pass
