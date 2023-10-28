import pytest
from bson import ObjectId
from mcore.types import DataHierarchy, _validate_object_id

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