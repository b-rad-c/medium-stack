from ..conftest import reset_collection, _test_client_crud_ops, _check_client_response_id, mstack

import time

from typing import List

from mcore.types import ContentId
from mcore.client import *
from mcore.models import *
from mcore.errors import NotFoundError
from mserve import IndexResponse

import pytest

#
# main + core
#

def test_main():
    data = mstack.index()
    assert mstack.response.status_code == 200
    assert isinstance(data, IndexResponse)

def test_core_users():
    _test_client_crud_ops(
        User, 
        UserCreator, 
        mstack.create_user, 
        mstack.list_users, 
        mstack.read_user, 
        mstack.delete_user
    )

def test_core_file_uploader():

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
        _check_client_response_id(mstack)

    # read #

    uploader_read = mstack.read_file_uploader(id=created_uploader.id)
    assert uploader_read == created_uploader
    _check_client_response_id(mstack)

    # list #

    uploader_list = mstack.list_file_uploaders()
    assert len(uploader_list) == 10
    for uploader in uploader_list:
        assert isinstance(uploader, FileUploader)

    _check_client_response_id(mstack)

    # pagination by 10 #

    assert len(mstack.list_file_uploaders(offset=0, size=10)) == 10
    _check_client_response_id(mstack)

    # pagination by 5 #

    total = 0
    for offset in range(0, 10, 5):
        for uploader in mstack.list_file_uploaders(offset=offset, size=5):
            assert isinstance(uploader, FileUploader)
            total += 1

    assert total == 10
    _check_client_response_id(mstack)

    # pagination by 3 #

    total = 0
    for offset in range(0, 10, 3):
        for uploader in mstack.list_file_uploaders(offset=offset, size=3):
            assert isinstance(uploader, FileUploader)
            total += 1

    assert total == 10
    _check_client_response_id(mstack)

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

def test_core_file_upload_process(image_file_path):
    updates:List[FileUploader] = []

    def progress(uploader:FileUploader):
        updates.append(uploader)

    uploader = mstack.upload_file(image_file_path, FileUploadTypes.image, on_update=progress)

    assert uploader.status == FileUploadStatus.process_queue

    last_uploaded = -1
    for update in updates:
        assert update.total_uploaded <= update.total_size
        assert update.total_uploaded > last_uploaded

        if update.total_uploaded == update.total_size:
            assert update.status == FileUploadStatus.process_queue
        else:
            assert update.status == FileUploadStatus.uploading
        
        last_uploaded = update.total_uploaded

    for _ in range(10):
        uploader = mstack.read_file_uploader(id=uploader.id)
        if uploader.status not in [FileUploadStatus.processing, FileUploadStatus.process_queue]:
            break
        time.sleep(0.5)
    
    assert uploader.status == FileUploadStatus.complete
    assert uploader.result_cid is not None
    assert isinstance(uploader.result_cid, ContentId)
