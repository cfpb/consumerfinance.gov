# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailadmin.taggable
import wagtail.wagtailimages.models
import django.db.models.deletion
from django.conf import settings
import taggit.managers


def migrate_images_data(apps, schema_editor):
    CFGOVImageModel = apps.get_model('v1.CFGOVImage')
    UserModel = apps.get_model(settings.AUTH_USER_MODEL)

    # Migrate image data
    for image in wagtail.wagtailimages.models.Image.objects.all():
        new_image = CFGOVImageModel()
        for field in ['title', 'file', 'width', 'height', 'focal_point_x',
                      'focal_point_y', 'focal_point_width',
                      'focal_point_height', 'file_size', 'tags']:
            value = getattr(image, field)
            setattr(new_image, field, value)
        user = UserModel.objects.get(id=image.uploaded_by_user.id)
        new_image.uploaded_by_user = user
        new_image.save()


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailimages', '0010_change_on_delete_behaviour'),
        ('v1', '0030_documentdetailpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CFGOVImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('file', models.ImageField(height_field='height', upload_to=wagtail.wagtailimages.models.get_upload_to, width_field='width', verbose_name='file')),
                ('width', models.IntegerField(verbose_name='width', editable=False)),
                ('height', models.IntegerField(verbose_name='height', editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at', db_index=True)),
                ('focal_point_x', models.PositiveIntegerField(null=True, blank=True)),
                ('focal_point_y', models.PositiveIntegerField(null=True, blank=True)),
                ('focal_point_width', models.PositiveIntegerField(null=True, blank=True)),
                ('focal_point_height', models.PositiveIntegerField(null=True, blank=True)),
                ('file_size', models.PositiveIntegerField(null=True, editable=False)),
                ('alt', models.CharField(max_length=100, blank=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text=None, verbose_name='tags')),
                ('uploaded_by_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='uploaded by user')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, wagtail.wagtailadmin.taggable.TagSearchable),
        ),
        migrations.CreateModel(
            name='CFGOVRendition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.ImageField(height_field='height', width_field='width', upload_to='images')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('focal_point_key', models.CharField(default='', max_length=255, editable=False, blank=True)),
                ('filter', models.ForeignKey(related_name='+', to='wagtailimages.Filter')),
                ('image', models.ForeignKey(related_name='renditions', to='v1.CFGOVImage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(migrate_images_data),
    ]
