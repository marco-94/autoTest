"""
封装通用的model
"""
from django.db import models
import time
import random


class BaseModel(models.Model):
    updated_tm = models.DateTimeField(auto_now=True)
    created_tm = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
