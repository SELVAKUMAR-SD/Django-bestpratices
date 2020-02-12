""" Exception """
from rest_framework.exceptions import APIException
from rest_framework import status

from utils.error_handler import get_error_details


class APIError(APIException):
    """ Customized Exception Handler """

    def __init__(self, detail):
        super(APIError, self).__init__(detail, self.__class__.__name__)
        self.detail = get_error_details(detail, self.__class__.__name__)


class NotFound(APIError):
    """ Not Found Error class """
    status_code = status.HTTP_404_NOT_FOUND


class AuthenticationFailed(APIError):
    """ UnAuthorized Error """
    status_code = status.HTTP_401_UNAUTHORIZED


class PermissionDenied(APIError):
    """ Permission Denied """
    status_code = status.HTTP_403_FORBIDDEN


class MethodNotAllowed(APIError):
    """ Unsupported Method """
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED


class UnsupportedMediaType(APIError):
    """ UnSupported Media """
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


class BadRequest(APIError):
    """ Invalid Request """
    status_code = status.HTTP_400_BAD_REQUEST


class ExpiredSignature(APIError):
    """ Expired Token"""


class DecodeError(APIError):
    """ Decoder Error """


class InvalidKeyError(APIError):
    """ Invalid Key """


class InvalidSignatureError(APIError):
    """ Invalid Signature """
