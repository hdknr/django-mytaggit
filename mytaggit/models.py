# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from taggit.models import TagBase, GenericTaggedItemBase
from taggit.managers import TaggableManager as BaseTaggableManager
from . import methods


class Tag(TagBase, methods.Tag):

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def slugify(self, tag, i=None):
        tag = self.to_roman(tag)
        return super(Tag, self).slugify(tag, i=i)


class TaggedItem(GenericTaggedItemBase):

    tag = models.ForeignKey(
        Tag, related_name="%(app_label)s_%(class)s_items")


class TaggableManager(BaseTaggableManager):

    def __init__(self, verbose_name=_("Tags"),
                 help_text=_("A comma-separated list of tags."),
                 through=None, **kwargs):
        through = through or TaggedItem
        super(TaggableManager, self).__init__(
            verbose_name=verbose_name, help_text=help_text,
            through=through, **kwargs)
