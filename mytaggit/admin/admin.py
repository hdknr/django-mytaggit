from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from ..models import Tag
from . import inlines


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [inlines.TaggedItemInline]
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}