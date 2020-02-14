""" common functions for project """
import json
from functools import wraps

from apps.user.models import UserRole
from utils.errors import (BadRequest,
                          PermissionDenied,
                          AuthenticationFailed)


def no_content_response():
    """
    Common response for delete API
    :return: HTTP response
    """
    return '', 204, {'content-type': 'application/json'}


def is_authorized_role(roles):
    def decorator(function):
        @wraps(function)
        def wrap(request, *args, **kwargs):
            if not request.user_obj:
                raise AuthenticationFailed('User not found')
            user = request.user_obj
            if UserRole(user.role) not in roles:
                raise PermissionDenied('''User doesn't have
                 sufficient permissions to perform this operation''')

            return function(request, *args, **kwargs)

        return wrap

    return decorator


def require_json(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        payload = json.loads(request.body)
        if not payload:
            raise BadRequest('Json Missing')
        return function(payload, *args, **kwargs)

    return decorator


def validate_payload_fields(fields):
    def decorator(function):
        @wraps(function)
        def validate(payload, *args, **kwargs):
            for key, err_msg in fields:
                if not payload.get(key):
                    raise BadRequest(err_msg)
            return function(payload, *args, **kwargs)

        return validate

    return decorator


def allowed_params(func):
    @wraps(func)
    def decorator(request, *args, **kwargs):
        filter_param = request.GET.get('password', None)
        if filter_param:
            if filter_param not in request.user_obj.__serialized_attributes__:
                raise BadRequest('{msg} not allowed'.format(msg=filter_param))
        return func(request, *args, **kwargs)

    return decorator
