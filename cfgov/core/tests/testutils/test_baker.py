from unittest import TestCase

from django.contrib.contenttypes.models import ContentType

from core.testutils.baker import ActualContentTypeBaker
from v1.models import CFGOVPage


class ActualContentTypeBakerTestCase(TestCase):
    def test_type_mapping(self):
        cfgovpage_baker = ActualContentTypeBaker(CFGOVPage)
        content_type = cfgovpage_baker.type_mapping[ContentType]()
        self.assertEqual("v1", content_type.app_label)
        self.assertEqual("cfgovpage", content_type.model)
