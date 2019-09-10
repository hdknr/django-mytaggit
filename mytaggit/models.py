from django.db import models, router
from django.db.models import signals
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify as default_slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.functional import cached_property

from taggit.models import TagBase, GenericTaggedItemBase
from taggit.managers import (
    _TaggableManager as _BaseTaggableManager,
    TaggableManager as BaseTaggableManager,
)
from taggit.utils import require_instance_manager
from markdownx.models import MarkdownxField
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
        Tag, related_name="%(app_label)s_%(class)s_items", 
        on_delete=models.CASCADE)

    value = models.TextField(
        _('Tag Value'), 
        help_text=_('Optional Value for Tag'),
        null=True, blank=True, default=None)

    comment = MarkdownxField(
        _('Tag Comment'), 
        help_text=_('Optional Comment for Tag'),
        null=True, blank=True, default=None)

    users = models.ManyToManyField(
        User, blank=True)

    class Meta:
        verbose_name = _('Tagged Item')
        verbose_name_plural = _('Tagged Items')


class _TaggableManager(_BaseTaggableManager):
    @require_instance_manager
    def add_users(self, tags, users=[]):
        db = router.db_for_write(self.through, instance=self.instance)

        tag_objs = self._to_tag_model_instances(tags)
        new_ids = {t.pk for t in tag_objs}

        # NOTE: can we hardcode 'tag_id' here or should the column name be got
        # dynamically from somewhere?
        vals = (self.through._default_manager.using(db)
                .values_list('tag_id', flat=True)
                .filter(**self._lookup_kwargs()))

        new_ids = new_ids - set(vals)

        signals.m2m_changed.send(
            sender=self.through, action="pre_add",
            instance=self.instance, reverse=False,
            model=self.through.tag_model(), pk_set=new_ids, using=db,
        )

        for tag in tag_objs:
            taggeditem, created = self.through._default_manager.using(db).get_or_create(
                tag=tag, **self._lookup_kwargs())

            if users and hasattr(taggeditem, 'users'):
                taggeditem.users.add(*users)

        signals.m2m_changed.send(
            sender=self.through, action="post_add",
            instance=self.instance, reverse=False,
            model=self.through.tag_model(), pk_set=new_ids, using=db,
        )


class TaggableManager(BaseTaggableManager):

    def __init__(self, verbose_name=_("Tags"),
                 help_text=_("A comma-separated list of tags."),
                 through=None, **kwargs):
        through = through or TaggedItem
        kwargs['manager'] = _TaggableManager
        super(TaggableManager, self).__init__(
            verbose_name=verbose_name, help_text=help_text,
            through=through, **kwargs)
