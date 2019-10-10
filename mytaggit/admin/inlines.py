from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.urls import reverse
from django.utils.html import mark_safe
from ..models import TaggedItem
from . import forms
from markdownx.widgets import AdminMarkdownxWidget
from markdownx.models import MarkdownxField



class TaggedItemInline(admin.TabularInline):
    readonly_fields = ['item_link']
    model = TaggedItem
    raw_id_fields = ['users', 'content_type']
    fields = [
        'id', 'item_link',
        'tag',
        'content_type', 'object_id', 
        'value', 'comment',
    ]
    extra = 1
    formfield_overrides = {
        MarkdownxField: {'widget': AdminMarkdownxWidget}
    }

    def item_link(self, obj):
        url = reverse(f"admin:{obj.content_type.app_label}_{obj.content_type.model}_change", args=[obj.object_id])
        return mark_safe(f'<a href="{url}">{obj}</a>')


class GenericTaggedItemInline(GenericTabularInline):
    model = TaggedItem
    raw_id_fields = ['tag', 'users', 'content_type']
    exclude = ['tag', 'value']
    extra = 1
    form = forms.TaggedItemForm
    readonly_fields = ['tag_link']
    formfield_overrides = {
        MarkdownxField: {'widget': AdminMarkdownxWidget}
    }

    def tag_link(self, obj):
        if not obj.tag:
            return ''
        url = reverse(f"admin:{obj.tag._meta.app_label}_{obj.tag._meta.model_name}_change", args=[obj.tag.id])
        return mark_safe(f'<a href="{url}">{obj.tag}</a>')