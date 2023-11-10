import os

from mcore.models import (
    FileUploader,
    FileUploadTypes,
    FileUploadStatus,
    ImageFile,
    AudioFile,
    VideoFile
)
from mcore.db import MongoDB
from mcore.util import DaemonController



MSERVE_INGEST_DAEMON_INTERVAL = float(os.environ.get('MSERVE_INGEST_DAEMON_INTERVAL', 2.5))
MSERVE_UPLOAD_CLEANUP_THRESHOLD = int(os.environ.get('MSERVE_UPLOAD_CLEANUP_THRESHOLD', 3600))
MSERVE_UPLOAD_TIMEOUT_THRESHOLD = int(os.environ.get('MSERVE_UPLOAD_TIMEOUT_THRESHOLD', 3600))


db = MongoDB.from_cache()


def ingest_uploaded_file(uploader:FileUploader):
    print(f'ingesting: {uploader}', flush=True)

    uploader.status = FileUploadStatus.processing
    db.update(uploader)

    if uploader.type == FileUploadTypes.image:
        obj = ImageFile.from_filepath(uploader.local_storage_path())
    elif uploader.type == FileUploadTypes.audio:
        obj = AudioFile.from_filepath(uploader.local_storage_path())
    elif uploader.type == FileUploadTypes.video:
        obj = VideoFile.from_filepath(uploader.local_storage_path())
    else:
        raise ValueError(f'unknown file upload type: {uploader.type}')
    
    db.create(obj)

    uploader.status = FileUploadStatus.complete
    db.update(uploader)

    print(f'created: {obj}', flush=True)


def ingest_daemon():

    print('begin ingest daemon', flush=True)
    
    controller = DaemonController()

    while controller.run_daemon:
        try:
            for uploader in db.find(FileUploader, filter={'status': FileUploadStatus.process_queue}, size=1):
                ingest_uploaded_file(uploader)

        except Exception as e:
            raise e

        controller.sleep(MSERVE_INGEST_DAEMON_INTERVAL)
        
    print('exiting ingest daemon', flush=True)


def cleanup_process():
    """
    a scheduled process that:
        * looks for uploads with status (error|complete) and modifed date > MSERVE_UPLOAD_CLEANUP_THRESHOLD
            -> deletes file and db entry
        * looks for uploads with status (uploading|processing|pending) and modifed data > TIMEOUT_THRESHOLD 
            -> sets status to error with timeout message and deletes file but keeps db entry
    """

if __name__ == '__main__':
    ingest_daemon()
