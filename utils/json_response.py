""" Customizing JSON Response """
from django.http import JsonResponse

from .encoder import JSONEncoder


class JSONResponse(JsonResponse):
    """ Customized Response """

    def __init__(self, data, json_key=None, encoder=JSONEncoder,
                 **kwargs):
        kwargs['safe'] = False
        if json_key:
            super().__init__({json_key: data}, encoder, **kwargs)
        else:
            super().__init__(data, encoder, **kwargs)
