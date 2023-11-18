import datetime
import signal
import time

from mcore.types import ContentId

from pydantic import BaseModel

__all__ = [
    'example_model',
    'example_cid',
    'utc_now',
    'DaemonController'
]


def example_model(model_type:BaseModel, index=0):
    try:
        example = model_type.model_json_schema()['examples'][index]
    except KeyError:
        raise AssertionError(f'model {model_type.__class__.__name__} does not have examples defined')
    except IndexError:
        raise AssertionError(f'model {model_type.__class__.__name__} does not define example at index: {index}')
    
    return model_type(**example)

def example_cid(model_type:BaseModel, index=0):
    try:
        example = model_type.model_json_schema()['examples'][index]
    except KeyError:
        raise AssertionError(f'model {model_type.__class__.__name__} does not have examples defined')
    except IndexError:
        raise AssertionError(f'model {model_type.__class__.__name__} does not define example at index: {index}')
    
    try:
        cid = example['cid']
    except KeyError:
        raise AssertionError(f'model {model_type.__class__.__name__} does not define a cid in the example at index: {index}')
    
    return ContentId.parse(cid)

def utc_now():
    """mongodb returns timezone unaware objects with less precision that datetime,
    this hack creates utc timestamps that will be the same before and after mongo
    ensure that pydantic models can be compared for equality
    """
    date = datetime.datetime.now(datetime.timezone.utc)
    micro = str(date.microsecond)
    return date.replace(microsecond=int(micro[0:3] + '000'), tzinfo=None)

class DaemonController:

    def __init__(self):
        self.run_daemon = True
        signal.signal(signal.SIGTERM, self.handle_sigterm)

    def handle_sigterm(self, signum, frame):
        print(f"Caught signal {signum}...")
        self.run_daemon = False

    def sleep(self, duration:float, sleep_interval:float = 0.1):
        end_time = time.time() + duration
        while time.time() < end_time and self.run_daemon:
            time.sleep(sleep_interval)