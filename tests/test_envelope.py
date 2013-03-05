from unittest import TestCase

from imapbot.envelope import Envelope

from helpers import SAMPLE_ENVELOPE


class EnvelopeTestCase(TestCase):
    def setUp(self):
        self.envelope = Envelope(SAMPLE_ENVELOPE)

    def test_value_error(self):
        self.assertRaises(ValueError, lambda: self.envelope['nothere'])

    def test_get_by_name(self):
        self.assertEqual('Mon, 4 Mar 2013 17:51:24 -0800', self.envelope['date'])

    def test_get_by_index(self):
        self.assertEqual('Mon, 4 Mar 2013 17:51:24 -0800', self.envelope[0])

    def test_get_email(self):
        self.assertEqual('roberto.c.aguilar@gmail.com', self.envelope.get_email('from'))
