# Generated by Django 3.0.6 on 2020-06-08 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('mytaggit', '0007_auto_20200601_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='taggeditem',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mytaggit_taggeditem_tagged_items', to='contenttypes.ContentType', verbose_name='Content type'),
        ),
        migrations.AlterField(
            model_name='taggeditem',
            name='object_id',
            field=models.IntegerField(db_index=True, verbose_name='Object id'),
        ),
    ]