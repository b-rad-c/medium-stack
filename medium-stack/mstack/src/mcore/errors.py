class MediumCoreError(Exception):
    pass


class MediumFilePayloadError(MediumCoreError):
    pass


class MediumDBError(MediumCoreError):
    pass


class NotFoundError(MediumCoreError):
    pass
