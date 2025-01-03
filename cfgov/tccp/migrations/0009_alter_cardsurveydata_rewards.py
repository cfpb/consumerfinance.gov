# Generated by Django 3.2.24 on 2024-03-25 19:23

from django.db import migrations
import tccp.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tccp', '0008_state_names'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardsurveydata',
            name='rewards',
            field=tccp.fields.JSONListField(blank=True, choices=[('Cashback rewards', 'Cash back'), ('Travel-related rewards', 'Travel'), ('Other rewards', 'Other')], default=list),
        ),
    ]
