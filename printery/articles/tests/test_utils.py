# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.test import TestCase

from common.utils import get_protocol


class TestGetProtocol(TestCase):
    def test_get_protocol(self):
        settings.SECURE_SSL_REDIRECT = False
        self.assertEqual(get_protocol(), 'http')

        settings.SECURE_SSL_REDIRECT = True
        self.assertEqual(get_protocol(), 'https')
