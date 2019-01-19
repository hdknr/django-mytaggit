# https://github.com/glemmaPaul/django-taggit-serializer/blob/master/taggit_serializer/serializers.py
import json
import six
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import serializers
from . import models
import json


def drf_endpoint(instance):
    ''' DRF endpoint '''
    try:
        if hasattr(instance, 'get_endpoint_url'):
            return hasattr(instance, 'get_endpoint_url')
        name = f"{instance._meta.model_name}-detail"
        return reverse(name, kwargs={'pk': instance.pk})
    except:
        pass
    return ''
    

class TagSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    slug = serializers.CharField(required=False)

    class Meta:
        model = models.Tag
        fields = ['name', 'slug', 'url', 'id']

    def get_url(self, obj):
        try:
            url = obj.get_absolute_url()
            request = self.context.get('request', None)
            return request and request.build_absolute_uri(url) or url
        except:
            return ''

    def is_valid(self, raise_exception=False):
        res = super(TagSerializer, self).is_valid(
            raise_exception=False)
        if not res:
            self._existing = self.Meta.model.objects.filter(
                name=self.initial_data['name']).first()
            res = self._existing and True or False
        return res

    def save(self, **kwargs):
        if hasattr(self, '_existing'):
            self.instance = self._existing
            self._errors = None     # force no errors
            return self.instance
        else:
            return super(TagSerializer, self).save(**kwargs)

    def get_or_create(self, data):
        if isinstance(data, str):
            return self.Meta.model.objects.get_or_create(name=data)[0]
        return self.Meta.model.objects.get_or_create(name=data['name'])[0]


class TagManagerSerializerField(serializers.ListField):
    child = TagSerializer()

    def to_internal_value(self, data):
        request = ('request' in self.context) and self.context['request']
        if request and request.POST:
            data = json.loads(data[0])
        res = [self.child.get_or_create(item) for item in data]
        return res

    def to_representation(self, data):
        if isinstance(data, list):
            return super(TagManagerSerializerField, self).to_representation(data)
        return super(TagManagerSerializerField, self).to_representation(data.all())


class ContentTypeField(serializers.Field):
    SPLITER = '_'

    def to_representation(self, obj):
        return self.SPLITER.join(obj.natural_key())

    def to_internal_value(self, data):
        return ContentType.objects.get_by_natural_key(*data.split(self.SPLITER))


class TaggedItemSerializer(serializers.ModelSerializer):
    content_type = ContentTypeField()
    name = serializers.CharField(source='tag.name')
    slug = serializers.CharField(source='tag.slug')
    url = serializers.SerializerMethodField()
    endpoint = serializers.SerializerMethodField() 

    class Meta:
        model = models.TaggedItem
        fields = ['id', 'content_type', 'object_id', 'url', 'endpoint', 'name', 'slug']

    def get_url(self, obj):
        try:
            url = obj.content_object.get_absolute_url()
            request = self.context.get('request', None)
            return request and request.build_absolute_uri(url) or url
        except:
            return ''

    def get_endpoint(self, obj):
        try:
            url = drf_endpoint(obj.content_object)
            request = self.context.get('request', None)
            return (request and url) and request.build_absolute_uri(url) or url or None
        except:
            pass
        return ''

    def is_valid(self, raise_exception=False):
        self.patch_tag()
        return super(TaggedItemSerializer, self).is_valid(
            raise_exception=raise_exception)

    def patch_tag(self):
        slug = self.initial_data.pop('slug', '')
        name = self.initial_data.pop('name', '')
        if name:
            self._tag, created = models.Tag.objects.get_or_create(name=name)
            self.initial_data['slug'] = self._tag.slug
            self.initial_data['name'] = self._tag.name

    def save(self, **kwargs):
        kwargs['tag']  = self._tag
        instance = self.Meta.model.objects.filter(
            content_type=self.validated_data['content_type'],
            object_id=self.validated_data['object_id'],
            tag=self._tag).first()
        if instance:
            self.instance = instance
        else:
            super(TaggedItemSerializer, self).save(**kwargs)


class TagList(list):
    def __init__(self, *args, **kwargs):
        pretty_print = kwargs.pop("pretty_print", True)
        list.__init__(self, *args, **kwargs)
        self.pretty_print = pretty_print

    def __add__(self, rhs):
        return TagList(list.__add__(self, rhs))

    def __getitem__(self, item):
        result = list.__getitem__(self, item)
        try:
            return TagList(result)
        except TypeError:
            return result

    def __str__(self):
        if self.pretty_print:
            return json.dumps(self, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            return json.dumps(self)


class TagListSerializerField(serializers.Field):
    child = serializers.CharField()
    default_error_messages = {
        'not_a_list': _('Expected a list of items but got type "{input_type}".'),
        'invalid_json': _('Invalid json list. A tag list submitted in string form must be valid json.'),
        'not_a_str': _("All list items must be of string type.")
    }

    def __init__(self, **kwargs):
        pretty_print = kwargs.pop("pretty_print", True)

        style = kwargs.pop("style", {})
        kwargs["style"] = {'base_template': 'textarea.html'}
        kwargs["style"].update(style)

        super(TagListSerializerField, self).__init__(**kwargs)

        self.pretty_print = pretty_print

    def to_internal_value(self, value):
        if isinstance(value, six.string_types):
            if not value:
                value = "[]"
            try:
                value = json.loads(value)
            except ValueError:
                self.fail('invalid_json')

        if not isinstance(value, list):
            self.fail('not_a_list', input_type=type(value).__name__)

        for s in value:
            if not isinstance(s, six.string_types):
                self.fail('not_a_str')

            self.child.run_validation(s)

        return value

    def to_representation(self, value):
        if not isinstance(value, TagList):
            if not isinstance(value, list):
                value = [tag.name for tag in value.all()]
            value = TagList(value, pretty_print=self.pretty_print)

        return value

class TaggitSerializer(serializers.Serializer):
    def create(self, validated_data):
        to_be_tagged, validated_data = self._pop_tags(validated_data)

        tag_object = super(TaggitSerializer, self).create(validated_data)

        return self._save_tags(tag_object, to_be_tagged)

    def update(self, instance, validated_data):
        to_be_tagged, validated_data = self._pop_tags(validated_data)

        tag_object = super(TaggitSerializer, self).update(
            instance, validated_data)

        return self._save_tags(tag_object, to_be_tagged)

    def _save_tags(self, tag_object, tags):
        for key in tags.keys():
            tag_values = tags.get(key)
            getattr(tag_object, key).set(*tag_values)

        return tag_object

    def _pop_tags(self, validated_data):
        to_be_tagged = {}

        for key in self.fields.keys():
            field = self.fields[key]
            if isinstance(field, TagListSerializerField):
                if key in validated_data:
                    to_be_tagged[key] = validated_data.pop(key)

        return (to_be_tagged, validated_data)
