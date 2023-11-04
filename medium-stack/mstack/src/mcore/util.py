import datetime


__all__ = [
    'utc_now'
]


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc)
