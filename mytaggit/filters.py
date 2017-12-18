# coding: utf-8
import rest_framework_filters as filters
from . import models


class TagFilter(filters.FilterSet):

    class Meta:
        model = models.Tag
        exclude = []


class TaggedItemFilter(filters.FilterSet):

    class Meta:
        model = models.TaggedItem
        exclude = []
