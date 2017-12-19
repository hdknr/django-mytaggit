# coding: utf-8
import rest_framework_filters as filters
from django.db.models import Q
from . import models


class TagFilter(filters.FilterSet):

    is_active = filters.BooleanFilter(method='filter_is_actvie')

    class Meta:
        model = models.Tag
        exclude = []

    def filter_is_actvie(self, queryset, name, value):
        ''' True(value=1), False(value=0)'''
        q = Q(slug='') | Q(name='') | Q(mytaggit_taggeditem_items__isnull=True)
        if value == 1:
            return queryset.exclude(q)
        elif value == 0:
            return queryset.filter(q)
        return queryset



class TaggedItemFilter(filters.FilterSet):

    class Meta:
        model = models.TaggedItem
        exclude = []
