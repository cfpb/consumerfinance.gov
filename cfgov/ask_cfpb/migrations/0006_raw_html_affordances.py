# Generated by Django 3.2.24 on 2024-03-05 19:48

from django.db import migrations
import v1.blocks
import v1.models.snippets
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0005_add_table_intro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answerpage',
            name='notification',
            field=wagtail.fields.StreamField([('notification', wagtail.blocks.StructBlock([('type', wagtail.blocks.ChoiceBlock(choices=[('information', 'Information'), ('warning', 'Warning')])), ('message', wagtail.blocks.CharBlock(help_text='The main notification message to display.', required=True)), ('explanation', wagtail.blocks.TextBlock(help_text='Explanation text appears below the message in smaller type.', required=False)), ('links', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(required=False)), ('aria_label', wagtail.blocks.CharBlock(help_text='Add an ARIA label if the link text does not describe the destination of the link (e.g. has ambiguous text like "Learn more" that is not descriptive on its own).', required=False)), ('url', wagtail.blocks.CharBlock(default='/', required=False)), ('is_link_boldface', wagtail.blocks.BooleanBlock(default=False, required=False))]), help_text='Links appear on their own lines below the explanation.', required=False))]))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='answerpage',
            name='sidebar',
            field=wagtail.fields.StreamField([('related_links', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('paragraph', wagtail.blocks.RichTextBlock(required=False)), ('links', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(required=False)), ('aria_label', wagtail.blocks.CharBlock(help_text='Add an ARIA label if the link text does not describe the destination of the link (e.g. has ambiguous text like "Learn more" that is not descriptive on its own).', required=False)), ('url', wagtail.blocks.CharBlock(default='/', required=False)), ('is_link_boldface', wagtail.blocks.BooleanBlock(default=False, required=False))])))])), ('email_signup', v1.blocks.EmailSignUpChooserBlock()), ('reusable_text', v1.blocks.ReusableTextChooserBlock(v1.models.snippets.ReusableText))], blank=True, use_json_field=True),
        ),
    ]
