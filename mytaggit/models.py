from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify as default_slugify
from django.core.urlresolvers import reverse
from django.utils.functional import cached_property
from taggit.models import TagBase, GenericTaggedItemBase
from taggit.managers import TaggableManager as BaseTaggableManager
from . import methods


class Tag(TagBase, methods.Tag):

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def slugify(self, tag, i=None):
        tag = self.to_roman(tag)
        slug = default_slugify(tag)
        if i is not None:
            slug += "-%d" % i
        return slug

    def get_absolute_url(self):
        name = getattr(settings, 'MYTAGGIT_URL', None)
        return name and reverse(name, kwargs={'slug': self.slug}) or ''

    @cached_property
    def is_active(self):
        return self.slug and self.name and self.mytaggit_taggeditem_items.count() > 0


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
