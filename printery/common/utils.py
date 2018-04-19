# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from uuid import UUID

from operator import itemgetter

from django.conf import settings


def get_protocol():
    """
    Return protocol of site. If ``SECURE_SSL_REDIRECT`` is ``True`` than return ``https`` else return ``http``
    Usage:
    >>> get_protocol()

    :return: String
    """
    is_secure = getattr(settings, 'SECURE_SSL_REDIRECT', False)
    if is_secure:
        return 'https'
    else:
        return 'http'
