""" Auth Function """
import crypt
import datetime
import jwt

from apps.user.models import User
from django.core.exceptions import ObjectDoesNotExist

from crud_samples import settings
from utils.errors import (NotFound,
                          PermissionDenied,
                          AuthenticationFailed,
                          InvalidSignatureError)


def get_password_hash(password):
    """
    Get hashed password
    :param password: String
    :return: Hashed password
    """
    return crypt.crypt(password)


def check_password(password, user):
    """
    Check given password is correct
    :param password: String
    :param user: object
    :return: Exception if Error
    """
    if not crypt.crypt(password, user.password_hash) == \
           user.password_hash:
        raise PermissionDenied('Password incorrect')


def get_jwt(identity, exp_time):
    """
    Generate JWT
    :param identity: UUId - String
    :param exp_time: time_stamp
    :return: JWT token
    """
    payload = dict(identity=identity, exp=get_auth_exp(exp_time))
    return jwt.encode(payload,
                      settings.SECRET_KEY).decode('utf-8')


def get_auth_exp(timeout_in_minutes):
    """
    Generating expiry timestamp
    :param timeout_in_minutes: Integer
    :return: timestamp value
    """
    _timestamp = datetime.datetime.utcnow() + datetime. \
        timedelta(minutes=timeout_in_minutes)
    return _timestamp


def get_jwt_user(token):
    """
    Validating token and user
    :param token: JWT - String
    :return: Exception if error
    """

    if not token:
        raise NotFound('Token Missing')

    try:
        payload = jwt.decode(token,
                             settings.SECRET_KEY)
    except jwt.InvalidSignatureError as err:
        raise InvalidSignatureError(str(err))
    except jwt.ExpiredSignature \
           or jwt.DecodeError \
           or jwt.InvalidTokenError as err:
        raise AuthenticationFailed(str(err))

    try:
        obj = User.objects.get(uuid=payload['identity'])
    except ObjectDoesNotExist:
        raise AuthenticationFailed('Invalid Credentials')

    return obj
