class MobileConverter:
    regex = '1[3-9]\d{9}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)


class UsernameConverter:
    regex = '[a-zA-Z0-9_-]{5,20}'

    def to_python(self, value):
        return value
    #
    # def to_url(self, value):
    #     return value

from django.urls import converters
class UUIDConverter:
    regex = '[\w-]+'
    def to_python(self, value):
        return str(value)
    # def to_url(self, value):
    #     return str(value)
from django.db import models
class BaseModel(models.Model):
    create_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time=models.DateTimeField(auto_now=True,verbose_name='跟新时间')
    class Meta:
        abstract = True