# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from wagtail.wagtailimages.utils import get_fill_filter_spec_migrations

class Migration(migrations.Migration):

	dependencies = [
		('v1', '0039_add_filter_spec_to_cfgovrendition'),
	]

	forward, reverse = get_fill_filter_spec_migrations('v1', 'CFGOVRendition')
	operations = [
		migrations.RunPython(forward, reverse),
	]