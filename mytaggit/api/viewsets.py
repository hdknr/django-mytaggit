from collections import OrderedDict
from rest_framework import viewsets, pagination, permissions
from rest_framework.response import Response
from . import serializers, filters
from .. import models


class Pagination(pagination.PageNumberPagination):
    page_size = 16
    max_page_size = 16
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_range', list(self.page.paginator.page_range)),
            ('current_page', self.page.number),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class TagViewSet(viewsets.ModelViewSet):

    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    filter_class = filters.TagFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = Pagination


class TaggedItemViewSet(viewsets.ModelViewSet):

    queryset = models.TaggedItem.objects.all()
    serializer_class = serializers.TaggedItemSerializer
    filter_class = filters.TaggedItemFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = Pagination
