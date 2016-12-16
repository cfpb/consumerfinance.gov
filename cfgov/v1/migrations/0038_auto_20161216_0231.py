# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from wagtail.wagtailimages.utils import get_fill_filter_spec_migrations

class Migration(migrations.Migration):

	dependencies = [
		('v1', '0037_auto_20161216_0231'),
	]

	forward, reverse = get_fill_filter_spec_migrations('v1', 'CFGOVRendition')
	operations = [
		migrations.RunPython(forward, reverse),
	]