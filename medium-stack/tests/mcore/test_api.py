from string import ascii_uppercase

from mcore.api import *
from mcore.models import *
from mcore.errors import NotFoundError
from mserve import IndexResponse

import pytest

mstack = MStackClient()


def test_main():
    data = mstack.index()
    assert mstack.response.status_code == 200
    assert isinstance(data, IndexResponse)


def test_core_users(reset_collection):

    # init #

    reset_collection(User)
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

    reset_collection(User)


def test_core_file_uploader(reset_collection):

    # init #

    reset_collection(FileUploader)
    assert len(mstack.list_file_uploaders()) == 0, 'file uploader collection was not reset'

    # create #

    creator_params = FileUploaderCreator.model_config['json_schema_extra']['examples'][0]
    created_uploaders = []

    for _ in range(10):
        new_uploader = FileUploaderCreator(**creator_params)
        new_uploader.total_size *= 1_000

        created_uploader = mstack.create_file_uploader(new_uploader)
        created_uploaders.append(created_uploader)
        assert isinstance(created_uploader, FileUploader)

    # read #

    uploader_read = mstack.read_file_uploader(id=created_uploader.id)
    assert uploader_read == created_uploader

    # list #

    uploader_list = mstack.list_file_uploaders()
    assert len(uploader_list) == 10
    for uploader in uploader_list:
        assert isinstance(uploader, FileUploader)

    # pagination by 10 #

    assert len(mstack.list_file_uploaders(offset=0, size=10)) == 10

    # pagination by 5 #

    total = 0
    for offset in range(0, 10, 5):
        for uploader in mstack.list_file_uploaders(offset=offset, size=5):
            assert isinstance(uploader, FileUploader)
            total += 1

    assert total == 10

    # pagination by 3 #

    total = 0
    for offset in range(0, 10, 3):
        for uploader in mstack.list_file_uploaders(offset=offset, size=3):
            assert isinstance(uploader, FileUploader)
            total += 1

    assert total == 10

    # delete by id #

    result = mstack.delete_file_uploader(id=created_uploader.id)
    assert result is None
    assert mstack.response.status_code == 201

    result = mstack.delete_file_uploader(id=created_uploader.id)    # run delete again because the endpoint is designed 
    assert result is None                                           # to return the same response if the item was already deleted
    assert mstack.response.status_code == 201

    with pytest.raises(NotFoundError):
        mstack.read_user(id=created_uploader.id)

    reset_collection(FileUploader)
