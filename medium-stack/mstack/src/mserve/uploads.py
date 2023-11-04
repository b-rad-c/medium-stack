
DELETE_THRESHOLD = 0
TIMEOUT_THRESHOLD = 0

def ingest_uploaded_file():
    """
    calls ContentModel.from_filepath and inserts result into database
    """


def ingest_daemon():
    """
    infinite loop that quieries for file uploads with status "pending" and calls ingest_uploaded_file
        -> uses multiprocessing pool
    """

def cleanup_process():
    """
    a scheduled process that:
        * looks for uploads with status (error|complete) and modifed date > DELETE_THRESHOLD
            -> deletes file and db entry
        * looks for uploads with status (uploading|processing|pending) and modifed data > TIMEOUT_THRESHOLD 
            -> sets status to error with timeout message and deletes file but keeps db entry
    """
