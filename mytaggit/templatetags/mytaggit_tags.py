from django import template
from mytaggit.models import Tag

register = template.Library()

@register.simple_tag
def tag(slug=None, name=None):
    q = {'slug': slug} if slug else {'name': name}
    return Tag.objects.filter(**q).first()


@register.filter
def for_content(tag, natural_key):
    q = dict(
        i for i in
        zip(('content_type__app_label', 'content_type__model'),
            natural_key.split('.'))
    )
    return tag.mytaggit_taggeditem_items.filter(**q)
