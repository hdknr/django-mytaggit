from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
import rest_framework_filters as filters
from . import models


class TagFilter(filters.FilterSet):
    keyword = filters.CharFilter(
        label=_('Keyword'), name='keyword', method='filter_keyword')
    is_active = filters.BooleanFilter(
        label=_('Is Active'), name='is_active', method='filter_is_actvie')

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

    def filter_keyword(self, queryset, name, value):
        q = Q(slug='') | Q(name='') | Q(mytaggit_taggeditem_items__isnull=True)
        return value and queryset.filter(
            Q(name__icontains=value) | Q(slug__icontains=value)) or queryset


class TaggedItemFilter(filters.FilterSet):

    class Meta:
        model = models.TaggedItem
        exclude = []
