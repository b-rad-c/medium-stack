import datetime


__all__ = [
    'utc_now'
]


def utc_now():
    """mongodb returns timezone unaware objects with less precision that datetime,
    this hack creates utc timestamps that will be the same before and after mongo
    ensure that pydantic models can be compared for equality
    """
    date = datetime.datetime.now(datetime.timezone.utc)
    micro = str(date.microsecond)
    return date.replace(microsecond=int(micro[0:3] + '000'), tzinfo=None)
