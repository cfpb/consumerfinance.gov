from __future__ import absolute_import

from django.db import models

from regulations3k.forms import RegDownField


class RegDownTextField(models.TextField):

    description = "Text rendered with the RegDown extensions to Markdown"

    def formfield(self, **kwargs):
        # Force all RegDownTextFields to use a RegDownField for forms
        defaults = {'form_class': RegDownField}
        defaults.update(kwargs)
        return super(RegDownTextField, self).formfield(**defaults)
