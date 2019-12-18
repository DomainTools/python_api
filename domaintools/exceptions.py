"""Defines the Exceptions that can be raised from the DomainTools API"""


class ServiceException(Exception):

    def __init__(self, code, reason):
        self.code = code
        self.reason = reason
        super(ServiceException, self).__init__(str(reason))


class BadRequestException(ServiceException):
    pass


class InternalServerErrorException(ServiceException):
    pass


class NotAuthorizedException(ServiceException):
    pass


class NotFoundException(ServiceException):
    pass


class ServiceUnavailableException(ServiceException):
    pass


class IncompleteResponseException(ServiceException):
    pass

class RequestUriTooLongException(ServiceException):
    pass
