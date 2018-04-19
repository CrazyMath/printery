# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import factory
from django.utils.lorem_ipsum import words

from .models import Article


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    @factory.lazy_attribute
    def title(self):
        return words(5, common=False)
