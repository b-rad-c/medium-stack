import os
import sys
import logging

from hashlib import md5
from socket import gethostname

from mcore.models import (
    FileUploader,
    FileUploadTypes,
    FileUploadStatus,
    ImageFile,
    AudioFile,
    VideoFile
)
from mcore.db import MongoDB
from mcore.errors import MStackFilePayloadError
from mcore.util import DaemonController, utc_now



MSERVE_INGEST_DAEMON_INTERVAL = float(os.environ.get('MSERVE_INGEST_DAEMON_INTERVAL', 2.5))
MSERVE_UPLOAD_CLEANUP_THRESHOLD = int(os.environ.get('MSERVE_UPLOAD_CLEANUP_THRESHOLD', 3600))
MSERVE_UPLOAD_TIMEOUT_THRESHOLD = int(os.environ.get('MSERVE_UPLOAD_TIMEOUT_THRESHOLD', 3600))


db = MongoDB.from_cache()

stream_handler = logging.StreamHandler(sys.stdout)

logging.basicConfig(handlers=[stream_handler], level=logging.INFO)


#
# ingest
#


def obtain_lock(uploader:FileUploader) -> FileUploader | None:
    """atttempt to obtain a lock on the file uploader for processing,
    returns the updated file uploader if successful, None if not"""

    logging.info(f'obtaining lock for: {uploader.id}')

    status = FileUploadStatus.process_queue.value

    if uploader.id is None:
        raise ValueError(f'FileUploader must have an id to obtain a lock')
    if uploader.lock is not None:
        raise ValueError(f'FileUploader already has a lock')
    if uploader.status != FileUploadStatus.process_queue:
        raise ValueError(f'FileUploader status must be {status} to obtain a lock')
    
    collection = db.get_collection(uploader)
    
    # create lock name and set on database object
    # this call uses collection.update_one instead of db.update method so that
    # it can filter for the id & status instead of just the id bc there may be a race
    # condition where another process has already changed the status
    lock_name = md5(f'{gethostname()}-{os.getpid()}'.encode()).hexdigest()
    result = collection.update_one({'_id': uploader.id, 'status': status}, {'$set': {'lock': lock_name}})
    if result.modified_count != 1:
        return None

    # query for id & lock_name and attempt to update status,
    # if result modifies 1 document we have obtained lock,
    # if not there was a race condition and another process has the lock
    # this call uses collection.update_one instead of db.update method so that
    # it can filter for the id & lock_name to verify that it obtained the lock
    updates = {'$set': {'status': FileUploadStatus.processing, 'modifed': utc_now()}}
    result = collection.update_one({'_id': uploader.id, 'lock': lock_name, 'status': status}, updates)
    if result.modified_count == 1:
        logging.info(f'lock obtained for: {uploader.id}')
        return db.read(uploader)
    else:
        logging.info(f'could not obtain lock for: {uploader.id}')
        return None


def ingest_uploaded_file(uploader:FileUploader):
    logging.info(f'ingesting: {uploader.id}')

    if uploader.type == FileUploadTypes.image:
        obj = ImageFile.ingest(uploader.local_path(), uploader.user_cid)
    elif uploader.type == FileUploadTypes.audio:
        obj = AudioFile.ingest(uploader.local_path(), uploader.user_cid)
    elif uploader.type == FileUploadTypes.video:
        obj = VideoFile.ingest(uploader.local_path(), uploader.user_cid)
    else:
        raise ValueError(f'unknown file upload type: {uploader.type}')
    
    db.create(obj)

    uploader.status = FileUploadStatus.complete
    db.update(uploader)

    logging.info(f'ingest complete, created: {obj}')


def ingest_daemon():

    logging.info('begin ingest daemon')
    
    controller = DaemonController()

    while controller.run_daemon:
        try:
            for uploader in db.find(FileUploader, filter={'status': FileUploadStatus.process_queue}, size=3):
                locked_uploader = obtain_lock(uploader)
                if locked_uploader is not None:
                    try:
                        ingest_uploaded_file(locked_uploader)
                    except Exception as e:
                        msg = str(e) if isinstance(e, MStackFilePayloadError) else 'Error during ingest process'
                        locked_uploader.error = msg
                        locked_uploader.status = FileUploadStatus.error
                        db.update(locked_uploader)
                        logging.error(f'error ingest file uploader: {locked_uploader.id} - {e}', exc_info=True)

        except Exception as e:
            logging.error(f'error in ingest daemon: {e}', exc_info=True)

        controller.sleep(MSERVE_INGEST_DAEMON_INTERVAL)
        
    logging.info('exiting ingest daemon')


#
# clean up
#

def cleanup_upload(uploader:FileUploader):
    try:
        uploader.local_path().unlink()
    except FileNotFoundError:
        pass
    db.delete(uploader)


def timeout_upload(uploader:FileUploader):
    try:
        uploader.local_path().unlink()
    except FileNotFoundError:
        pass

    uploader.error = 'upload timeout'
    uploader.status = FileUploadStatus.error
    uploader.update_timestamp()
    db.update(uploader)


def cleanup_process():
    """
    a scheduled process that:
        * looks for uploads with status (error|complete) and modifed date > MSERVE_UPLOAD_CLEANUP_THRESHOLD
            -> deletes file and db entry
        * looks for uploads with status (uploading|processing|pending) and modifed data > TIMEOUT_THRESHOLD 
            -> sets status to error with timeout message and deletes file but keeps db entry
    """
    
    logging.info('begin cleanup process')

    #
    # clean up finished and errored uploads
    #

    try:
        query = {
            'status': {'$in': [FileUploadStatus.error, FileUploadStatus.complete]}, 
            'modified': {'$lt': utc_now() - MSERVE_UPLOAD_CLEANUP_THRESHOLD}
        }
        for uploader in db.find(FileUploader, filter=query):
            try:
                cleanup_upload(uploader)
            except Exception as e:
                logging.error(f'error cleaning up file uploader: {uploader.id} - {e}', exc_info=True)
    except Exception as e:
        logging.error(f'error cleaning uploads: {e}', exc_info=True)

    #
    # mark stale uploads as timeout out
    #
        
    try:
        query = {
            'status': {'$in': [FileUploadStatus.uploading, FileUploadStatus.processing, FileUploadStatus.process_queue]},
            'modified': {'$lt': utc_now() - MSERVE_UPLOAD_TIMEOUT_THRESHOLD}
        }
        for uploader in db.find(FileUploader, filter=query):
            uploader.error = 'upload timeout'
            uploader.status = FileUploadStatus.error
            try:
                uploader.local_storage_path().unlink()
            except FileNotFoundError:
                pass
            db.update(uploader)

    except Exception as e:
        logging.error(f'error timing out uploads: {e}', exc_info=True)
        
    logging.info('exiting cleanup process')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['ingest', 'cleanup'])
    args = parser.parse_args()

    match args.command:
        case 'ingest':
            ingest_daemon()
        case 'cleanup':
            cleanup_process()
        case _:
            raise ValueError(f'invalid command: {args.command}')
