# Generated by Django 2.1 on 2018-10-09 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytaggit', '0003_taggeditem_value'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taggeditem',
            options={'verbose_name': 'Tagged Item', 'verbose_name_plural': 'Tagged Items'},
        ),
        migrations.AlterField(
            model_name='taggeditem',
            name='value',
            field=models.TextField(blank=True, default=None, help_text='Optional Value for Tag', null=True, verbose_name='Tag Value'),
        ),
    ]
