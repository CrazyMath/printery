# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import sys
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        sys.stdout.write('Started fill db\r\n')

        sys.stdout.write('Completed fill db\r\n')
