# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0005_delete_answertagproxy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=wagtail.wagtailcore.fields.RichTextField(help_text='Do not use H2 or H3 to style text. Only use the HTML Editor for troubleshooting. To style tips, warnings and notes, select the content that will go inside the rule lines (so, title + paragraph) and click the Pencil button to style it. Click again to unstyle the tip.', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer_es',
            field=wagtail.wagtailcore.fields.RichTextField(help_text='Do not use H2 or H3 to style text. Only use the HTML Editor for troubleshooting. Also note that tips styling (the Pencil button) does not display on the front end.', verbose_name='Spanish answer', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='audiences',
            field=models.ManyToManyField(help_text='Tag any audiences that may be interested in the answer.', to='ask_cfpb.Audience', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='category',
            field=models.ManyToManyField(help_text='Categorize this answer. Avoid putting into more than one category.', to='ask_cfpb.Category', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='featured',
            field=models.BooleanField(default=False, help_text='Check to make this one of two featured answers on the landing page.'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='next_step',
            field=models.ForeignKey(blank=True, to='ask_cfpb.NextStep', help_text="Formerly known as action items or upsell items.On the web page, these are labeled as 'Explore related resources.'", null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='snippet',
            field=wagtail.wagtailcore.fields.RichTextField(help_text='Optional answer intro, 180-200 characters max. Avoid adding links, images, videos or other rich text elements.', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='snippet_es',
            field=wagtail.wagtailcore.fields.RichTextField(help_text='Do not use this field. It is not currently displayed on the front end.', verbose_name='Spanish snippet', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='statement',
            field=models.TextField(help_text='(Optional) Use this field to rephrase the question title as a statement. Use only if this answer has been chosen to appear on a money topic portal (e.g. /consumer-tools/debt-collection).', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='subcategory',
            field=models.ManyToManyField(help_text='Choose any subcategories related to the answer.', to='ask_cfpb.SubCategory', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='update_english_page',
            field=models.BooleanField(default=False, help_text='Check the box(es) above after you\u2019ve finished making edits to the English or Spanish answer record below. Make sure to check before saving in order to publish your edits or share as a draft.', verbose_name='Send to English page for review'),
        ),
        migrations.AlterField(
            model_name='category',
            name='intro',
            field=wagtail.wagtailcore.fields.RichTextField(help_text='Do not use H2, H3, H4, or H5 to style this text. Do not add links, images, videos or other rich text elements.', blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='intro_es',
            field=wagtail.wagtailcore.fields.RichTextField(help_text='Do not use this field. It is not currently displayed on the front end.', blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='Do not edit this field'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug_es',
            field=models.SlugField(help_text='Do not edit this field'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='description',
            field=wagtail.wagtailcore.fields.RichTextField(help_text='This field is not currently displayed on the front end.', blank=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='description_es',
            field=wagtail.wagtailcore.fields.RichTextField(help_text='This field is not currently displayed on the front end.', blank=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='more_info',
            field=models.TextField(help_text='This field is not currently displayed on the front end.', blank=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='related_subcategories',
            field=models.ManyToManyField(default=None, help_text='Maximum 3 related subcategories', related_name='_subcategory_related_subcategories_+', to='ask_cfpb.SubCategory', blank=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='slug_es',
            field=models.SlugField(help_text='This field is not currently used on the front end.', null=True, blank=True),
        ),
    ]
