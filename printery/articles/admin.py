# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    fields = ('title',)
    list_display = ('title', 'article_url', 'status', 'writer', 'editor', 'create_at')
    date_hierarchy = 'create_at'
    search_fields = ('title', 'writer__username', 'editor__username')


admin.site.register(Article, ArticleAdmin)
