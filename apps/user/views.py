""" User API """

from rest_framework.decorators import api_view

from utils.auth import check_password
from utils.json_response import JSONResponse
from utils.utils import (is_authorized_role,
                         require_json,
                         validate_payload_fields,
                         allowed_query_params)
from .helpers import create_user, generate_jwt, pagination
from .models import User, UserRole


@api_view(['POST'])
@require_json
@validate_payload_fields([('email', 'Email missing'),
                          ('password', 'Password missing'),
                          ('phone_no', 'Phone number missing')])
def signup(payload):
    """
    User signup
    :param payload: Dict
    :return: User object
    """
    password = payload.pop('password', False)
    result = create_user(payload, password)
    return JSONResponse(result, status=201)


@api_view(['POST'])
@require_json
def login(payload):
    """
    User login
    :param payload: Dict
    :return: Access Token and Refresh Token
    """
    email = payload.get('email', None)
    password = payload.get('password', None)

    user = User.find_by_email(email)
    check_password(password, user)
    return JSONResponse({**generate_jwt(user.uuid),
                         "user": user})


@api_view(['GET'])
@is_authorized_role((UserRole.CUSTOMER,))
def details(request):
    """
    Get user details
    :param request: Request
    :return: user object
    """
    return JSONResponse(request.user_obj, json_key='user')


@api_view(['GET'])
@allowed_query_params(['first_name'])
def user_list(request, params):
    """
    Get all user with pagination
    :return: list of user objects
    """
    page = request.GET.get('page', None)
    limit = request.GET.get('limit', None)

    return JSONResponse(pagination(page, limit, params),
                        json_key='users')
