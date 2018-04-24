from __future__ import unicode_literals

from django.test import TestCase

from regulations3k.models import EffectiveVersion, Part, Section, Subpart
from regulations3k.wagtail_hooks import (
    EffectiveVersionModelAdmin, PartModelAdmin, SectionModelAdmin,
    SubpartModelAdmin
)


class TestRegs3kHooks(TestCase):

    def test_reg_model_hooks(self):
        self.assertEqual(PartModelAdmin.model, Part)
        self.assertEqual(SubpartModelAdmin.model, Subpart)
        self.assertEqual(SectionModelAdmin.model, Section)
        self.assertEqual(EffectiveVersionModelAdmin.model, EffectiveVersion)
