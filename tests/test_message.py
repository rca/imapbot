import os

from unittest import TestCase

from imapbot.message import Message

from tests.helpers import SAMPLE_ENVELOPE

MODULE_DIR = os.path.dirname(__file__)


class MessageTestCase(TestCase):
    def __init__(self, methodName='runTest'):
        super(MessageTestCase, self).__init__(methodName=methodName)

        with open(os.path.join(MODULE_DIR, 'files', 'message.txt')) as fh:
            self.message_text = fh.read()

    def setUp(self):
        self.message = Message(1, SAMPLE_ENVELOPE, self.message_text, None)

    def test_parse_body(self):
        self.assertEqual(2, len(self.message.parsed))

    def test_plain(self):
        self.assertEqual('testing.\r\n', self.message.plain)

    def test_html(self):
        self.assertEqual('<div dir="ltr">testing.</div>\r\n', self.message.html)
