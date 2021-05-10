# -*- coding: utf-8 -*-
import django

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgeChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('age', models.IntegerField()),
                ('aside', models.CharField(max_length=500)),
            ],
            options={
                'ordering': ['age'],
            },
        ),
        migrations.CreateModel(
            name='Calibration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('results_json', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('h1', models.CharField(max_length=255, blank=True)),
                ('intro', models.TextField(max_length=255)),
                ('h2', models.CharField(max_length=255, blank=True)),
                ('h3', models.CharField(max_length=255, blank=True)),
                ('h4', models.CharField(max_length=255, blank=True)),
                ('final_steps', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('slug', models.SlugField(blank=True)),
                ('question', models.TextField(blank=True)),
                ('answer_yes_a_subhed', models.CharField(help_text='Under 50', max_length=255, blank=True)),
                ('answer_yes_a', models.TextField(help_text='Under 50', blank=True)),
                ('answer_yes_b_subhed', models.CharField(help_text='50 and older', max_length=255, blank=True)),
                ('answer_yes_b', models.TextField(help_text='50 and older', blank=True)),
                ('answer_no_a_subhed', models.CharField(help_text='Under 50', max_length=255, blank=True)),
                ('answer_no_a', models.TextField(help_text='Under 50', blank=True)),
                ('answer_no_b_subhed', models.CharField(help_text='50 and older', max_length=255, blank=True)),
                ('answer_no_b', models.TextField(help_text='50 and older', blank=True)),
                ('answer_unsure_a_subhed', models.CharField(help_text='Under 50', max_length=255, blank=True)),
                ('answer_unsure_a', models.TextField(help_text='Under 50', blank=True)),
                ('answer_unsure_b_subhed', models.CharField(help_text='50 and older', max_length=255, blank=True)),
                ('answer_unsure_b', models.TextField(help_text='50 and older', blank=True)),
                ('workflow_state', models.CharField(default='SUBMITTED', max_length=255, choices=[('APPROVED', 'Approved'), ('REVISED', 'Revised'), ('SUBMITTED', 'Submitted')])),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('instructions', models.TextField(max_length=255, blank=True)),
                ('note', models.TextField(max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tooltip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('text', models.TextField(max_length=255, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='step1',
            field=models.ForeignKey(related_name='step1', blank=True, to='retirement_api.Step', null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='page',
            name='step2',
            field=models.ForeignKey(related_name='step2', blank=True, to='retirement_api.Step', null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='page',
            name='step3',
            field=models.ForeignKey(related_name='step3', blank=True, to='retirement_api.Step', null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
    ]
