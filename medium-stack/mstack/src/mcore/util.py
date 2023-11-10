import datetime
import signal
import time


__all__ = [
    'utc_now',
    'DaemonController'
]


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