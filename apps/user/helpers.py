""" User helper functions """
import re

from crud_samples import settings
from utils.auth import get_password_hash, get_jwt
from utils.errors import NotFound, BadRequest
from .models import User, UserRole


def _validate_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if not email:
        raise NotFound('Email Missing')

    if not re.search(regex, email):
        raise BadRequest('Email Format is invalid')


def create_user(payload, password):
    """
    Create user
    :param payload: Dict
    :param password: String
    :return: Obj
    """
    _validate_email(payload.get('email', False))
    password_hash = get_password_hash(password)

    payload['role'] = UserRole.CUSTOMER.value

    user = User(password_hash=password_hash,
                **payload)
    user.save()

    return user


def generate_jwt(user_uuid):
    """
    Generate token dict
    :param user_uuid: UUID - String
    :return: dict(access_token, refresh_token)
    """
    user_uuid = str(user_uuid)

    access_token = get_jwt(user_uuid,
                           settings.JWT_ACCESS_TOKEN_TIME_OUT)
    refresh_token = get_jwt(user_uuid,
                            settings.JWT_REFRESH_TOKEN_TIME_OUT)

    return dict(access_token=access_token,
                refresh_token=refresh_token)


def pagination(page_number, limit, filter_params=None):
    """
    Get pagination objects
    :param page_number: Integer
    :param limit: Integer
    :param filter_params: String
    :return: List of objects
    """
    if page_number and limit and not filter_params:
        objs = User.objects.all() \
            [(int(page_number) - 1) * int(limit):
             int(page_number) * int(limit)]

    elif page_number and limit and filter_params:
        objs = User.objects.filter(first_name__contains=filter_params) \
            [(int(page_number) - 1) * int(limit):
             int(page_number) * int(limit)]

    else:
        objs = User.objects.all()

    return objs
