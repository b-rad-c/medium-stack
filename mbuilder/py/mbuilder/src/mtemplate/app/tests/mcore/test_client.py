from ..conftest import reset_collection, _check_client_response_id, _test_client_crud_ops

import time

from typing import List
from pathlib import Path

from mcore.types import ContentId
from mcore.db import MongoDB
from mcore.client import *
from mcore.models import *
from mserve import IndexResponse

db = MongoDB.from_cache()

#
# main + core
#

def test_main(client):
    data = client.index()
    assert client.response.status_code == 200
    assert isinstance(data, IndexResponse)

def test_users(client:MStackClient):
    pass

def test_profiles(client:MStackClient):
    _test_client_crud_ops(
        client,
        Profile,
        ProfileCreator,
        client.profile_create,
        client.profile_list,
        client.profile_read,
        client.profile_delete
    )

def test_file_uploader(client:MStackClient):

    # init #

    reset_collection(FileUploader)
    assert len(client.file_uploaders_list()) == 0, 'file uploader collection was not reset'

    # create #

    creator_params = FileUploaderCreator.model_config['json_schema_extra']['examples'][0]
    created_uploaders = []

    for _ in range(10):
        new_uploader = FileUploaderCreator(**creator_params)
        new_uploader.total_size *= 1_000

        created_uploader = client.file_uploader_create(new_uploader)
        created_uploaders.append(created_uploader)
        assert isinstance(created_uploader, FileUploader)
        _check_client_response_id(client)

    # read #

    uploader_read = client.file_uploader_read(id=created_uploader.id)
    assert uploader_read == created_uploader
    _check_client_response_id(client)

    # list #

    uploader_list = client.file_uploaders_list()
    assert len(uploader_list) == 10
    for uploader in uploader_list:
        assert isinstance(uploader, FileUploader)

    _check_client_response_id(client)

    # pagination by 10 #

    assert len(client.file_uploaders_list(offset=0, size=10)) == 10
    _check_client_response_id(client)

    # pagination by 5 #

    total = 0
    for offset in range(0, 10, 5):
        for uploader in client.file_uploaders_list(offset=offset, size=5):
            assert isinstance(uploader, FileUploader)
            total += 1

    assert total == 10
    _check_client_response_id(client)

    # pagination by 3 #

    total = 0
    for offset in range(0, 10, 3):
        for uploader in client.file_uploaders_list(offset=offset, size=3):
            assert isinstance(uploader, FileUploader)
            total += 1

    assert total == 10
    _check_client_response_id(client)

    reset_collection(FileUploader)

def test_file_upload_process(image_file_path, client:MStackClient):
    updates:List[FileUploader] = []

    def progress(uploader:FileUploader):
        updates.append(uploader)

    uploader = client.upload_file(image_file_path, FileUploadTypes.image, on_update=progress)

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
        uploader = client.file_uploader_read(id=uploader.id)
        if uploader.status not in [FileUploadStatus.processing, FileUploadStatus.process_queue]:
            break
        time.sleep(0.5)
    
    assert uploader.status == FileUploadStatus.complete
    assert uploader.result_cid is not None
    assert isinstance(uploader.result_cid, ContentId)

def test_image_file(image_file, client:MStackClient):
    pass

def test_image_release(client:MStackClient, image_file_path:Path):
    image_file = ImageFile.ingest(image_file_path, client.user.cid, leave_original=True)
    db.create(image_file)

    _test_client_crud_ops(
        client, 
        ImageRelease, 
        ImageReleaseCreator, 
        client.image_release_create,
        client.image_release_list,
        client.image_release_read,
        client.image_release_delete
    )

def test_audio_file(audio_file, client:MStackClient):
    pass

def test_audio_release(client:MStackClient, audio_file_path:Path):
    audio_file = AudioFile.ingest(audio_file_path, client.user.cid, leave_original=True)
    db.create(audio_file)

    _test_client_crud_ops(
        client, 
        AudioRelease, 
        AudioReleaseCreator, 
        client.audio_release_create,
        client.audio_release_list,
        client.audio_release_read,
        client.audio_release_delete
    )

def test_video_file(video_file, client:MStackClient):
    pass

def test_video_release(client:MStackClient, video_file_path:Path):
    video_file = VideoFile.ingest(video_file_path, client.user.cid, leave_original=True)
    db.create(video_file)

    _test_client_crud_ops(
        client, 
        VideoRelease, 
        VideoReleaseCreator, 
        client.video_release_create,
        client.video_release_list,
        client.video_release_read,
        client.video_release_delete
    )
