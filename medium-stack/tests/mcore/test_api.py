from string import ascii_uppercase

from mcore.api import *
from mcore.models import *
from mcore.mongo import MongoDB
from mcore.errors import NotFoundError
from mserve import IndexResponse

import pytest

mstack = MStackClient()
db = MongoDB.from_cache()

def _reset_collection(model_type):
    db.get_collection(model_type).drop()


def test_main():
    data = mstack.index()
    assert mstack.response.status_code == 200
    assert isinstance(data, IndexResponse)


def test_core_users():

    # init #

    _reset_collection(User)
    assert len(mstack.list_users()) == 0, 'user collection was not reset'

    # create #

    creator_params = UserCreator.model_config['json_schema_extra']['examples'][0]
    created_users = []
    
    for index in range(10):
        new_user = UserCreator(**creator_params)        # create user by incrementing middle initial
        new_user.middle_name = ascii_uppercase[index]   # to ensure each user has a unique cid

        created_user = mstack.create_user(new_user)
        created_users.append(created_user)
        assert isinstance(created_user, User)

    # read #

    user_read_id = mstack.read_user(id=created_user.id)
    assert user_read_id == created_user

    user_read_cid = mstack.read_user(cid=created_user.cid)
    assert user_read_cid == created_user

    # list #

    user_list = mstack.list_users()
    assert len(user_list) == 10
    for user in user_list:
        assert isinstance(user, User)

    # pagination by 10 #

    assert len(mstack.list_users(offset=0, size=10)) == 10

    # pagination by 5 #

    total = 0
    for offset in range(0, 10, 5):
        for user in mstack.list_users(offset=offset, size=5):
            assert isinstance(user, User)
            total += 1
    assert total == 10

    # pagination by 3 #

    total = 0
    for offset in range(0, 10, 3):
        for user in mstack.list_users(offset=offset, size=3):
            assert isinstance(user, User)
            total += 1

    assert total == 10

    # delete by id #

    result = mstack.delete_user(id=created_users[0].id)
    assert result is None
    assert mstack.response.status_code == 201

    result = mstack.delete_user(id=created_users[0].id)    # run delete again because the endpoint is designed 
    assert result is None                                  # to return the same response if the item was already deleted
    assert mstack.response.status_code == 201

    with pytest.raises(NotFoundError):
        mstack.read_user(id=created_users[0].id)

    # delete by cid #

    result = mstack.delete_user(cid=created_users[1].cid)
    assert result is None
    assert mstack.response.status_code == 201

    result = mstack.delete_user(cid=created_users[1].cid)
    assert result is None
    assert mstack.response.status_code == 201

    with pytest.raises(NotFoundError):
        mstack.read_user(cid=created_users[1].cid)


def test_core_file_uploader():
    pass