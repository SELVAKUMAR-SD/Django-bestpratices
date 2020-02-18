""" User Related Model """
import enum
import random
import string

from django.db import models

from .base_model import BaseModel


class UserRole(enum.Enum):
    """ User Role enum """
    ADMIN = 'ADMIN'
    VENDOR = 'VENDOR'
    CUSTOMER = 'CUSTOMER'


class User(BaseModel):
    """ User Model """
    __serialized_attributes__ = ('uuid', 'first_name', 'last_name',
                                 'email', 'phone_no', 'role',
                                 'referral_code', 'referral', 'score')
    __updatable_attributes__ = ('first_name', 'last_name', 'email',
                                'role', 'phone_no', 'referral_code',
                                'referral', 'score')

    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=256)
    password_hash = models.CharField(max_length=256)
    phone_no = models.CharField(max_length=12)
    role = models.CharField(max_length=25)
    score = models.FloatField(default=0)
    referral_code = models.CharField(max_length=15, unique=True,
                                     null=True)
    referral = models.ForeignKey('self', on_delete=models.CASCADE,
                                 null=True)

    @property
    def name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @classmethod
    def find_by_email(cls, email):
        """
        Get the customer object by email
        :param email: String
        :return: User object
        """
        return cls.objects.get(email=email)

    @classmethod
    def get_count(cls):
        """
        Get count of user
        :return: Integer
        """
        pass

    @staticmethod
    def generate_referral(size=8, chars=string.ascii_uppercase +
                                        string.digits):
        return ''.join(random.choice(chars) for n in range(size))

    class Meta:
        db_table = 'users'
        unique_together = ['email', 'phone_no']
