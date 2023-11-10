import os
import time
from mcore.util import DaemonController



MSERVE_INGEST_DAEMON_INTERVAL = float(os.environ.get('MSERVE_INGEST_DAEMON_INTERVAL', 5.0))
MSERVE_UPLOAD_CLEANUP_THRESHOLD = int(os.environ.get('MSERVE_UPLOAD_CLEANUP_THRESHOLD'), 3600)
MSERVE_UPLOAD_TIMEOUT_THRESHOLD = int(os.environ.get('MSERVE_UPLOAD_TIMEOUT_THRESHOLD'), 3600)



def ingest_uploaded_file():
    """
    calls ContentModel.from_filepath and inserts result into database
    """

def ingest_loop():
    pass


def ingest_daemon():
    """
    infinite loop that quieries for file uploads with status "pending" and calls ingest_uploaded_file
        -> uses multiprocessing pool
    """
    controller = DaemonController()

    while controller.run_daemon:

        ingest_loop()

        controller.sleep(MSERVE_INGEST_DAEMON_INTERVAL)
        
    print('exiting ingest daemon')


def cleanup_process():
    """
    a scheduled process that:
        * looks for uploads with status (error|complete) and modifed date > MSERVE_UPLOAD_CLEANUP_THRESHOLD
            -> deletes file and db entry
        * looks for uploads with status (uploading|processing|pending) and modifed data > TIMEOUT_THRESHOLD 
            -> sets status to error with timeout message and deletes file but keeps db entry
    """
