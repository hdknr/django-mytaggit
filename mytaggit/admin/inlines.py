from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from ..models import TaggedItem
from . import forms


class TaggedItemInline(admin.TabularInline):
    model = TaggedItem
    raw_id_fields = ['users', 'content_type']
    extra = 1


class GenericTaggedItemInline(GenericTabularInline):
    model = TaggedItem
    raw_id_fields = ['tag', 'users', 'content_type']
    exclude = ['tag', 'value']
    extra = 1
    form = forms.TaggedItemForm