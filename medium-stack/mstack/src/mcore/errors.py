

class MStackCoreError(Exception):
    pass


class MStackClientError(MStackCoreError):
    def __init__(self, msg, url, exc, response=None) -> None:
        super().__init__(msg)
        self.url = url
        self.exc = exc
        self.response = response
        try:
            self.status_code = response.status_code
        except AttributeError:
            self.status_code = None

class MStackFilePayloadError(MStackCoreError):
    pass


class MStackDBError(MStackCoreError):
    pass


class NotFoundError(MStackCoreError):
    pass
