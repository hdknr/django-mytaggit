from django.conf.urls import url, include
from . import views, api

urlpatterns = [
    url(r'^api/', include(api)),
]
