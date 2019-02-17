# coding: utf-8
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register(r'tag', viewsets.TagViewSet, base_name='tag')
router.register(r'taggeditem', viewsets.TaggedItemViewSet, base_name='taggeditem')

urlpatterns = [
    url(r'^', include(router.urls)),
]
