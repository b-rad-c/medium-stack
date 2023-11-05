import os
import time
import signal


MSERVE_INGEST_DAEMON_INTERVAL = float(os.environ.get('MSERVE_INGEST_DAEMON_INTERVAL', 5.0))
MSERVE_UPLOAD_CLEANUP_THRESHOLD = int(os.environ.get('MSERVE_UPLOAD_CLEANUP_THRESHOLD'), 3600)
MSERVE_UPLOAD_TIMEOUT_THRESHOLD = int(os.environ.get('MSERVE_UPLOAD_TIMEOUT_THRESHOLD'), 3600)

RUN_DAEMON = True

def handle_sigterm(signum, _):
    global RUN_DAEMON
    print(f"Caught signal {signum}...")
    RUN_DAEMON = False

signal.signal(signal.SIGTERM, handle_sigterm)


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
    while RUN_DAEMON:
        time.sleep(MSERVE_INGEST_DAEMON_INTERVAL)

        if not RUN_DAEMON:
            break

        ingest_loop()
        
    print('exiting ingest daemon')


def cleanup_process():
    """
    a scheduled process that:
        * looks for uploads with status (error|complete) and modifed date > MSERVE_UPLOAD_CLEANUP_THRESHOLD
            -> deletes file and db entry
        * looks for uploads with status (uploading|processing|pending) and modifed data > TIMEOUT_THRESHOLD 
            -> sets status to error with timeout message and deletes file but keeps db entry
    """
