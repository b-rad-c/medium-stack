import pytest
from bson import ObjectId
from typing import Annotated, List
from pydantic import BaseModel, ValidationError
from mcore.types import DataHierarchy, _validate_object_id, unique_list_validator, _list_is_unique, TagList


def test_mongo_id():
    obj_id_string = '653456b4375e9bbe89939316'
    obj_id = ObjectId('653456b4375e9bbe89939316')

    assert _validate_object_id(None) is None

    assert _validate_object_id(obj_id_string) == obj_id
    assert _validate_object_id(obj_id) == obj_id

    assert isinstance(_validate_object_id(obj_id_string), ObjectId)
    assert isinstance(_validate_object_id(obj_id), ObjectId)

def test_data_hierarchy():
    hierarchy = 'root/sub/topic'
    hierarchy_obj = DataHierarchy.validate(hierarchy)

    assert hierarchy_obj.string == hierarchy
    assert len(hierarchy_obj.levels) == 3
    assert hierarchy_obj.levels[0] == 'root'
    assert hierarchy_obj.levels[1] == 'sub'
    assert hierarchy_obj.levels[2] == 'topic'
    assert str(hierarchy_obj) == hierarchy

    with pytest.raises(ValueError):
        DataHierarchy.validate('/a/b//c')

    with pytest.raises(ValueError):
        DataHierarchy.validate('')

    with pytest.raises(ValueError):
        DataHierarchy.validate(1)

    with pytest.raises(ValueError):
        DataHierarchy.validate(None)
    
    with pytest.raises(ValueError):
        DataHierarchy.validate(True)

    with pytest.raises(ValueError):
        DataHierarchy.validate(['a', 'b', 'c'])

    with pytest.raises(ValueError):
        DataHierarchy.validate({'a': 1, 'b': 2, 'c': 3})

    with pytest.raises(ValueError):
        DataHierarchy.validate(['root', 'sub', 'topic'])

def test_unique_list():
    _list_is_unique([1, 2, 3])
    _list_is_unique(['a', 'b', 'c'])
    _list_is_unique([True, False])

    with pytest.raises(ValueError):
        _list_is_unique([1, 2, 3, 1])

    with pytest.raises(ValueError):
        _list_is_unique(['a', 'b', 'c', 'a'])

    with pytest.raises(ValueError):
        _list_is_unique([True, False, True])

    class TestModel(BaseModel):
        names: Annotated[List[str], unique_list_validator]

    TestModel(names=['alice', 'bob', 'charlie'])

    with pytest.raises(ValidationError):
        TestModel(names=['alice', 'bob', 'alice'])


def test_tag_list():

    class TestModel(BaseModel):
        tags: TagList

    TestModel(tags=['red', 'green', 'blue'])
    TestModel(tags=None)

    with pytest.raises(ValidationError):
        TestModel(tags=['red', 'green', 'red'])

    with pytest.raises(ValidationError):
        TestModel(tags=[1, 2, 3])

    long_tag_list = []
    for n in range(0, 20):
        long_tag_list.append(f'tag{n}')
    
    with pytest.raises(ValidationError):
        TestModel(tags=long_tag_list)
