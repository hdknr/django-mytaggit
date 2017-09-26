# coding: utf-8
from django.db import models
from mytaggit.models import TaggableManager


class Food(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager()

    def __str__(self):
        return self.name
