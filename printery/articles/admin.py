# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)
