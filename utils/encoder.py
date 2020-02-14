""" DjangoEncoder """
import enum

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet

from apps.user.models import BaseModel
from utils.errors import APIError


class JSONEncoder(DjangoJSONEncoder):
    """ Customized JSON Encoder """

    def default(self, o):
        """ Encoding an obj to JSON """
        if isinstance(o, enum.Enum):
            return o.value

        if isinstance(o, APIError):
            return o.detail

        if isinstance(o, QuerySet):
            return list(o)

        if isinstance(o, BaseModel):
            return o.serialize()

        return super().default(o)
