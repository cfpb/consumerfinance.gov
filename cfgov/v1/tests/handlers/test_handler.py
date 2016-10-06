import mock
from unittest import TestCase
from v1.handlers import Handler


class TestHandler(TestCase):
    def setUp(self):
        self.page = mock.Mock()
        self.request = mock.Mock()
        self.context = {}
        self.handler = Handler(self.page, self.request, self.context)

    def test_process_raises_NotImplementedError(self):
        with self.assertRaises(NotImplementedError) as nie:
            self.handler.process()
