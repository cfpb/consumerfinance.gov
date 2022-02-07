from unittest import TestCase, mock

from ...handlers import Handler


class TestHandler(TestCase):
    def setUp(self):
        self.page = mock.Mock()
        self.request = mock.Mock()
        self.context = {}
        self.handler = Handler(self.page, self.request, self.context)

    def test_process_raises_NotImplementedError(self):
        with self.assertRaises(NotImplementedError):
            self.handler.process()
