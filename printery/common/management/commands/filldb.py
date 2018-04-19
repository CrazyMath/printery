# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import sys

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from printery.articles.factories import ArticleFactory

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        sys.stdout.write('Started fill db\r\n')
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create(
                username='admin',
                email='admin@example.com',
                is_staff=True,
                is_superuser=True,
            )
            admin.set_password('test1234')
            admin.save()
            sys.stdout.write('Admin user was created\r\n')

        if not User.objects.filter(username='writer').exists():
            admin = User.objects.create(
                username='writer',
                email='writer@example.com',
                role=User.WRITER
            )
            admin.set_password('test1234')
            admin.save()
            sys.stdout.write('Writer user was created\r\n')

        if not User.objects.filter(username='editor').exists():
            admin = User.objects.create(
                username='editor',
                email='editor@example.com',
                role=User.EDITOR
            )
            admin.set_password('test1234')
            admin.save()
            sys.stdout.write('Editor user was created\r\n')

        ArticleFactory.create_batch(30)
        sys.stdout.write('30 Articles was created\r\n')

        sys.stdout.write('Completed fill db\r\n')
