# coding: utf-8

from django.contrib import admin
from .models import Tag, TaggedItem


class TaggedItemInline(admin.TabularInline):
    model = TaggedItem
    raw_id_fields = ['users', 'content_type']
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}
