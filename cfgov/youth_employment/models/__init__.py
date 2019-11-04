from __future__ import unicode_literals

import json

from wagtail.wagtailcore.models import PageManager

from youth_employment.blocks import YESChecklist

from v1.models import BrowsePage


class YESCarBuyingGuide(BrowsePage):
  objects = PageManager()
  
  template = 'youth-employment/index.html'

  #yes_checklist = YESChecklist()

  def get_context(self, request, *args, **kwargs):
    context = super(BrowsePage, self).get_context(request, *args, **kwargs)
    context.update({
      'expandables_content': json.dumps(self.content.stream_data),
    })
    return context

