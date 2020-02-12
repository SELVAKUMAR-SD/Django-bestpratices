""" Base Model For users """
import uuid
from datetime import datetime
from django.db import models


class BaseModel(models.Model):
    """ Base Model for users """

    __serialized_attributes__ = ()
    __updatable_attributes__ = ()

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now_add=True,
                                      null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def serialize(self):
        return {c: getattr(self, c) for c in self.__serialized_attributes__}

    def update(self, attributes):
        for key, value in attributes.items():
            if key not in self.__updatable_attributes__:
                continue
            setattr(self, key, value)

    def delete(self, **kwargs):
        setattr(self, 'deleted_at', datetime.utcnow())
        self.save()
        super(BaseModel, self).delete(**kwargs)

    def force_delete(self):
        self.delete()

    class Meta:
        abstract = True
