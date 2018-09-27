from django import forms
from django.utils.translation import ugettext_lazy as _
from ..models import TaggedItem, Tag


class TaggedItemForm(forms.ModelForm):
    tag_name = forms.CharField(
        label=_('Tag Name'), required=True)
    tag_value = forms.CharField(
        label=_('Tag Value'), 
        help_text=_('Tag Value Help'), 
        required=False, 
        widget=forms.Textarea(attrs={'rows':2, 'cols':50})) 

    class Meta:
        model = TaggedItem
        exclude = ['value']

    def __init__(self, instance=None, *args, **kwargs):
        if instance:
            kwargs['initial'] = {
                'tag_name': instance.tag.name, 'tag_value': instance.value}
        super().__init__(instance=instance, *args, **kwargs)
        if 'tag' in self.fields:
            self.fields['tag'].required = False

    def save(self, *args, **kwargs):
        self.instance.tag, created = Tag.objects.get_or_create(
            name=self.cleaned_data['tag_name'])
        self.instance.value = self.cleaned_data.get('tag_value', None)
        return super().save(*args, **kwargs)