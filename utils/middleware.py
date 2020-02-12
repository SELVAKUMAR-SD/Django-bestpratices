""" Middleware """
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from crud_samples.settings import ALLOWED_URLS
from utils.auth import get_jwt_user
from utils.errors import NotFound


class AuthenticationMiddlewareJWT(MiddlewareMixin):
    """
    Middleware class for decode the given JWT
    and append the user obj with request and handle the
    URL path which need JWT
    """

    def process_request(self, request):
        """ Processing the request """
        path = request.get_full_path()
        if any(word in path for word in ALLOWED_URLS):
            return

        token = request.META.get('HTTP_AUTHORIZATION', None)

        request.user_obj = SimpleLazyObject(lambda: get_jwt_user(token))
        return
